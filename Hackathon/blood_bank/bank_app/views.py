from django.shortcuts import render, redirect, get_object_or_404
from .models import UserDetail, DonorDetail, PatientDetails
from django.contrib import messages
from django.utils import timezone
import datetime
from .scoring import priority_score
from .matching import find_match, COMPATIBILITY
from .llm_urgency import extract_cohere_urgency


def index(request):
    donors = DonorDetail.objects.all()
    total_donors = donors.count()
    
    # Distinct blood groups available from donors
    available_blood_groups = donors.values_list('blood_group', flat=True).distinct()
    
    # Active requests to display on homepage (approved patients only)
    needy_patients = PatientDetails.objects.filter(is_approved=True)
    
    context = {
        'donors': donors,
        'total_donors': total_donors,
        'available_blood_groups': available_blood_groups,
        'needy_patients': needy_patients,
    }
    return render(request, 'html/index.html', context)


def user_registration(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        password = request.POST.get('password', '')
        blood_group = request.POST.get('blood_group', '')
        profile_pic = request.FILES.get('profile_pic')
        
        if profile_pic and not profile_pic.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            messages.error(request, "Only image files are allowed")
            return redirect("user-registration")

        email_list = UserDetail.objects.filter(email=email)
        if email_list.exists():
            messages.error(request, "The Email is already registered, please try another one")
            return redirect("user-registration")
        else:
            u = UserDetail(
                name=name,
                email=email,
                phone=phone,
                address=address,
                password=password,
                blood_group=blood_group,
                profile_pic=profile_pic
            )
            u.save()
            messages.success(request, "User registered successfully!")
            return redirect('user-login')
            
    return render(request, 'user/user_registration.html')


def donor_registration(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        locality = request.POST.get('address', '') or request.POST.get('locality', '')
        blood_group = request.POST.get('blood_group', '')
        last_donation_date = request.POST.get('last_donation_date') or None
        never_donated = request.POST.get('never_donated') == 'on'
        health_conditions = request.POST.get('health_conditions', '')

        email_list = DonorDetail.objects.filter(email=email)
        if email_list.exists():
            messages.error(request, "The Email is already registered as a donor, please try another one")
            return redirect("donor-registration")
        else:
            d = DonorDetail(
                name=name,
                email=email,
                phone=phone,
                password=password,
                locality=locality,
                blood_group=blood_group,
                last_donation_date=last_donation_date,
                never_donated=never_donated,
                health_conditions=health_conditions
            )
            d.save()
            messages.success(request, "Donor registered successfully!")
            return redirect("donor-login")
            
    return render(request, 'donor/donor_registration.html')


def patient_registration(request):
    """
    Registers incoming patient emergency requests and saves directly into PatientDetails table.
    """
    if request.method == "POST":
        patient_name = request.POST.get('patient_name', '')
        patient_phone = request.POST.get('patient_phone', '')
        patient_email = request.POST.get('patient_email', '')
        password = request.POST.get('password', '')
        required_blood_group = request.POST.get('required_blood_group', '')
        locality = request.POST.get('locality', '')
        condition = request.POST.get('condition', '')
        hospital = request.POST.get('hospital', '')
        medical_report = request.FILES.get('medical_report')

        if PatientDetails.objects.filter(patient_email=patient_email).exists():
            messages.error(request, "A request with this email already exists.")
            return redirect('patient-registration')

        PatientDetails.objects.create(
            patient_name=patient_name,
            patient_phone=patient_phone,
            patient_email=patient_email,
            password=password,
            required_blood_group=required_blood_group,
            locality=locality,
            condition=condition,
            hospital=hospital,
            medical_report=medical_report
        )
        messages.success(request, "Emergency blood request submitted successfully!")
        return redirect('admin_priority_dashboard')

    return render(request, 'patient/emergency_request.html')


def approve_patient(request, patient_email):
    """
    Admin verification action that marks patient request verified.
    """
    patient = get_object_or_404(PatientDetails, patient_email=patient_email)
    patient.is_approved = True
    patient.save()
    messages.success(request, f"Patient request for {patient.patient_name} verified!")
    return redirect('admin_priority_dashboard')


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email', '') or request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = UserDetail.objects.filter(email=email, password=password)
        if user.exists():
            request.session['session_key'] = email
            request.session['role'] = "user"
            messages.success(request, "Logged in successfully!")
            return redirect('user-home')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('user-login')
            
    return render(request, 'user/user_login.html')


def donor_login(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        donor = DonorDetail.objects.filter(email=email, password=password)
        if donor.exists():
            request.session['session_key'] = email
            request.session['role'] = "donor"
            messages.success(request, "Logged in successfully!")
            return redirect('donor-home')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('donor-login')
            
    return render(request, 'donor/donor_login.html')


def donor_home(request):
    donor_email = request.session.get('session_key')
    current_donor = None
    if donor_email:
        current_donor = DonorDetail.objects.filter(email=donor_email).first()

    patient_requests = PatientDetails.objects.filter(is_approved=True)

    context = {
        'donor': current_donor,
        'patient_requests': patient_requests,
        'total_requests': patient_requests.count(),
    }
    return render(request, 'donor/donor_home.html', context)


def user_home(request):
    user_email = request.session.get('session_key')
    current_user = None
    if user_email:
        current_user = UserDetail.objects.filter(email=user_email).first()

    # Filter donatable donors: either never donated or last donation was >= 90 days ago
    cutoff_date = timezone.now().date() - datetime.timedelta(days=90)
    all_donors = DonorDetail.objects.all()
    eligible_donors = [
        d for d in all_donors
        if d.never_donated or d.last_donation_date is None or d.last_donation_date <= cutoff_date
    ]

    context = {
        'user': current_user,
        'available_donors': eligible_donors,
        'total_donors': len(eligible_donors),
    }
    return render(request, 'user/user_home.html', context)


def donor_info(request):
    user_email = request.session.get('session_key')
    current_user = UserDetail.objects.filter(email=user_email).first() if user_email else None

    cutoff_date = timezone.now().date() - datetime.timedelta(days=90)
    all_donors = DonorDetail.objects.all()
    eligible_donors = [
        d for d in all_donors
        if d.never_donated or d.last_donation_date is None or d.last_donation_date <= cutoff_date
    ]

    # If user is logged in and has a blood group, filter donors by compatibility
    if current_user and current_user.blood_group:
        user_blood = current_user.blood_group.upper()
        compatible_groups = COMPATIBILITY.get(user_blood, [user_blood])
        eligible_donors = [d for d in eligible_donors if d.blood_group.upper() in compatible_groups]

    return render(request, 'user/donor_info.html', {'donors': eligible_donors})


def user_info(request):
    patients = PatientDetails.objects.filter(is_approved=True)
    return render(request, 'donor/user_info.html', {'patients': patients})


def aboutUS(request):
    return render(request, 'html/abouUS.html')


def user_edit(request):
    user_email = request.session.get('session_key')
    if not user_email:
        messages.error(request, "Please log in first.")
        return redirect('user-login')

    user = UserDetail.objects.filter(email=user_email).first()

    if request.method == "POST":
        if user:
            user.name = request.POST.get('name', user.name)
            user.phone = request.POST.get('phone', user.phone)
            user.address = request.POST.get('address', user.address)
            
            profile_pic = request.FILES.get('profile_pic')
            if profile_pic:
                user.profile_pic = profile_pic
                
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('edit-user-details')

    return render(request, 'user/edit_details.html', {'user_key': user})    


def donor_edit(request):
    donor_email = request.session.get('session_key')
    if not donor_email:
        messages.error(request, "Please log in as donor first.")
        return redirect('donor-login')

    donor = DonorDetail.objects.filter(email=donor_email).first()

    if request.method == "POST":
        if donor:
            donor.name = request.POST.get('name', donor.name)
            donor.phone = request.POST.get('phone', donor.phone)
            donor.blood_group = request.POST.get('blood_group', donor.blood_group)
            donor.locality = request.POST.get('locality', donor.locality)
            donor.health_conditions = request.POST.get('health_conditions', donor.health_conditions)
            donor.save()
            messages.success(request, "Donor profile updated successfully!")
            return redirect('edit-donor-details')

    return render(request, 'donor/edit_details.html', {'donor_key': donor})    


# --- AI PRIORITIZER & MATCHING VIEWS ---

def admin_priority_dashboard(request):
    """
    Ranks all patient requests for the admin/hospital view using AI priority scoring.
    """
    patients_qs = PatientDetails.objects.all()
    ranked_patients = []

    for p in patients_qs:
        # 1. Base rule-based score
        base_res = priority_score(
            blood_req=p.required_blood_group,
            notes=p.condition or "",
            created_at=None
        )

        # 2. Cloud LLM semantic urgency boost
        llm_res = extract_cohere_urgency(p.condition or "")

        # 3. Combine scores and explanations
        total_score = base_res["score"] + llm_res.get("score_boost", 0)
        reasons = [base_res["reason"]]
        if llm_res.get("reason_tag"):
            reasons.append(llm_res["reason_tag"])

        ranked_patients.append({
            "patient_name": p.patient_name,
            "patient_phone": p.patient_phone,
            "patient_email": p.patient_email,
            "required_blood_group": p.required_blood_group,
            "locality": p.locality,
            "condition": p.condition,
            "hospital": p.hospital,
            "priority_score": total_score,
            "priority_reason": " | ".join(reasons)
        })

    # Sort descending by priority score
    ranked_patients.sort(key=lambda x: x["priority_score"], reverse=True)

    return render(request, "html/act_respond.html", {"patients": ranked_patients})


def match_donors_for_patient(request, patient_email):
    """
    Finds verified, compatible nearby donors for a specific patient.
    """
    patient = get_object_or_404(PatientDetails, patient_email=patient_email)

    # Format patient data expected by matching.py
    patient_dict = {
        "blood_group_needed": patient.required_blood_group,
        "locality": patient.locality
    }

    # Format donor queryset for find_match()
    donors_qs = DonorDetail.objects.all()
    donor_pool = []
    for d in donors_qs:
        donor_pool.append({
            "id": d.email,
            "name": d.name,
            "phone": d.phone,
            "blood_group": d.blood_group,
            "locality": d.locality,
            "verified": True,
            "is_available": True,
            "last_donation_date": d.last_donation_date
        })

    matched_donors = find_match(patient_dict, donor_pool)

    return render(request, "user/donor_info.html", {
        "patient": patient,
        "matched_donors": matched_donors
    })

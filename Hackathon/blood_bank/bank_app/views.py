from django.shortcuts import render, redirect
from .models import UserDetail, DonorDetail, PatientDetails
from django.contrib import messages
from django.utils import timezone


# Create your views here.

def index(request):
    donors = DonorDetail.objects.all()
    total_donors = donors.count()
    
    # Get distinct blood groups available in DonorDetail
    available_blood_groups = donors.values_list('blood_group', flat=True).distinct()
    
    context = {
        'donors': donors,
        'total_donors': total_donors,
        'available_blood_groups': available_blood_groups,
    }
    return render(request, 'html/index.html', context)


def user_registration(request):
    if request.method == "GET":
        return render(request, 'user/user_registration.html')
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        password = request.POST['password']
        blood_group = request.POST['blood_group']
        profile_pic = request.FILES.get('profile_pic')
        
        if profile_pic and not profile_pic.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            messages.error(request, "Only image files are allowed")
            return redirect("user-registration")

        email_list = UserDetail.objects.filter(email=email)
        # check email existence before registering
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


def donor_registration(request):
    if request.method == "GET":
        return render(request, 'donor/donor_registration.html')
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password', '')
        locality = request.POST.get('address', '') or request.POST.get('locality', '')
        blood_group = request.POST.get('blood_group')
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

def user_login(request):
    if request.method == "GET":
        return render(request, 'user/user_login.html')
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

def donor_login(request):
    if request.method == "GET":
        return render(request, 'donor/donor_login.html')
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

def donor_home(request):
    donor_email = request.session.get('session_key')
    current_donor = None
    if donor_email:
        current_donor = DonorDetail.objects.filter(email=donor_email).first()

    patient_requests = PatientDetails.objects.all()

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

    available_donors = DonorDetail.objects.all()

    context = {
        'user': current_user,
        'available_donors': available_donors,
        'total_donors': available_donors.count(),
    }
    return render(request, 'user/user_home.html', context)

def donor_info(request):
    donors = DonorDetail.objects.all()
    return render(request, 'user/donor_info.html', {'donors': donors})

def user_info(request):
    patients = PatientDetails.objects.all()
    return render(request, 'donor/user_info.html', {'patients': patients})

def aboutUS(request):
    return render(request,'html/abouUS.html')

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




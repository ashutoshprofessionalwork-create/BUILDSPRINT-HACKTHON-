from django.shortcuts import render, redirect
from .models import UserDetail, DonorDetail
from django.contrib import messages
from django.utils import timezone


# Create your views here.

def index(request):
    return render(request, 'html/index.html')


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
            return redirect("user-login")

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
            return redirect('user-registration')


def donor_registration(request):
    if request.method == "GET":
        return render(request, 'donor/donor_registration.html')
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
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
                locality=locality,
                blood_group=blood_group,
                last_donation_date=last_donation_date,
                never_donated=never_donated,
                health_conditions=health_conditions
            )
            d.save()
            messages.success(request, "Donor registered successfully!")
            return redirect("donor-registration")




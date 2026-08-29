from django.shortcuts import render , redirect
from .models import UserDetail
from django.contrib import messages
from django.utils import timezone



# Create your views here.

def index(request):
    return render(request, 'html/index.html')


def user_registration(request):
    if request.method=="GET":
        return render(request, 'user/user_registration.html')
    if request.method=="POST":
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        address=request.POST['address']
        password=request.POST['password']
        blood_group=request.POST['blood_group']
        profile_pic=request.POST['profile_pic']
    if not profile_pic.name.lower().endswith((".jpg",".jpeg",".png",".gif",".webp")):
        messages.error(request,"only image files are allowed")
        return redirect("user-registration")    
    email_list=UserDetail.objects.filter(email=email)
    #check email exsitance before registering
    if len(email_list)>0:
        messages.error(request,"The Email has registered pls try another one")
        return redirect("user-registration")
    else:
        u=UserDetail(name=name,email=email,phone=phone,password=password,profile_pic=profile_pic)#craeting ofbject for UserDetails model
        u.save()#insert data
        return redirect('user-login')#logical name of url which is defined in urls.py file    



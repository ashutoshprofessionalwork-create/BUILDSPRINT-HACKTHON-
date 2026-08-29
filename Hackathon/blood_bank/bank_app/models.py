from django.db import models
from django.utils import timezone

#----------------------Blood Bank--------------------#

class UserDetail(models.Model):
    name=models.CharField(max_length=45)
    phone=models.CharField(max_length=13)
    email=models.EmailField(max_length=45, primary_key=True)
    address=models.CharField(max_length=100)
    password=models.CharField(max_length=20)
    blood_group=models.CharField()
    profile_pic=models.ImageField(default="", upload_to="userPics")

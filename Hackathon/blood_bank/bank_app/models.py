from django.db import models
from django.utils import timezone

#----------------------Blood Bank Models--------------------#

class UserDetail(models.Model):
    name = models.CharField(max_length=45)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=45, primary_key=True)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=5)
    profile_pic = models.ImageField(default="", upload_to="userPics")


class DonorDetail(models.Model):
    name = models.CharField(max_length=45)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=45, primary_key=True)
    password = models.CharField(max_length=20, default="")
    blood_group = models.CharField(max_length=5)
    locality = models.CharField(max_length=100, default="")
    last_donation_date = models.DateField(blank=True, null=True)
    never_donated = models.BooleanField(default=False)
    health_conditions = models.TextField(blank=True, null=True)


class PatientDetails(models.Model):
    patient_name = models.CharField(max_length=45)
    patient_phone = models.CharField(max_length=13)
    patient_email = models.EmailField(max_length=45, primary_key=True)
    password=models.CharField(max_length=20)
    required_blood_group = models.CharField(max_length=5)
    locality = models.CharField(max_length=100, default="")
    condition = models.TextField(blank=True, null=True)
    hospital = models.CharField(max_length=100, default="")
    medical_report = models.FileField(upload_to="medicalReports", null=True, blank=True)

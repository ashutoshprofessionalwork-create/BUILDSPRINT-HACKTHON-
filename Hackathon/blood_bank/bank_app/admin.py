from django.contrib import admin
from .models import UserDetail, DonorDetail, PatientDetails

admin.site.register(UserDetail)
admin.site.register(DonorDetail)
admin.site.register(PatientDetails)


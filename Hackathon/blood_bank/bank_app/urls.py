from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='home-page'),
    path('user-registration/',views.user_registration,name='user-registration'),
    path('donor-registration/',views.donor_registration,name='donor-registration'),
]

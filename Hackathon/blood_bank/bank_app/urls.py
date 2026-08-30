from django.urls import path
<<<<<<< HEAD
from . import views

urlpatterns = [
    path('priority-queue/', views.admin_priority_dashboard, name='admin_priority_dashboard'),
    path('match/<str:patient_email>/', views.match_donors_for_patient, name='match_donors_for_patient'),
    path('approve-patient/<str:patient_email>/', views.approve_patient, name='approve_patient'),
    path('patient-registration/', views.patient_registration, name='patient-registration'),
    path('', views.index, name='home-page'),
    path('user-registration/', views.user_registration, name='user-registration'),
    path('donor-registration/', views.donor_registration, name='donor-registration'),
    path('user-login/', views.user_login, name='user-login'),
    path('user-home/', views.user_home, name='user-home'),
    path('donor-login/', views.donor_login, name='donor-login'),
    path('donor-home/', views.donor_home, name='donor-home'),
    path('aboutUS/', views.aboutUS, name='aboutUS'),
    path('donor-info/', views.donor_info, name='donor-info'),
    path('user-info/', views.user_info, name='user-info'),
    path('edit-details-donor/', views.donor_edit, name='edit-donor-details'),
    path('edit-detials-user/', views.user_edit, name='edit-user-details'),
]
=======
from .import views

urlpatterns = [
    path('',views.index,name='home-page'),
    path('user-registration/',views.user_registration,name='user-registration'),
    path('donor-registration/',views.donor_registration,name='donor-registration'),
    path('user-login/',views.user_login,name='user-login'),
    path('user-home/',views.user_home,name='user-home'),
    path('donor-login/',views.donor_login,name='donor-login'),
    path('donor-home/',views.donor_home,name='donor-home'),
    path('aboutUS/',views.aboutUS,name='aboutUS'),
    path('donor-info/',views.donor_info,name='donor-info'),
    path('user-info/',views.user_info,name='user-info'),
    path('edit-details-donor/',views.donor_edit,name='edit-donor-details'),
    path('edit-detials-user/',views.user_edit,name='edit-user-details'),
]
>>>>>>> d2ff81020421b5956a8e5e59199447b2c3f96de4

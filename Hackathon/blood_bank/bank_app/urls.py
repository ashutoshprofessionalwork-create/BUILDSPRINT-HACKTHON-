from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='home-page'),
    path('user-registration/',views.user_registration,name='user-registration'),
    path('donor-registration/',views.donor_registration,name='donor-registration'),
    path('user-login/',views.user_login,name='user-login'),
    path('donor-login/',views.donor_login,name='donor-login'),
    path('aboutUS/',views.aboutUS,name='aboutUS'),
    path('donor-info/',views.donor_info,name='donor-info'),
    path('user-info/',views.user_info,name='user-info'),
]

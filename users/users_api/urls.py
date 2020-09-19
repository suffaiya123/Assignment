from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_api, name='signup_api'),
    path('users_detail/', views.users_details, name='users_detail'),
    path('temp_profile_image/', views.tempprofileimage),
    path('users_edit/', views.user_profile_edit, name='users_edit'),

]

# 127.0.0.1:8000/api/v1/signup/

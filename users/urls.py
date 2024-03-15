from django.urls import path

from users import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_in_otp/', views.sign_in_otp, name='sign_in_otp'),
    path('sign_in_otp_confirmation/', views.sign_in_otp_confirmation, name='sign_in_otp_confirmation'),
    path('phone_auth/', views.phone_auth, name='phone_auth'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('rest_password_otp/', views.rest_password_otp, name='rest_password_otp'),
    path('sign_out/', views.sign_out, name='sign_out'),


    path('test_data/', views.test_data, name='test_data')
]

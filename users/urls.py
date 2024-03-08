from django.urls import path

from users import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('phone_auth/', views.phone_auth, name='phone_auth'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('rest_password_otp/', views.rest_password_otp, name='rest_password_otp'),
]

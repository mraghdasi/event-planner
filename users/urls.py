from django.urls import path

from users import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.login, name='login'),
    path('otp/', views.otp, name='otp'),
]

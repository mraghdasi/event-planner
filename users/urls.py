from django.urls import path

from users import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),


    # APIs
    path('edit_profile_api/', views.edit_profile_api, name='edit_profile_api')
]

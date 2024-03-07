from django.urls import path
from django.conf.urls.static import static
from EventPlanner import settings
from admin_dash import views


urlpatterns = [
                  path('', views.admin_home, name='admin_home'),
                  path('users/', views.admin_users, name='admin_users'),
                  path('meetings/', views.admin_meetings, name='admin_meetings'),
                  path('rooms/', views.admin_rooms, name='admin_rooms'),
                  path('teams/', views.admin_teams, name='admin_teams'),



              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

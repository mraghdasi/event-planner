from django.conf.urls.static import static
from django.urls import path

from EventPlanner import settings
from admin_dash import views

urlpatterns = [
                  path('', views.admin_home, name='admin_home'),
                  path('users/', views.admin_users, name='admin_users'),
                  path('meetings/', views.admin_meetings, name='admin_meetings'),
                  path('rooms/', views.admin_rooms, name='admin_rooms'),
                  path('teams/', views.admin_teams, name='admin_teams'),
                  path('edit_user/<int:pk>', views.edit_user, name='edit_user'),
                  path('edit_team/<int:pk>', views.edit_team, name='edit_team'),
                  path('add_team/', views.add_team, name='add_team'),
                  path('edit_room/<int:pk>', views.edit_room, name='edit_room'),
                  path('add_room/', views.add_room, name='add_room'),
                  path('edit_meeting/<int:pk>', views.edit_meeting, name='edit_meeting'),
                  path('delete_meeting/<int:pk>', views.delete_meeting, name='delete_meeting'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

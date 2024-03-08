from django.conf.urls.static import static
from django.urls import path

from EventPlanner import settings
from meetings import views

app_name = 'meeting'

urlpatterns = [
                  path('room/<int:id>/', views.RoomDetail.as_view(), name='room_detail'),
                  path('', views.RoomList.as_view(), name='room_list'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

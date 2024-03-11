from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path

from EventPlanner import settings
from meetings import views

app_name = 'meeting'

urlpatterns = [
                  path('room/<int:id>/', login_required(views.RoomDetail.as_view(), login_url='sign_in'),
                       name='room_detail'),
                  path('', login_required(views.RoomList.as_view(), login_url='sign_in'), name='room_list'),

                  path('create_comment/<int:pk>', views.create_comment, name='create_comment'),
                  path('room_comments/<int:pk>', views.room_comments, name='room_comments'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

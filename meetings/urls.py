from django.urls import path

from meetings.views import CreateRoomView

app_name = 'meeting'
urlpatterns = [
    path('create-room/', CreateRoomView.as_view(), name='create_room'),
    path('create-room/<int:pk>/', CreateRoomView.as_view(), name='detail_room'),
]

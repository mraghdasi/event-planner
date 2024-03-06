from django.conf.urls.static import static
from django.urls import path

from EventPlanner import settings
from meetings import views

urlpatterns = [
                  path('', views.homepage, name='homepage'),
                  path('more/', views.more, name='more'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

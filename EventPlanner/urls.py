from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from EventPlanner import settings
from main import views as ma

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', ma.homepage, name='homepage')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

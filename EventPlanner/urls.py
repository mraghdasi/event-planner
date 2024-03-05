from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

from EventPlanner import settings
from users.views import index

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index, name='index'),
                  path('users', include('users.urls')),
                  path('meetings/', include('meetings.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

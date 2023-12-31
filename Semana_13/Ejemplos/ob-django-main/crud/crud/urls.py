
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contactos/', include('contactos.urls')),
    path('tareas/', include('tareas.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

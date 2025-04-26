#from django.contrib import admin
from django.urls import path
from .views import index, recurso_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name="index"),
    path('recurso/', recurso_view, name="recurso"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#from django.contrib import admin
from django.urls import path,include
from .views import index, recurso_view, ItemViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
    path('recurso/', recurso_view, name="recurso"),
    path('api/', include(router.urls)),  # Cambia la raíz del router a '/api/'
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
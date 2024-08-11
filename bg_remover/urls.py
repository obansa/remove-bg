from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'remover', views.RemoverViewSet, basename='remove')
router.register(r'image-upload', views.ImageUploadViewSet, basename='image-upload')

urlpatterns = [
    path('api/', include(router.urls)),
    # path('register/', views.RemoverViewSet.as_view({'get': 'list'}), name='register'),
]
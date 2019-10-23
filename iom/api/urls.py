from rest_framework.routers import DefaultRouter
from api.viewsets import core_viewsets
from django.urls import path, include

router = DefaultRouter()
router.register(r'slider', core_viewsets.SliderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
from rest_framework.routers import DefaultRouter
from api.viewsets import core_viewsets
from django.urls import path, include
from api.viewsets import core_viewsets

router = DefaultRouter()
router.register(r'slider', core_viewsets.SliderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dummy_api', core_viewsets.dummy_api_view),
]

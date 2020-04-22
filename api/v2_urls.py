from django.urls import path
from api.viewsets import core_viewsets

urlpatterns = [
    path('openspace', core_viewsets.OpenSpaceView.as_view({'get': 'list'}), name='open_space'),
]

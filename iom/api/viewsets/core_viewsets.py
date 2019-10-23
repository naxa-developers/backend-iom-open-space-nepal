from rest_framework import viewsets
from core.models import Slider
from api.serializers.core_serializers import SliderSerializer


class SliderViewSet(viewsets.ModelViewSet):
    serializer_class = SliderSerializer
    queryset = Slider.objects.all()
    permission_classes = []





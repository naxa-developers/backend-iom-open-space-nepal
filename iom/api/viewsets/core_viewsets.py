from rest_framework import viewsets
from core.models import Slider, CreateOpenSpace
from api.serializers.core_serializers import SliderSerializer,\
    CreateOpenSpaceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


class SliderViewSet(viewsets.ModelViewSet):
    serializer_class = SliderSerializer
    queryset = Slider.objects.all()
    permission_classes = []


class CreateOpenSpaceViewSet(viewsets.ModelViewSet):
    serializer_class = CreateOpenSpaceSerializer
    queryset = CreateOpenSpace.objects.all()
    permission_classes = []


@api_view(['GET',])
def dummy_api_view(request):
    data = {
        "open_space": 192929,
        "district": 34,
        "municipality": 78,
        "total_area": 3737229,
        "total_capacity": 89393,

    }
    return Response({"data": data})



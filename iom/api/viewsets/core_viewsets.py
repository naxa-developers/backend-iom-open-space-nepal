from rest_framework import viewsets
from core.models import Slider, CreateOpenSpace, Resource
from api.serializers.core_serializers import SliderSerializer,\
    CreateOpenSpaceSerializer, ResourceSerializer
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


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    permission_classes = []

    def filter_queryset(self, queryset):
        category = self.request.query_params.get('category')
        document_type = self.request.query_params.get('document_type')

        if category and document_type:
            return self.queryset.filter(category=category,
                                        document_type=document_type)
        else:
            return self.queryset




@api_view(['GET', ])
def dummy_api_view(request):
    data = {
        "open_space": 192929,
        "district": 34,
        "municipality": 78,
        "total_area": 3737229,
        "total_capacity": 89393,

    }
    return Response({"data": data})



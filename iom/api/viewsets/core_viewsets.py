from rest_framework import viewsets
from core.models import Slider, CreateOpenSpace, Resource, Province, District,\
    Municipality, SuggestedUse, Services, Question, OpenSpace, Report
from api.serializers.core_serializers import SliderSerializer,\
    CreateOpenSpaceSerializer, ResourceSerializer, ProvinceSerializer,\
    DistrictSerializer, MunicipalitySerializer, SuggestedUseSerializer,\
    ServiceSerializer, QuestionSerializer, OpenSpaceSerializer,\
    ReportSerializer
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
        content = self.request.query_params.get('content')

        if content:
            return Resource.objects.filter(title__icontains=content)

        elif category and document_type:
            return Resource.objects.filter(category=category,
                                           document_type=document_type)

        else:
            return Resource.objects.all()


class ProvinceViewSet(viewsets.ModelViewSet):
    serializer_class = ProvinceSerializer
    queryset = Province.objects.all()
    permission_classes = []


class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()
    permission_classes = []


class SuggestedUseViewSet(viewsets.ModelViewSet):
    serializer_class = SuggestedUseSerializer
    queryset = SuggestedUse.objects.all()
    permission_classes = []


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Services.objects.all()
    permission_classes = []


class MunicipalityViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipalitySerializer
    queryset = Municipality.objects.all()
    permission_classes = []


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = []


class OpenSpaceViewSet(viewsets.ModelViewSet):
    serializer_class = OpenSpaceSerializer
    queryset = OpenSpace.objects.all()
    permission_classes = []


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = []


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



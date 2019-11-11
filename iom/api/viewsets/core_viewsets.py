from rest_framework import viewsets
from core.models import Slider, CreateOpenSpace, Resource, Province, District,\
    Municipality, SuggestedUse, Services, Question, OpenSpace, Report
from api.serializers.core_serializers import SliderSerializer,\
    CreateOpenSpaceSerializer, ResourceSerializer, ProvinceSerializer,\
    DistrictSerializer, MunicipalitySerializer, SuggestedUseSerializer,\
    ServiceSerializer, QuestionSerializer, OpenSpaceSerializer,\
    ReportSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
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


class OpenSpaceLandingApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = []
        open_spaces = OpenSpace.objects.all()
        for open_space in open_spaces:
            if open_space.image:
                data.append(
                    {
                        "title": open_space.title,
                        "province": open_space.province.name,
                        "district": open_space.district.name,
                        "municipality": open_space.municipality.name,
                        "address": open_space.address,
                        "image": open_space.image.url,
                        "latitude": open_space.latitude,
                        "longitude": open_space.longitude
                    }
                )
            else:
                data.append(
                    {
                        "title": open_space.title,
                        "province": open_space.province.name,
                        "district": open_space.district.name,
                        "municipality": open_space.municipality.name,
                        "address": open_space.address,
                        "image": None,
                        "latitude": open_space.latitude,
                        "longitude": open_space.longitude
                    }
                )

        return Response({"data": data})


class DistrictApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = []
        districts = District.objects.all()

        for district in districts:
            data.append(
                {
                    "id": district.id,
                    "name": district.name
                }
            )

        return Response({"data": data})


class MunicipalityApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = []
        municipalities = Municipality.objects.all()

        for municipality in municipalities:
            data.append(
                {
                    "id": municipality.id,
                    "name": municipality.name
                }
            )

        return Response({"data": data})


class ProvinceApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = []
        provinces = Province.objects.all()

        for province in provinces:
            data.append(
                {
                    "id": province.id,
                    "name": province.name
                }
            )

        return Response({"data": data})


# class GlimpseOfOpenSpace(APIView):
#     authentication_classes = []
#     permission_classes = []
#
#     def get(self, request):
#         open_space = OpenSpace.objects.all()
#         district = District.objects.all().count()
#         municipality = Municipality.objects.all().count()
#         total_area =
#         total_capacity =









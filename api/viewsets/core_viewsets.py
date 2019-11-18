from rest_framework import viewsets
from core.models import Slider, CreateOpenSpace, Resource, Province, District, \
    Municipality, SuggestedUse, Services, OpenSpace, Report
from api.serializers.core_serializers import SliderSerializer, \
    CreateOpenSpaceSerializer, ResourceSerializer, ProvinceSerializer, \
    DistrictSerializer, MunicipalitySerializer, SuggestedUseSerializer, \
    ServiceSerializer, OpenSpaceSerializer, \
    ReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.core.serializers import serialize
import json


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


# class QuestionViewSet(viewsets.ModelViewSet):
#     serializer_class = QuestionSerializer
#     queryset = Questions.objects.all()
#     permission_classes = []


class OpenSpaceViewSet(viewsets.ModelViewSet):
    serializer_class = OpenSpaceSerializer
    queryset = OpenSpace.objects.all()
    permission_classes = []


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = []

    def perform_create(self, serializer):
        location = self.queryset.open_space.location
        serializer.save(location=location)


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
                        "id": open_space.id,
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
                        "id": open_space.id,
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
                    "name": district.name,
                    "province": district.province.name
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
                    "name": municipality.name,
                    "district": municipality.district.name
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


class GlimpseOfOpenSpace(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        open_space = OpenSpace.objects.all().count()
        district = OpenSpace.objects.values('district').distinct().count()
        municipality = OpenSpace.objects.values(
            'municipality').distinct().count()
        total_area = OpenSpace.objects.aggregate(
            Sum('total_area')).get('total_area__sum')
        total_capacity = OpenSpace.objects.aggregate(
            Sum('capacity')).get('capacity__sum')

        data = {
            "open_space": open_space,
            "district": district,
            "municipality": municipality,
            "total_area": total_area,
            "total_capacity": total_capacity,

        }

        return Response({"data": data})


class OpenSpaceGeojsonViewSet(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        serializers = serialize('geojson', OpenSpace.objects.all(),
                                geometry_field='polygons',
                                fields=('pk', 'title', 'description', 'status',
                                        'catchment_area', 'ownership',
                                        'elevation', 'access_to_site',
                                        'special_feature', 'address',
                                        'province', 'district',
                                        'municipality', 'ward', 'capacity',
                                        'total_area', 'usable_area', 'image',
                                        'maps', 'location', 'centroid', 'latitude'))

        # print(serializers)
        # a = OpenSpace.objects.filter(id=4)
        # print(a[0].polygons.centroid.x)

        OpenSpaceGeoJson = json.loads(serializers)
        return Response(OpenSpaceGeoJson)


class SingleOpenSpaceGeojsonViewSet(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        open_id = self.request.query_params.get('id')
        serializers = serialize('geojson',
                                OpenSpace.objects.filter(id=open_id),
                                geometry_field='polygons',
                                fields=('pk', 'title', 'description', 'status',
                                        'catchment_area', 'ownership',
                                        'elevation', 'access_to_site',
                                        'special_feature', 'address',
                                        'province', 'district',
                                        'municipality', 'ward', 'capacity',
                                        'total_area', 'usable_area', 'image',
                                        'maps', 'location'))

        open_space_geo_json = json.loads(serializers)
        return Response(open_space_geo_json)


class DistrictGeojsonViewSet(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        district_id = self.request.query_params.get('id')
        serializers = serialize('geojson',
                                District.objects.filter(id=district_id),
                                geometry_field='boundary',
                                fields=('pk', 'name', 'province'))

        district_geo_json = json.loads(serializers)
        return Response(district_geo_json)


class MunicipalityGeojsonViewSet(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        municipality_id = self.request.query_params.get('id')
        serializers = serialize('geojson', Municipality.objects.filter(
            id=municipality_id), geometry_field='boundary',
                                fields=('pk', 'name', 'district'))

        district_geo_json = json.loads(serializers)
        return Response(district_geo_json)

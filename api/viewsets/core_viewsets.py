from rest_framework import viewsets
from core.models import Slider, CreateOpenSpace, Resource, Province, District, \
    Municipality, SuggestedUse, Services, OpenSpace, Report, AvailableFacility, \
    Gallery
from api.serializers.core_serializers import SliderSerializer, \
    CreateOpenSpaceSerializer, ResourceSerializer, ProvinceSerializer, \
    DistrictSerializer, MunicipalitySerializer, SuggestedUseSerializer, \
    ServiceSerializer, OpenSpaceSerializer, \
    ReportSerializer, AvailableFacilitySerializer, \
    GallerySerializer, OpenSpaceAttributeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.core.serializers import serialize
import json
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from rest_framework.parsers import JSONParser
import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from datetime import datetime, timedelta
from rest_framework_swagger.views import get_swagger_view
from rest_framework.decorators import api_view
from django.http import Http404, HttpResponse
from django.db import connection
from django.contrib.gis.geos import Point


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

#
# class QuestionViewSet(viewsets.ModelViewSet):
#     serializer_class = QuestionSerializer
#     queryset = Questions.objects.all()
#     permission_classes = []


class OpenSpaceViewSet(viewsets.ModelViewSet):
    serializer_class = OpenSpaceSerializer
    queryset = OpenSpace.objects.all()
    permission_classes = []


class GalleryViewSet(viewsets.ModelViewSet):
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()
    permission_classes = []

    def filter_queryset(self, queryset):
        typee = self.request.query_params.get('type')
        if typee == 'map':
            return queryset.filter(type='map')

        elif typee == 'image':
            return queryset.filter(type='image')

        else:
            return queryset


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = []

    def filter_queryset(self, queryset):
        print(queryset)
        reports = Report.objects.filter(date__gte=datetime.now() - timedelta(days=7))
        status = self.request.query_params.get('status')
        # urgency = self.request.query_params.get('urgency')
        openspace = self.request.query_params.get('id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if status:
            return reports.filter(status=status)

        elif openspace:
            return queryset.filter(open_space=openspace)

        elif start_date and end_date:
            return queryset.filter(date__range=(start_date, end_date))

        elif start_date and end_date and status:
            return queryset.filter(date__range=(start_date, end_date), status=status)

        else:
            return queryset


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
                        "province": open_space.province.id,
                        "district": open_space.district.id,
                        "municipality": open_space.municipality.id,
                        "address": open_space.address,
                        "image": open_space.image.url,
                        "latitude": open_space.polygons.centroid.y,
                        "longitude": open_space.polygons.centroid.x,
                        "centroid": [open_space.polygons.centroid.x, open_space.polygons.centroid.y]
                    }
                )
            else:
                data.append(
                    {
                        "id": open_space.id,
                        "title": open_space.title,
                        "province": open_space.province.id,
                        "district": open_space.district.id,
                        "municipality": open_space.municipality.id,
                        "address": open_space.address,
                        "image": None,
                        "latitude": open_space.polygons.centroid.y,
                        "longitude": open_space.polygons.centroid.x,
                        "centroid": [open_space.polygons.centroid.x, open_space.polygons.centroid.y]
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


class ProvinceGeojsonViewSet(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        province_id = self.request.query_params.get('id')
        if province_id:
            serializers = serialize('geojson',
                                    Province.objects.filter(id=province_id),
                                    geometry_field='boundary',
                                    fields=('pk', 'name', 'code'))
        else:
            serializers = serialize('geojson',
                                    Province.objects.all(),
                                    geometry_field='boundary',
                                    fields=('pk', 'name', 'code'))
        province_geo_json = json.loads(serializers)
        return Response(province_geo_json)


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


class NearByMeViewSet(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        api_json = {}
        open_space_id = self.request.query_params.get('id')
        distance = self.request.query_params.get('distance')
        count = int(self.request.query_params.get('count'))
        type = self.request.query_params.get('type')
        open_space = OpenSpace.objects.get(id=open_space_id)
        longitude = open_space.centroid[0]
        latitude = open_space.centroid[1]
        openspace_location = GEOSGeometry('POINT({} {})'.format(longitude, latitude), srid=4326)
        resource_queryset = AvailableFacility.objects \
                                .filter(location__distance_lte=(openspace_location, D(km=distance)), type=type) \
                                .annotate(distance=Distance('location', openspace_location)) \
                                .order_by('distance')[0:count]
        print(resource_queryset)
        resource_json = AvailableFacilitySerializer(resource_queryset, many=True)
        json = JSONRenderer().render(resource_json.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        api_json['facility'] = data

        return Response(api_json)


class NearByMeOpenSpace(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        api_json = {}
        count = int(self.request.query_params.get('count'))
        distance = self.request.query_params.get('distance')
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        user_location = GEOSGeometry('POINT({} {})'.format(longitude, latitude), srid=4326)

        resource_queryset = OpenSpace.objects \
                                .filter(polygons__distance_lte=(user_location, D(km=distance))) \
                                .annotate(distance=Distance('polygons', user_location)) \
                                .order_by('distance')[0:count]
        print(resource_queryset)
        resource_json = OpenSpaceAttributeSerializer(resource_queryset, many=True)
        json = JSONRenderer().render(resource_json.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        api_json['open_space'] = data
        return Response(api_json)


class AvailableFacilityViewSet(viewsets.ModelViewSet):
    serializer_class = AvailableFacilitySerializer
    queryset = AvailableFacility.objects.all()
    authentication_classes = []


@api_view(['GET'])
def province_tile(request, zoom, x, y):
    """
    Custom view to serve Mapbox Vector Tiles for the custom polygon model.
    """
    if len(request.GET) == 0:
        sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, code, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_province) AS tile"
    else:
        try:
            dist = request.GET['district']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, code, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_province where id = " + dist + ") AS tile"

        except:
            print("")
        try:
            prov = request.GET['province']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, code, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_province where province_id_id = " + prov + ") AS tile"
        except:
            print("")

    with connection.cursor() as cursor:
        cursor.execute(sql_data, [zoom, x, y])
        tile = bytes(cursor.fetchone()[0])
        # return HttpResponse(len(tile))
        if not len(tile):
            raise Http404()
    return HttpResponse(tile, content_type="application/x-protobuf")



@api_view(['GET'])
def district_tile(request, zoom, x, y):
    """
    Custom view to serve Mapbox Vector Tiles for the custom polygon model.
    """
    if len(request.GET) == 0:
        sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, code, province_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_district) AS tile"
    else:
        try:
            dist = request.GET['district']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, code, province_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_district where id = " + dist + ") AS tile"
        except:
            print("")
        try:
            prov = request.GET['province']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, code, province_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_district where province_id_id = " + prov + ") AS tile"
        except:
            print("")

    with connection.cursor() as cursor:
        cursor.execute(sql_data, [zoom, x, y])
        tile = bytes(cursor.fetchone()[0])
        # return HttpResponse(len(tile))
        if not len(tile):
            raise Http404()
    return HttpResponse(tile, content_type="application/x-protobuf")


@api_view(['GET'])
def municipality_tile(request, zoom, x, y):
    """
    Custom view to serve Mapbox Vector Tiles for the custom polygon model.
    """
    if len(request.GET) == 0:
        sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, province_id, hlcit_code, district_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_municipality) AS tile"
    else:
        try:
            dist = request.GET['district']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, province_id, hlcit_code, district_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_municipality where id = " + dist + ") AS tile"
        except:
            print("")
        try:
            prov = request.GET['province']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, hlcit_code, province_id, district_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_municipality where province_id_id = " + prov + ") AS tile"
        except:
            print("")

    with connection.cursor() as cursor:
        cursor.execute(sql_data, [zoom, x, y])
        tile = bytes(cursor.fetchone()[0])
        # return HttpResponse(len(tile))
        if not len(tile):
            raise Http404()
    return HttpResponse(tile, content_type="application/x-protobuf")

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from core.models import Slider, CreateOpenSpace, Resource, Province, District, \
    Municipality, SuggestedUseList, ServiceList, OpenSpace, Report, AvailableFacility, \
    Gallery, SuggestedUseData, ServiceData, ServiceList
from api.serializers.core_serializers import SliderSerializer, \
    CreateOpenSpaceSerializer, ResourceSerializer, ProvinceSerializer, \
    DistrictSerializer, MunicipalitySerializer, SuggestedUseSerializer, \
    ServiceSerializer, OpenSpaceSerializer, \
    ReportSerializer, AvailableFacilitySerializer, \
    GallerySerializer, OpenSpaceAttributeSerializer, ServiceListSerializer, AllOpenSpaceSerializer
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
import datetime


class SliderViewSet(viewsets.ModelViewSet):
    serializer_class = SliderSerializer
    queryset = Slider.objects.all()
    permission_classes = []


class CreateOpenSpaceViewSet(viewsets.ModelViewSet):
    serializer_class = CreateOpenSpaceSerializer
    queryset = CreateOpenSpace.objects.all()
    permission_classes = []


class CreateNewOpenSpaceViewSet(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        data = []
        querysets = CreateOpenSpace.objects.all()

        for queryset in querysets:
            queries = queryset.create_open.all()
            i = []

            for query in queries:
                i.append({
                    'title': query.title,
                    'title_nep': query.title_nep
                })

            data.append({
                'id': queryset.id,
                'title': queryset.title,
                'title_nep': queryset.title_nep,
                'image': queryset.image.url,
                'points': i
            })

        return Response({'data': data})


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
    queryset = SuggestedUseData.objects.all()
    permission_classes = []

    def filter_queryset(self, queryset):
        open_space_id = self.request.query_params.get('id')
        return queryset.filter(open_space=open_space_id)


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = ServiceData.objects.all()
    permission_classes = []


class ServiceListViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceListSerializer
    queryset = ServiceList.objects.all()
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

    # def perform_create(self, serializer):
    #     if self.ward:
    #         serializer.save(address=self.municipality.name + '-' + self.ward + ',' + self.district.name)
    #     else:
    #         serializer.save(address=self.municipality.name + ',' + self.district.name)


class GalleryViewSet(viewsets.ModelViewSet):
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()
    permission_classes = []

    def filter_queryset(self, queryset):
        img_type = self.request.query_params.get('type')
        open_space = self.request.query_params.get('id')

        if img_type == 'map' and open_space:
            return Gallery.objects.filter(type='map', open_space=open_space)

        elif img_type == 'image' and open_space:
            return Gallery.objects.filter(type='image', open_space=open_space)

        elif img_type == 'map':
            print('def')
            return Gallery.objects.filter(type='map')

        elif img_type == 'image':
            print('def')
            return Gallery.objects.filter(type='image')

        elif open_space:
            print('def')
            return Gallery.objects.filter(open_space=open_space)

        else:
            return queryset


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = []

    def filter_queryset(self, queryset):
        status = self.request.query_params.get('status')
        open_space = self.request.query_params.get('id')
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')
        token = self.request.query_params.get('token')

        if start_date_str and end_date_str and status and open_space:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
            return queryset.filter(date__range=[start_date, end_date], status=status, open_space=open_space)

        elif start_date_str and end_date_str and open_space:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
            return queryset.filter(date__range=[start_date, end_date], open_space=open_space)

        elif start_date_str and end_date_str and status:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
            return queryset.filter(date__range=[start_date, end_date], status=status)

        elif start_date_str and end_date_str:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
            return queryset.filter(date__range=[start_date, end_date])

        elif status and open_space:
            return queryset.filter(status=status, open_space=open_space)

        elif status:
            return queryset.filter(status=status)

        elif open_space:
            return queryset.filter(open_space=open_space)

        elif token:
            return queryset.filter(token=token)

        else:
            return queryset


class OpenSpaceLandingApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = []
        open_spaces = OpenSpace.objects.all()
        for open_space in open_spaces:
            polygons = open_space.polygons

            if polygons and open_space.image and open_space.thumbnail:
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
                        "centroid": [open_space.polygons.centroid.x, open_space.polygons.centroid.y],
                        "thumbnail": open_space.thumbnail.url
                    }
                )

            if polygons and open_space.image and not open_space.thumbnail:
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
                        "centroid": [open_space.polygons.centroid.x, open_space.polygons.centroid.y],
                        "thumbnail": None
                    }
                )

            elif polygons and not open_space.image:
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
                        "centroid": [open_space.polygons.centroid.x, open_space.polygons.centroid.y],
                        "thumbnail": None
                    }
                )

            elif open_space.image and open_space.thumbnail and not open_space.polygons:
                data.append(
                    {
                        "id": open_space.id,
                        "title": open_space.title,
                        "province": open_space.province.id,
                        "district": open_space.district.id,
                        "municipality": open_space.municipality.id,
                        "address": open_space.address,
                        "image": open_space.image.url,
                        "latitude": None,
                        "longitude": None,
                        "centroid": None,
                        "thumbnail": open_space.thumbnail.url
                    }
                )

            elif open_space.image and not open_space.thumbnail and not open_space.polygons:
                data.append(
                    {
                        "id": open_space.id,
                        "title": open_space.title,
                        "province": open_space.province.id,
                        "district": open_space.district.id,
                        "municipality": open_space.municipality.id,
                        "address": open_space.address,
                        "image": open_space.image.url,
                        "latitude": None,
                        "longitude": None,
                        "centroid": None,
                        "thumbnail": None
                    }
                )

            elif not open_space.image and not open_space.polygons:
                data.append(
                    {
                        "id": open_space.id,
                        "title": open_space.title,
                        "province": open_space.province.id,
                        "district": open_space.district.id,
                        "municipality": open_space.municipality.id,
                        "address": open_space.address,
                        "image": None,
                        "latitude": None,
                        "longitude": None,
                        "centroid": None,
                        "thumbnail": None
                    }
                )
            elif open_space is None:
                data.append(
                    {
                        "id": None,
                        "title": None,
                        "province": None,
                        "district": None,
                        "municipality": None,
                        "address": None,
                        "image": None,
                        "latitude": None,
                        "longitude": None,
                        "centroid": None,
                        "thumbnail": None
                    }
                )
            else:
                pass
            # else:
            #     print('defff')
            #     data.append(
            #         {
            #             "id": open_space.id,
            #             "title": open_space.title,
            #             "province": open_space.province.id,
            #             "district": open_space.district.id,
            #             "municipality": open_space.municipality.id,
            #             "address": open_space.address,
            #             "image": None,
            #             "latitude": open_space.polygons.centroid.y,
            #             "longitude": open_space.polygons.centroid.x,
            #             "centroid": [open_space.polygons.centroid.x, open_space.polygons.centroid.y]
            #         }
            #     )

        return Response({"data": data})


class AddedOpenAPi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = []
        id = self.request.query_params.get('id')
        open_spaces = OpenSpace.objects.all()
        if id:
            open_space = OpenSpace.objects.get(id=id)

            data.append(
                {
                    "id": open_space.id,
                    "centroid": [open_space.polygons.centroid.x, open_space.polygons.centroid.y]
                }
            )
        else:
            for open_space in open_spaces:
                data.append(
                    {
                        "id": open_space.id,
                        "centroid": [open_space.polygons.centroid.x, open_space.polygons.centroid.y]
                    }
                )

        return Response({"data": data})


class DistrictApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = []
        id = self.request.query_params.get('province_id')

        districts = District.objects.all()

        if id:
            districts = districts.filter(province=id)

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
        id = self.request.query_params.get('district_id')
        municipalities = Municipality.objects.all()

        if id:
            municipalities = municipalities.filter(district=id)

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


# class DistanceApi(APIView):
#     authentication_classes = []
#     permission_classes = []
#
#     def get(self, request):
#         data = []
#         open_id = self.request.query_params.get('open_id')
#         open_space = OpenSpace.objects.get(id=open_id)
#         facility_id = self.request.query_params.get('facility_id')
#         facility = AvailableFacility.objects.get(id=facility_id)
#
#         open_point = open_space.centroid
#         print(open_point)
#
#         # data.append(
#         #     {
#         #         "id": province.id,
#         #         "name": province.name
#         #     }
#         # )
#
#         return Response({"data": data})


class GlimpseOfOpenSpace(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        district_list = []
        municipality_list = []
        open_count = []
        municipality_format = []
        open_space_c = OpenSpace.objects.all().count()
        district = OpenSpace.objects.values('district').distinct().count()
        municipality = OpenSpace.objects.values(
            'municipality').distinct().count()
        total_area = OpenSpace.objects.aggregate(
            Sum('total_area')).get('total_area__sum')
        total_capacity = OpenSpace.objects.aggregate(
            Sum('capacity')).get('capacity__sum')

        districts = OpenSpace.objects.values('district__name').order_by('district__name').distinct()
        count = districts.count()

        for i in range(0, count):
            district_list.append(districts[i]['district__name'])

        print(district_list)

        municipalities = OpenSpace.objects.values('municipality__name', 'municipality__hlcit_code').order_by('municipality__name').distinct()

        for i in range(0, municipality):
            municipality_list.append({municipalities[i]['municipality__name']:
                                      municipalities[i]['municipality__hlcit_code']})

            municipality_format.append({
                'name': municipalities[i]['municipality__name'],
                'hlcit_code': municipalities[i]['municipality__hlcit_code']
            })

        for municipality in municipalities:
            open_space = OpenSpace.objects.filter(municipality__hlcit_code=municipality['municipality__hlcit_code']).count()
            open_count.append({municipality['municipality__name']: open_space})

        data = {
            "open_space": open_space_c,
            "district": district,
            'district_list': district_list,
            "municipality": municipality,
            "municipality_list": municipality_list,
            "municipality_format": municipality_format,
            "total_area": total_area,
            "total_capacity": total_capacity,
            "open_count": open_count
        }

        return Response({"data": data})


class OpenSpaceGeojsonViewSet(APIView):
    permission_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        municipality_id = self.request.query_params.get('municipality_id', None)
        queryset = OpenSpace.objects.all()
        if municipality_id:
            queryset = queryset.filter(municipality_id=municipality_id)

        serializers = serialize('geojson', queryset,
                                geometry_field='polygons',
                                fields=('pk', 'title', 'description', 'status',
                                        'catchment_area', 'ownership',
                                        'elevation', 'access_to_site',
                                        'special_feature', 'address',
                                        'province', 'district',
                                        'municipality', 'ward', 'capacity',
                                        'total_area', 'usable_area', 'image',
                                        'maps', 'location', 'centroid', 'latitude', 'geoserver_url',
                                        'layername', 'workspace'))

        OpenSpaceGeoJson = json.loads(serializers)
        return Response(OpenSpaceGeoJson)


class SingleOpenSpaceGeojsonViewSet(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        open_id = self.request.query_params.get('id')
        mun_id = self.request.query_params.get('mun')
        if open_id == None:
            serializers = serialize('geojson',
                                    OpenSpace.objects.filter(municipality=mun_id),
                                    geometry_field='polygons',
                                    fields=('pk', 'title', 'description', 'status',
                                            'catchment_area', 'ownership',
                                            'elevation', 'access_to_site',
                                            'special_feature', 'address',
                                            'province', 'district',
                                            'municipality', 'ward', 'capacity',
                                            'total_area', 'usable_area', 'image',
                                            'maps', 'location', 'geoserver_url',
                                            'layername', 'workspace'))


        else:
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
                                            'maps', 'location', 'geoserver_url', 'layername', 'workspace'))

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
                                .filter(location__distance_lte=(openspace_location, D(km=distance)), available_type__title=type) \
                                .annotate(distance=Distance('location', openspace_location)) \
                                .order_by('distance')[0:count]
        print(resource_queryset)
        resource_json = AvailableFacilitySerializer(resource_queryset, many=True, context={'request': request})
        json = JSONRenderer().render(resource_json.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        api_json['facility'] = data

        return Response(api_json)


class AlternativeNearByMeViewSet(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        api_json = {}
        open_space_id = self.request.query_params.get('id')
        distance = self.request.query_params.get('distance')
        print(open_space_id)
        open_space = OpenSpace.objects.get(id=open_space_id)
        longitude = open_space.centroid[0]
        latitude = open_space.centroid[1]
        openspace_location = GEOSGeometry('POINT({} {})'.format(longitude, latitude), srid=4326)
        resource_queryset = AvailableFacility.objects \
            .filter(location__distance_lte=(openspace_location, D(km=distance))) \
            .annotate(distance=Distance('location', openspace_location)) \
            .order_by('distance')
        print(resource_queryset)
        resource_json = AvailableFacilitySerializer(resource_queryset, many=True, context={'request': request})
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
        resource_json = OpenSpaceAttributeSerializer(resource_queryset, many=True)
        json = JSONRenderer().render(resource_json.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        api_json['open_space'] = data
        return Response(api_json)


class OpenSpaceNearBy(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        api_json = {}
        latitude = self.request.data.get('latitude')
        longitude = self.request.data.get('longitude')
        distance = self.request.data.get('distance')

        if latitude and longitude:
            location = GEOSGeometry('POINT({} {})'.format(longitude, latitude), srid=4326)

        open_space = OpenSpace.objects \
            .filter(polygons__distance_lte=(location, D(km=distance))) \
            .annotate(distance=Distance('polygons', location)) \
            .order_by('distance')

        resource_json = OpenSpaceAttributeSerializer(open_space, many=True)
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


class OpenSpacePagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'


class OpenSpaceView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AllOpenSpaceSerializer
    queryset = OpenSpace.objects.all().prefetch_related('suggested_use', 'suggested_use__suggested_use',
                                                        'services', 'services__service', 'question_data',
                                                        'question_data__question', 'municipality')
    pagination_class = OpenSpacePagination
    renderer_classes = [JSONRenderer]

    def filter_queryset(self, queryset):
        municipality_id = self.request.query_params.get('municipality_id', None)
        if municipality_id:
            queryset = queryset.filter(municipality_id=municipality_id)
        return queryset




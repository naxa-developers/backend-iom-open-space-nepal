from core.models import Slider, CreateOpenSpace, Resource, Province, District, \
    Municipality, SuggestedUseData, ServiceList, OpenSpace, Report, QuestionsData, AvailableFacility, Gallery, \
    SuggestedUseList, ServiceData
from rest_framework import serializers
from datetime import date, datetime
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from dashboard.models import AgencyMessage


class AgencyMessageSerializer(serializers.ModelSerializer):
    agency_name = serializers.CharField(source='agency.agency_name')
    municipality_name = serializers.CharField(source='municipality.name')
    openspace_title = serializers.CharField(source='open_space.title')

    class Meta:
        model = AgencyMessage
        fields = ('agency', 'municipality', 'open_space', 'message',
                  'agency_name', 'municipality_name', 'openspace_title')


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


class CreateOpenSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateOpenSpace
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'


class SuggestedUseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedUseList
        fields = '__all__'


class SuggestedUseSerializer(serializers.ModelSerializer):
    suggested_use = SuggestedUseListSerializer()

    class Meta:
        model = SuggestedUseData
        fields = ('id', 'open_space', 'suggested_use',)


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceList
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    service = ServiceListSerializer()

    class Meta:
        model = ServiceData
        fields = ('description', 'open_space', 'service')


class QuestionDataSerializer(serializers.ModelSerializer):
    que = serializers.SerializerMethodField()

    class Meta:
        model = QuestionsData
        fields = ('question', 'ans', 'open_space', 'que')

    def get_que(self, instance):
        que = instance.question.title
        return que


class AvailableFacilitySerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    # distance = serializers.SerializerMethodField()
    type = serializers.CharField(source='available_type.title')
    # sub_type = serializers.CharField(source='available_sub_type.title')
    sub_type = serializers.SerializerMethodField()

    class Meta:
        model = AvailableFacility
        fields = ('id', 'name', 'type', 'available_type', 'available_sub_type', 'operator_type', 'address', 'location',
                  'province', 'district','sub_type', 'municipality', 'email', 'opening_hours',
                  'bank_type', 'phone_number', 'comments', 'website',
                  'bank_network', 'icon', 'latitude', 'longitude')

    def get_latitude(self, instance):
        return instance.location.y

    def get_longitude(self, instance):
        return instance.location.x

    def get_sub_type(self,instance):
        if instance.available_sub_type is not None:
            return instance.available_sub_type.title
        else:
            return None


    # def get_distance(self, instance):
    #     open_space_id = self.context['request'].query_params.get('id')
    #     open_space = OpenSpace.objects.get(id=open_space_id)
    #     centroid = open_space.centroid
    #     open_point = Point(centroid[0], centroid[1], srid=4326)
    #     distance = open_point.distance(instance.location)
    #     d = (distance/111)*1000
    #
    #     return d


class GallerySerializer(serializers.ModelSerializer):
    open_name = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ['image', 'type', 'open_space', 'thumbnail', 'open_name']

    def get_open_name(self, instance):
        return instance.open_space.title


class OpenSpaceSerializer(serializers.ModelSerializer):
    suggested_use = SuggestedUseSerializer(many=True, required=False)
    services = ServiceSerializer(many=True, required=False)
    question_data = QuestionDataSerializer(many=True, required=False)
    municipality_name = serializers.ReadOnlyField(source='municipality.name')
    province_name = serializers.ReadOnlyField(source='province.name')
    district_name = serializers.ReadOnlyField(source='district.name')

    # centroid = serializers.SerializerMethodField()

    class Meta:
        model = OpenSpace
        fields = ('id', 'suggested_use', 'question_data', 'services', 'title',
                  'current_land_use', 'ownership', 'elevation', 'district',
                  'access_to_site', 'special_feature', 'address', 'province',
                  'municipality', 'ward', 'capacity', 'total_area',
                  'usable_area', 'image', 'description', 'centroid', 'municipality_name',
                  'province_name', 'district_name', 'thumbnail', 'geoserver_url', 'layername', 'workspace')

    # def get_centroid(self, obj):
    #     center = []
    #     long=obj.polygons.centroid.x
    #     lat=obj.polygons.centroid.y
    #     center.append(long)
    #     center.append(lat)
    #     return center


class OpenSpaceAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenSpace
        fields = ('id', 'title', 'current_land_use', 'ownership', 'elevation',
                  'access_to_site', 'special_feature', 'address', 'province',
                  'municipality', 'ward', 'capacity', 'total_area', 'district',
                  'usable_area', 'image', 'description', 'centroid', )


class ReportSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    # date = serializers.DateTimeField("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Report
        fields = ('id', 'title', 'name', 'message', 'date', 'urgency',
                  'status', 'open_space', 'reported_by', 'image', 'location', 'token', 'count', 'address', 'reply')

    def get_location(self, instance):
        center = []
        long = instance.open_space.polygons.centroid.x
        lat = instance.open_space.polygons.centroid.y
        center.append(long)
        center.append(lat)
        return center

    def get_count(self, instance):
        date1 = instance.date
        date2 = datetime.now().date()
        delta = date2 - date1
        return delta.days

    def get_address(self, instance):
        return instance.open_space.address



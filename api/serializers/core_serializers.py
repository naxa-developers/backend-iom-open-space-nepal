from core.models import Slider, CreateOpenSpace, Resource, Province, District, \
    Municipality, SuggestedUseData, Services, OpenSpace, Report, QuestionsData, AvailableFacility, Gallery
from rest_framework import serializers
from datetime import date, datetime


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


class SuggestedUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedUseData
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'


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

    class Meta:
        model = AvailableFacility
        fields = ('id', 'name', 'type', 'operator_type', 'address', 'location',
                  'province', 'district', 'municipality', 'email', 'opening_hours',
                  'education_type', 'financial_type', 'bank_type', 'health_type',
                  'phone_number', 'comments', 'website', 'bank_network', 'icon',
                  'latitude', 'longitude')

        def get_latitude(self, instance):
            return instance.location.y

        def get_longitude(self, instance):
            return instance.location.x


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class OpenSpaceSerializer(serializers.ModelSerializer):
    suggested_use = SuggestedUseSerializer(many=True, required=False)
    services = ServiceSerializer(many=True, required=False)
    question_data = QuestionDataSerializer(many=True, required=False)

    # centroid = serializers.SerializerMethodField()

    class Meta:
        model = OpenSpace
        fields = ('id', 'suggested_use', 'question_data', 'services', 'title',
                  'current_land_use', 'ownership', 'elevation', 'district',
                  'access_to_site', 'special_feature', 'address', 'province',
                  'municipality', 'ward', 'capacity', 'total_area',
                  'usable_area', 'image', 'description', 'centroid', )

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

    class Meta:
        model = Report
        fields = ('id', 'title', 'name', 'message', 'date', 'urgency',
                  'status', 'open_space', 'reported_by', 'image', 'location', 'count', 'address')

    def get_location(self, instance):
        center = []
        long = instance.open_space.polygons.centroid.x
        lat = instance.open_space.polygons.centroid.y
        center.append(long)
        center.append(lat)
        return center

    def get_count(self, instance):
        date1 = instance.date.date()
        date2 = datetime.now().date()
        delta = date2 - date1
        return delta.days

    def get_address(self, instance):
        return instance.open_space.address



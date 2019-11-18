from core.models import Slider, CreateOpenSpace, Resource, Province, District,\
    Municipality, SuggestedUse, Services, OpenSpace, Report, QuestionsData
from rest_framework import serializers


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
        model = SuggestedUse
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'


class QuestionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionsData
        fields = '__all__'


# class FacilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Facility
#         fields = '__all__'


class OpenSpaceSerializer(serializers.ModelSerializer):
    suggested_use = SuggestedUseSerializer(many=True, required=False)
    services = ServiceSerializer(many=True, required=False)
    question_data = QuestionDataSerializer(many=True, required=False)
    centroid = serializers.SerializerMethodField()

    class Meta:
        model = OpenSpace
        fields = ('id', 'suggested_use', 'question_data', 'services', 'title',
                  'current_land_use', 'ownership', 'elevation',
                  'access_to_site', 'special_feature', 'address', 'province',
                  'municipality', 'ward', 'capacity', 'total_area',
                  'usable_area', 'image', 'maps', 'description', 'centroid')

    def get_centroid(self, obj):
        return obj.polygons.centroid


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'



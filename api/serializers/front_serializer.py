from front.models import OpenSpaceDef, OpenSpaceIde, Header, Contact,\
    OpenSpaceApp, AboutHeader, CriteriaDescription, CriteriaType, OpenSpaceCriteria, WhyMapOpenIcon, WhyMapOpenSpace
from rest_framework import serializers


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = '__all__'


class OpenSpaceDefSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenSpaceDef
        fields = '__all__'


class OpenSpaceIdeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenSpaceIde
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class OpenSpaceAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenSpaceApp
        fields = '__all__'


class AboutHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutHeader
        fields = '__all__'


class CriteriaDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriteriaDescription
        fields = '__all__'


class CriteriaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriteriaType
        fields = '__all__'


class OpenSpaceCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenSpaceCriteria
        fields = '__all__'


class WhyMapOpenIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyMapOpenIcon
        fields = '__all__'


class WhyMapOpenSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyMapOpenSpace
        fields = '__all__'





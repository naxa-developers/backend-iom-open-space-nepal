from front.models import OpenSpaceDef, OpenSpaceIde, Header
from rest_framework import serializers


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        field = '__all__'


class OpenSpaceDefSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenSpaceDef
        field = '__all__'


class OpenSpaceIdeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenSpaceIde
        field = '__all__'


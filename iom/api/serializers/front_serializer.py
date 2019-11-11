from front.models import OpenSpaceDef, OpenSpaceIde, Header, Contact,\
    OpenSpaceApp
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

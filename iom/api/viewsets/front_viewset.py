from rest_framework import viewsets
from front.models import OpenSpaceDef, OpenSpaceIde, Header
from api.serializers.front_serializer import OpenSpaceDefSerializer,\
    OpenSpaceIdeSerializer, HeaderSerializer


class HeaderViewSet(viewsets.ModelViewSet):
    serializer_class = HeaderSerializer
    queryset = Header.objects.all()
    permission_classes = []


class OpenSpaceIdeViewSet(viewsets.ModelViewSet):
    serializer_class = OpenSpaceIdeSerializer
    queryset = OpenSpaceIde.objects.all()
    permission_classes = []


class OpenSpaceDefViewSet(viewsets.ModelViewSet):
    serializer_class = OpenSpaceDefSerializer
    queryset = OpenSpaceDef.objects.all()
    permission_classes = []



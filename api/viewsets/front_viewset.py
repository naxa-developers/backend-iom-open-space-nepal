from rest_framework import viewsets
from front.models import OpenSpaceDef, OpenSpaceIde, Header, Contact,\
    OpenSpaceApp
from api.serializers.front_serializer import OpenSpaceDefSerializer,\
    OpenSpaceIdeSerializer, HeaderSerializer, ContactSerializer,\
    OpenSpaceAppSerializer

from api.serializers.core_serializers import AgencyMessageSerializer
from dashboard.models import AgencyMessage


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


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    permission_classes = []


class OpenSpaceAppViewSet(viewsets.ModelViewSet):
    serializer_class = OpenSpaceAppSerializer
    queryset = OpenSpaceApp.objects.all()
    permission_classes = []


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = AgencyMessageSerializer
    queryset = AgencyMessage.objects.all()
    permission_classes = []




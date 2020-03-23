from rest_framework import viewsets
from front.models import OpenSpaceDef, OpenSpaceIde, Header, Contact,\
    OpenSpaceApp, AboutHeader, CriteriaDescription, CriteriaType, OpenSpaceCriteria, WhyMapOpenIcon, WhyMapOpenSpace
from api.serializers.front_serializer import OpenSpaceDefSerializer,\
    OpenSpaceIdeSerializer, HeaderSerializer, ContactSerializer,\
    OpenSpaceAppSerializer, AboutHeaderSerializer, CriteriaDescriptionSerializer, CriteriaTypeSerializer, \
    OpenSpaceCriteriaSerializer, WhyMapOpenSpaceSerializer, WhyMapOpenIconSerializer

from api.serializers.core_serializers import AgencyMessageSerializer
from dashboard.models import AgencyMessage
from rest_framework.views import APIView
from rest_framework.response import Response


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


#About page viewsets

class AboutHeaderViewSet(viewsets.ModelViewSet):
    serializer_class = AboutHeaderSerializer
    queryset = AboutHeader.objects.all()
    permission_classes = []


class CriteriaDescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = CriteriaDescriptionSerializer
    queryset = CriteriaDescription.objects.all()
    permission_classes = []


class CriteriaTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CriteriaTypeSerializer
    queryset = CriteriaType.objects.all()
    permission_classes = []


class OpenSpaceCriteriaViewSet(viewsets.ModelViewSet):
    serializer_class = OpenSpaceCriteriaSerializer
    queryset = OpenSpaceCriteria.objects.all()
    permission_classes = []


class WhyMapOpenIconViewSet(viewsets.ModelViewSet):
    serializer_class = WhyMapOpenIconSerializer
    queryset = WhyMapOpenIcon.objects.all()
    permission_classes = []


class WhyMapOpenSpaceViewSet(viewsets.ModelViewSet):
    serializer_class = WhyMapOpenSpaceSerializer
    queryset = WhyMapOpenSpace.objects.all()
    permission_classes = []


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = AgencyMessageSerializer
    queryset = AgencyMessage.objects.all()
    permission_classes = []

    def filter_queryset(self, queryset):
        open_space_id = self.request.query_params.get('id', None)
        # municipality_hlcit = self.request.query_params.get('hlcit_code', None)
        if open_space_id:
            return queryset.filter(open_space__id=open_space_id)

        # elif municipality_hlcit:
        #     return queryset.filter()
        else:
            return queryset


# class FireBaseNotificationViewSet(APIView):


class UniqueMunicipalityOfMessage(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        data = []
        municipality_name = AgencyMessage.objects.values('municipality__name').order_by('municipality__name') \
            .distinct()

        for municipality in municipality_name:
            data.append(municipality['municipality__name'])

        return Response({'data': data})













from django.conf import settings
from django.contrib.gis.geos import Point
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.models import OpenSpace, AvailableFacility, Report, QuestionList, QuestionsData, ServiceData, ServiceList, \
    SuggestedUseList, SuggestedUseData, Resource, ResourceCategory, ResourceDocumentType, Province, District, \
    Municipality, Slider, CreateOpenSpace, Gallery, AvailableType, CreateOpenSpacePoints
from .models import UserProfile, UserAgency, AgencyMessage
import json
import random
import pandas as pd
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from .forms import OpenSpaceForm, AvailableFacilityForm, QuestionForm, QuestionDataForm, SuggestedForm, \
    SuggestedDataForm, ServiceForm, ServiceDataForm, ResourceCategoryForm, HeaderForm, SliderForm, OpenSpaceDefForm, \
    OpenSpaceIdeForm, OpenSpaceAppForm, ContactForm, CreateOpenSpaceForm, GalleryForm, ImportShapefileForm, \
    ResourceDocumentTypeForm, ResourceForm, AvailableTypeForm, AgencyMessageForm, UploadNewOpenSpaceForm, \
    WhyMapOpenSpaceForm, WhyMapOpenSpaceIconForm, AboutHeaderForm, OpenSpaceCriteriaForm, CriteriaDescriptionForm, \
    CriteriaTypeForm, CreateOpenSpacePointsForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission
from front.models import Header, OpenSpaceDef, OpenSpaceIde, OpenSpaceApp, Contact, WhyMapOpenSpace, WhyMapOpenIcon, \
    AboutHeader, OpenSpaceCriteria, CriteriaType, CriteriaDescription
from django.apps import apps
from django.contrib import messages
import base64
import os
from django.contrib.gis.utils import LayerMapping
from django.shortcuts import render_to_response
from dashboard import shapefileIO
from django.contrib.gis.gdal import DataSource
from fcm_django.models import FCMDevice
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .upload_functions import upload_eia, upload_amenities, upload_openspace


# Create your views here.
class HomePage(TemplateView):

    def get(self, request, *args, **kwargs):
        # category = ProductCategory.objects.order_by('id')
        # product = Product.objects.order_by('id')
        user = self.request.user

        try:
            if user.agency:
                return redirect('agency_message')

        except ObjectDoesNotExist:
            user_data = UserProfile.objects.get(user=user)
            print(user.groups.all())
            group = Group.objects.get(user=user)
            data_list1 = []
            data_list2 = []
            if group.name == 'admin':
                open_space_total = list(
                    OpenSpace.objects.filter(municipality__id=user_data.municipality.id).values_list('total_area',
                                                                                                     flat=True))
                open_space_usable = list(
                    OpenSpace.objects.filter(municipality__id=user_data.municipality.id).values_list('usable_area',
                                                                                                     flat=True))
                open_space_name = list(
                    OpenSpace.objects.filter(municipality__id=user_data.municipality.id).values_list('title', flat=True))
                mun_id = user_data.municipality.id
            else:
                open_space_total = list(OpenSpace.objects.values_list('total_area', flat=True))
                open_space_usable = list(
                    OpenSpace.objects.values_list('usable_area', flat=True))
                open_space_name = list(OpenSpace.objects.values_list('title', flat=True))

                mun_id = 0

            service_list = ServiceList.objects.order_by('id')

            columns = []
            columns_dict = {}
            color_dict = {}

            for l in service_list:
                if group.name == 'admin':
                    count = ServiceData.objects.filter(open_space__municipality=user_data.municipality.id,
                                                       service__id=l.id).count()
                else:
                    count = ServiceData.objects.filter(service__id=l.id).count()

                columns_dict.update({'data' + str(l.id): l.name})
                service = ['data' + str(l.id), count]
                columns.append(service)
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                rgb = 'rgb' + str((r, g, b))
                color_dict.update({'data' + str(l.id): rgb})

            open_spaces = json.dumps(open_space_name)
            data_list1.extend(open_space_total)
            data_list2.extend(open_space_usable)
            data_listt2 = [float(i) for i in data_list2]
            report = Report.objects.all()
            # print(service_open)
            pen_count = Report.objects.filter(status='pending').count()
            com_count = Report.objects.filter(status='replied').count()
            return render(request, 'dashboard.html',
                          {'data_list1': data_list1, 'data_list2': data_listt2, 'open_space_name': open_spaces,
                           'pie_count': columns, 'pie_name': columns_dict, 'pie_color': color_dict, 'group': group.name,
                           'mun_id': mun_id, 'user': user_data, 'pending': pen_count, 'completed': com_count, 'report': report})


def UploadShapeFile(request):
    if "GET" == request.method:
        return render(request, 'upload_shapefile.html')
    else:
        print(request.FILES.getlist("shapefile")[0])
        shp_file = request.FILES.getlist("shapefile")
        file = open(shp_file)
        os.path.realpath(file.name)
        ds = DataSource(shp_file)

        return HttpResponse('a')


def importShapefile(request):
    """ Let the user import a new shapefile.
    """
    if request.method == "GET":
        form = ImportShapefileForm()
        return render(request, "upload_shapefile.html", {'form': form, 'errMsg': None})

    elif request.method == "POST":
        errMsg = None  # initially.

        form = ImportShapefileForm(request.POST, request.FILES)
        if form.is_valid():
            shapefile = request.FILES['import_file']
            encoding = request.POST['character_encoding']
            errMsg = shapefileIO.importData(shapefile, encoding)
            print(errMsg)
            if errMsg == None:
                return HttpResponseRedirect("/dashboard/openspace-list")

        return render(request, "upload_shapefile.html", {'form': form, 'errMsg': errMsg})


def uploadOpenSpaceFile(request):

    municipality = Municipality.objects.all()
    province = Province.objects.all()
    district = District.objects.all()

    if request.method == "GET":
        form = UploadNewOpenSpaceForm()
        return render(request, "upload_open_space.html", {'form': form, 'provinces': province, 'districts':district, 'municipalities': municipality })

    elif request.method == "POST":
        form = UploadNewOpenSpaceForm(request.POST, request.FILES)
        if form.is_valid():
            open_space = request.FILES['open_space']
            eia_table = request.FILES['eia_table']
            nearby_amenities = request.FILES['nearby_amenities']

            upload_openspace(open_space)
            upload_openspace(eia_table)
            upload_openspace(nearby_amenities)

        return render(request, "upload_open_space.html", {'form': form, 'provinces': province, 'districts':district, 'municipalities': municipality})


class OpenSpaceList(LoginRequiredMixin, ListView):
    template_name = 'openspace_list.html'
    model = OpenSpace

    def get_context_data(self, **kwargs):
        data = super(OpenSpaceList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        print(user_data)
        url = 'openspace-list/'+self.kwargs['hlcit_code']
        if group.name == "admin":
            query_data = OpenSpace.objects.filter(municipality__id=user_data.municipality.id).select_related('province',
                                                                                                             'district',
                                                                                                             'municipality').order_by(
                'id')

        elif group.name == 'municipality_admin':
            query_data = OpenSpace.objects.filter(municipality__hlcit_code=user_data.municipality.hlcit_code).select_related('province', 'district', 'municipality').order_by('id')
            url = 'openspace-list/' + user_data.municipality.hlcit_code
            print(query_data)

        else:
            query_data = OpenSpace.objects.filter(municipality__hlcit_code=self.kwargs['hlcit_code']).select_related('province', 'district', 'municipality').order_by('id')

        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['list'] = query_data
        data['model'] = 'OpenSpace'
        # data['code'] = user_data.municipality.hlcit_code
        data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'openspace'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


# class OpenSpaceListMunicipality(LoginRequiredMixin, ListView):
#     template_name = 'openspace_municipality_list.html'
#     model = OpenSpace
#
#     def get_context_data(self, **kwargs):
#         data = super(OpenSpaceList, self).get_context_data(**kwargs)
#         user = self.request.user
#         user_data = UserProfile.objects.get(user=user)
#         que


class UserList(LoginRequiredMixin, ListView):
    template_name = 'user_list.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        data = super(UserList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        query_data = UserProfile.objects.all()
        print('test', self.request.user)
        data['list'] = query_data
        data['user'] = user_data
        data['active'] = 'user'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class AgencyList(LoginRequiredMixin, ListView):
    template_name = 'agency_list.html'
    model = UserAgency

    def get_context_data(self, **kwargs):
        data = super(AgencyList, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        query_data = UserAgency.objects.all()
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'user'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


def activate_user(request, **kwargs):
    user = User.objects.get(id=kwargs['id'])
    # user_data = UserProfile.objects.get(user=user)

    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()
    return redirect('user-list')


def publish_report(request, **kwargs):
    report = Report.objects.get(id=kwargs['pk'])

    if report.is_published:
        report.is_published = False
    else:
        report.is_published = True

    report.save()
    return redirect('report-list')


def activate_agency(request, **kwargs):
    user = User.objects.get(id=kwargs['id'])

    print(user)

    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()
    return redirect('agency_list')


class AvailableFacilityList(LoginRequiredMixin, ListView):
    template_name = 'available_list.html'
    model = AvailableFacility

    def get_context_data(self, **kwargs):
        data = super(AvailableFacilityList, self).get_context_data(**kwargs)
        query_data = AvailableFacility.objects.select_related('province', 'district', 'municipality').order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['model'] = 'AvailableFacility'
        data['url'] = 'available-list'
        data['user'] = user_data
        data['active'] = 'available'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class ReportList(LoginRequiredMixin, ListView):
    template_name = 'reports_list.html'
    model = Report

    def get_context_data(self, **kwargs):
        data = super(ReportList, self).get_context_data(**kwargs)
        query_data = Report.objects.select_related('open_space', ).order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)

        if group.name == 'municipality_admin':
            query_data = Report.objects.filter(open_space__municipality__hlcit_code=user_data.municipality.hlcit_code).select_related('open_space', ).order_by('id')

        else:
            query_data = Report.objects.select_related('open_space', ).order_by('id')

        open_space = OpenSpace.objects.all()

        url = 'report-list/'
        data['list'] = query_data
        data['open_spaces'] = open_space
        data['model'] = 'Report'
        # data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'available'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class QuestionsList(LoginRequiredMixin, ListView):
    template_name = 'question_list.html'
    model = QuestionList

    def get_context_data(self, **kwargs):
        data = super(QuestionsList, self).get_context_data(**kwargs)
        query_data = QuestionList.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'question-list/'
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['list'] = query_data
        data['model'] = 'QuestionList'
        data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'question'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class QuestionData(LoginRequiredMixin, ListView):
    template_name = 'questiondata_list.html'
    model = QuestionsData

    def get_context_data(self, **kwargs):
        data = super(QuestionData, self).get_context_data(**kwargs)
        query_data = QuestionsData.objects.filter(open_space=self.kwargs['id']).select_related('open_space',
                                                                                               'question', ).order_by(
            'id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        url = 'questiondata-list/' + str(self.kwargs['id'])
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['open_space_id'] = self.kwargs['id']
        data['list'] = query_data
        data['model'] = 'QuestionsData'
        data['url'] = base64_url
        # data['user'] = user_data
        data['active'] = 'question'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class SuggestedUseLists(LoginRequiredMixin, ListView):
    template_name = 'suggest_list.html'
    model = SuggestedUseList

    def get_context_data(self, **kwargs):
        data = super(SuggestedUseLists, self).get_context_data(**kwargs)
        query_data = SuggestedUseList.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'suggest-list/'
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['list'] = query_data
        data['model'] = 'SuggestedUseList'
        data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'available'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class SuggestedUseDataList(LoginRequiredMixin, ListView):
    template_name = 'suggestdata_list.html'
    model = SuggestedUseData

    def get_context_data(self, **kwargs):
        data = super(SuggestedUseDataList, self).get_context_data(**kwargs)
        query_data = SuggestedUseData.objects.filter(open_space=self.kwargs['id']).select_related(
            'open_space').order_by('id')

        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'suggestdata-list/' + str(self.kwargs['id'])
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['open_space_id'] = self.kwargs['id']
        data['list'] = query_data
        data['model'] = 'SuggestedUseData'
        data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'available'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class GalleryLists(LoginRequiredMixin, ListView):
    template_name = 'gallery_list.html'
    model = Gallery

    def get_context_data(self, **kwargs):
        data = super(GalleryLists, self).get_context_data(**kwargs)
        query_data = Gallery.objects.filter(open_space=self.kwargs['id']).order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'gallery-list/' + str(self.kwargs['id'])
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['open_space_id'] = self.kwargs['id']
        data['list'] = query_data
        data['model'] = 'Gallery'
        data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'gallery'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class ServiceLists(LoginRequiredMixin, ListView):
    template_name = 'service_list.html'
    model = ServiceList

    def get_context_data(self, **kwargs):
        data = super(ServiceLists, self).get_context_data(**kwargs)
        query_data = ServiceList.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'service-list/'
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['list'] = query_data
        data['model'] = 'ServiceList'
        data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'available'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class ServiceDataList(LoginRequiredMixin, ListView):
    template_name = 'servicedata_list.html'
    model = ServiceData

    def get_context_data(self, **kwargs):
        data = super(ServiceDataList, self).get_context_data(**kwargs)
        query_data = ServiceData.objects.filter(open_space=self.kwargs['id']).select_related('open_space',
                                                                                             'service', ).order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'servicedata-list/' + str(self.kwargs['id'])
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['open_space_id'] = self.kwargs['id']
        data['list'] = query_data
        data['model'] = 'ServiceData'
        data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'available'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class ResourceList(LoginRequiredMixin, ListView):
    template_name = 'resource_list.html'
    model = Resource

    def get_context_data(self, **kwargs):
        data = super(ResourceList, self).get_context_data(**kwargs)
        query_data = Resource.objects.select_related('category', 'document_type', ).order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'resource-list/'
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['model'] = 'Resource'
        data['url'] = base64_url
        data['list'] = query_data
        data['user'] = user_data
        data['active'] = 'resource'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class ResourceCategoryList(LoginRequiredMixin, ListView):
    template_name = 'resource_category_list.html'
    model = ResourceCategory

    def get_context_data(self, **kwargs):
        data = super(ResourceCategoryList, self).get_context_data(**kwargs)
        query_data = ResourceCategory.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'resource-category-list/'
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['list'] = query_data
        data['model'] = 'ResourceCategory'
        data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'resource'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class ResourceDocumentList(LoginRequiredMixin, ListView):
    template_name = 'resource_document_list.html'
    model = ResourceDocumentType

    def get_context_data(self, **kwargs):
        data = super(ResourceDocumentList, self).get_context_data(**kwargs)
        query_data = ResourceDocumentType.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'resource-document-list/'
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['model'] = 'ResourceDocumentType'
        data['url'] = base64_url
        data['list'] = query_data
        data['user'] = user_data
        data['active'] = 'resource'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class OpenSpaceCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = OpenSpace
    template_name = 'openspace_add.html'
    form_class = OpenSpaceForm
    success_message = 'Open successfully Created'

    def get_context_data(self, **kwargs):
        data = super(OpenSpaceCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['provinces'] = Province.objects.all().order_by('id')
        data['active'] = 'openspace'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('openspace-list')


class ResourceCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Resource
    template_name = 'resource_add.html'
    form_class = ResourceForm
    success_message = 'Resource successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ResourceCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['resource_cat'] = ResourceCategory.objects.all().order_by('id')
        data['resource_doc'] = ResourceDocumentType.objects.all().order_by('id')
        data['active'] = 'resource'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('resource-list')


class AddMunicipalityAvailableAmenities(LoginRequiredMixin, TemplateView):
    template_name = 'municipality_available_amenities_form.html'

    def get_context_data(self, **kwargs):
        data = super(AddMunicipalityAvailableAmenities, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'available'
        data['available_types'] = AvailableType.objects.all()
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count
        data["municipality"] = Municipality.objects.filter(hlcit_code=self.kwargs['hlcit_code']).\
            values('id', 'name', 'province_id', 'province__name').get()

        return data

    def post(self, request, **kwargs):
        my_data = request.POST
        uploaded_file = request.FILES['upload_csv']
        available_type = my_data['available_type']
        mun = Municipality.objects.get(hlcit_code=self.kwargs['hlcit_code'])
        district = mun.district
        province = mun.province
        df = pd.read_csv(uploaded_file).fillna('')
        upper_range = len(df)

        available_facilities_objs = []

        try:
            for row in range(0, upper_range):

                obj = AvailableFacility(
                    province=province,
                    district=district,
                    municipality=mun,
                    name=df['Name'][row],
                    ward_no=str(df['Ward No.'][row]),
                    phone_number=df['Contact'][row],
                    # address=df['Address'][row],
                    comments=df['Remarks'][row],
                    available_type_id=int(available_type),
                    # operator_type=df['operator_t'][row],
                    location=Point(float(df['Longitude'][row]), float(df['Latitude'][row])),
                )
                available_facilities_objs.append(obj)

            AvailableFacility.objects.bulk_create(available_facilities_objs)
        except Exception as e:
            return super(TemplateView, self).render_to_response(context={'error':
                                                                             'Please upload file with provided formats'})

        context = {}  # set your context
        # return reverse_lazy('available_ameni_list', kwargs={'title': available_type,
        #                                                     'hlcit_code': self.kwargs['hlcit_code']})
        available_type_obj = AvailableType.objects.get(id=available_type)
        return HttpResponseRedirect(reverse('available_ameni_list', args=(),
                                            kwargs={'title': available_type_obj.title,
                                                    'hlcit_code': self.kwargs['hlcit_code']}))
    #
    # def get_success_url(self):
    #     return reverse_lazy('available-list')


class AvailableFacilityCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = AvailableFacility
    template_name = 'available_facility_add.html'
    form_class = AvailableFacilityForm
    success_message = 'Available Facility successfully Created'

    def get_context_data(self, **kwargs):
        data = super(AvailableFacilityCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'available'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('available-list')


class QuestionCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = QuestionsList
    template_name = 'question_add.html'
    form_class = QuestionForm
    success_message = 'EIA successfully Created'

    def get_context_data(self, **kwargs):
        data = super(QuestionCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'question'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('question-list')


class ResourceUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Resource
    template_name = 'resource_edit.html'
    form_class = ResourceForm
    success_message = 'Resource Updated Created'

    def get_context_data(self, **kwargs):
        data = super(ResourceUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['resource_cat'] = ResourceCategory.objects.all().order_by('id')
        data['resource_doc'] = ResourceDocumentType.objects.all().order_by('id')
        data['active'] = 'resource'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('resource-list')


class OpenSpaceUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = OpenSpace
    template_name = 'openspace_edit.html'
    form_class = OpenSpaceForm
    success_message = 'Open successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(OpenSpaceUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['provinces'] = Province.objects.all().order_by('id')
        data['active'] = 'openspace'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('openspace-list')


class QuestionUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = QuestionList
    template_name = 'question_edit.html'
    form_class = QuestionForm
    success_message = 'Question successfully  updated'

    def get_context_data(self, **kwargs):
        data = super(QuestionUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'question'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('question-list')


class QuestionDataCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = QuestionsData
    template_name = 'questiondata_add.html'
    form_class = QuestionDataForm
    success_message = 'Question Data Facility successfully Created'

    def get_context_data(self, **kwargs):
        data = super(QuestionDataCreate, self).get_context_data(**kwargs)
        data['question'] = QuestionList.objects.order_by('id')
        data['open_space'] = OpenSpace.objects.filter(id=self.kwargs['id']).select_related('province', 'district',
                                                                                           'municipality').order_by(
            'id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'question'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/questiondata-list/' + str(self.kwargs['id'])


class QuestionDataUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = QuestionsData
    template_name = 'questiondata_edit.html'
    form_class = QuestionDataForm
    success_message = 'Question Data successfully  updated'

    def get_context_data(self, **kwargs):
        data = super(QuestionDataUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        data['question'] = QuestionList.objects.order_by('id')
        data['open_space'] = OpenSpace.objects.filter(id=self.kwargs['id']).select_related('province',
                                                                                           'district',
                                                                                           'municipality').order_by(
            'id')
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'question'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/questiondata-list/' + str(self.kwargs['id'])


class SuggestedCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = SuggestedUseList
    template_name = 'suggest_add.html'
    form_class = SuggestedForm
    success_message = 'Amenities successfully Created'

    def get_context_data(self, **kwargs):
        data = super(SuggestedCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'suggest'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('suggest-list')


class SuggestedUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SuggestedUseList
    template_name = 'suggest_edit.html'
    form_class = SuggestedForm
    success_message = 'Amenities successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(SuggestedUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'suggest'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('suggest-list')


class SuggestedDataCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = SuggestedUseData
    template_name = 'suggestdata_add.html'
    form_class = SuggestedDataForm
    success_message = 'Suggested Data successfully Created'

    def get_context_data(self, **kwargs):
        data = super(SuggestedDataCreate, self).get_context_data(**kwargs)
        data['open_space'] = OpenSpace.objects.filter(id=self.kwargs['id']).select_related('province',
                                                                                           'district',
                                                                                           'municipality').order_by(
            'id')
        data['suggest'] = SuggestedUseList.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'suggest'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/suggestdata-list/' + str(self.kwargs['id'])


class SuggestedDataUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SuggestedUseData
    template_name = 'suggestdata_edit.html'
    form_class = SuggestedDataForm
    success_message = 'Suggested Data successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(SuggestedDataUpdate, self).get_context_data(**kwargs)
        data['open_space'] = OpenSpace.objects.filter(id=self.kwargs['id']).select_related('province', 'district',
                                                                                           'municipality').order_by(
            'id')
        data['suggest'] = SuggestedUseList.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'suggest'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/suggestdata-list/' + str(self.kwargs['id'])


class ServiceCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ServiceList
    template_name = 'service_add.html'
    form_class = ServiceForm
    success_message = 'Service successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ServiceCreate, self).get_context_data(**kwargs)
        # data['open_space'] = OpenSpace.objects.select_related('province', 'district', 'municipality').order_by('id')
        # data['suggest'] = SuggestedUseList.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'service'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('service-list')


class GalleryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ServiceList
    template_name = 'gallery_add.html'
    form_class = GalleryForm
    success_message = 'Gallery successfully Created'

    def get_context_data(self, **kwargs):
        data = super(GalleryCreate, self).get_context_data(**kwargs)
        data['open_space'] = OpenSpace.objects.filter(id=self.kwargs['id']).select_related('province', 'district',
                                                                                           'municipality').order_by(
            'id')
        # data['suggest'] = SuggestedUseList.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'service'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/gallery-list/' + str(self.kwargs['id'])

    def form_valid(self, form):
        # user_data = UserProfile.objects.get(user=self.request.user)
        open_space = self.request.POST['open_space']
        type = self.request.POST.getlist('type')
        image = self.request.FILES.getlist('image')
        print(open_space)
        print(type)
        print(image)
        upper_range = len(type)
        for row in range(0, upper_range):
            Gallery.objects.create(open_space_id=open_space, type=type[row], image=image[row], )
        return HttpResponseRedirect(self.get_success_url())


class ServiceUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ServiceList
    template_name = 'service_edit.html'
    form_class = ServiceForm
    success_message = 'Service successfully Edited'

    def get_context_data(self, **kwargs):
        data = super(ServiceUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'suggest'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('service-list')


class ServiceDataCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ServiceData
    template_name = 'servicedata_add.html'
    form_class = ServiceDataForm
    success_message = 'Service Data successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ServiceDataCreate, self).get_context_data(**kwargs)
        data['open_space'] = OpenSpace.objects.filter(id=self.kwargs['id']).select_related('province', 'district',
                                                                                           'municipality').order_by(
            'id')
        data['service'] = ServiceList.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'service'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/servicedata-list/' + str(self.kwargs['id'])


class GalleryUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Gallery
    template_name = 'gallery_edit.html'
    form_class = GalleryForm
    success_message = 'Gallery successfully edited'

    def get_context_data(self, **kwargs):
        data = super(GalleryUpdate, self).get_context_data(**kwargs)
        data['open_space'] = OpenSpace.objects.filter(id=self.kwargs['id']).select_related('province', 'district',
                                                                                           'municipality').order_by(
            'id')
        # data['suggest'] = SuggestedUseList.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'openspace'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/gallery-list/' + str(self.kwargs['id'])


class ServiceDataUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ServiceData
    template_name = 'servicedata_edit.html'
    form_class = ServiceDataForm
    success_message = 'Service Data Updated Successfully'

    def get_context_data(self, **kwargs):
        data = super(ServiceDataUpdate, self).get_context_data(**kwargs)
        data['open_space'] = OpenSpace.objects.filter(id=self.kwargs['id']).select_related('province', 'district',
                                                                                           'municipality').order_by(
            'id')
        data['service'] = ServiceList.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'service'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/servicedata-list/' + str(self.kwargs['id'])


class ResourceCategoryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ResourceCategory
    template_name = 'resourcecategory_add.html'
    form_class = ResourceCategoryForm
    success_message = 'Resource Category successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ResourceCategoryCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'resource'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('resource-category-list')


class ResourceDocumentTypeCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ResourceDocumentType
    template_name = 'resourcedocument_add.html'
    form_class = ResourceDocumentTypeForm
    success_message = 'Resource Document Type successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ResourceDocumentTypeCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'resource'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('resource-document-list')


class HeaderList(LoginRequiredMixin, ListView):
    template_name = 'header.html'
    model = Header

    def get_context_data(self, **kwargs):
        data = super(HeaderList, self).get_context_data(**kwargs)
        query_data = Header.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['user'] = user_data
        data['active'] = 'header'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class HeaderUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Header
    template_name = 'header_edit.html'
    form_class = HeaderForm
    success_message = 'Openspace portal successfully  updated'

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(HeaderUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'header'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('header-list')


class SliderList(LoginRequiredMixin, ListView):
    template_name = 'slider_list.html'
    model = Slider

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(SliderList, self).get_context_data(**kwargs)
        query_data = Slider.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['model'] = 'Slider'
        data['url'] = 'slider-list'
        data['user'] = user_data
        data['active'] = 'slider'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class WhyMapOpenSpaceList(LoginRequiredMixin, ListView):
    template_name = 'why_map_openspace.html'
    model = WhyMapOpenSpace

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(WhyMapOpenSpaceList, self).get_context_data(**kwargs)
        query_data = WhyMapOpenSpace.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['model'] = 'WhyMapOpenSpace'
        data['url'] = 'why-openspace-list'
        data['user'] = user_data
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class WhyMapOpenSpaceUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = WhyMapOpenSpace
    template_name = 'why_map_openspace_update.html'
    form_class = WhyMapOpenSpaceForm
    success_message = 'Openspace portal successfully  updated'

    def get_context_data(self, **kwargs):
        data = super(WhyMapOpenSpaceUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'header'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('why-openspace-list')


class WhyMapOpenSpaceIconList(LoginRequiredMixin, ListView):
    template_name = 'why_map_openspace_icon.html'
    model = WhyMapOpenIcon

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(WhyMapOpenSpaceIconList, self).get_context_data(**kwargs)
        query_data = WhyMapOpenIcon.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['model'] = 'WhyMapOpenIcon'
        data['url'] = 'why-openicon-list'
        data['user'] = user_data
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class WhyMapOpenSpaceIconUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = WhyMapOpenIcon
    template_name = 'why_map_openicon_update.html'
    form_class = WhyMapOpenSpaceIconForm
    success_message = 'Openspace portal successfully  updated'

    def get_context_data(self, **kwargs):
        data = super(WhyMapOpenSpaceIconUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'header'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('why-openicon-list')


class WhyMapOpenSpaceIconCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = WhyMapOpenIcon
    template_name = 'why_map_openicon_add.html'
    form_class = WhyMapOpenSpaceIconForm
    success_message = 'Why map open icon successfully created'

    def get_context_data(self, **kwargs):
        data = super(WhyMapOpenSpaceIconCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'why-openicon-list'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count
        return data

    def get_success_url(self):
        return reverse_lazy('why-openicon-list')


class AboutHeaderList(LoginRequiredMixin, ListView):
    template_name = 'about_header_list.html'
    model = AboutHeader

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(AboutHeaderList, self).get_context_data(**kwargs)
        query_data = AboutHeader.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['model'] = 'AboutHeader'
        data['url'] = 'about-header-list'
        data['user'] = user_data
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class AboutHeaderUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AboutHeader
    template_name = 'about_header_update.html'
    form_class = AboutHeaderForm
    success_message = 'About Page Header successfully  updated'

    def get_context_data(self, **kwargs):
        data = super(AboutHeaderUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'header'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('about-header-list')


class OpenSpaceCriteriaList(LoginRequiredMixin, ListView):
    template_name = 'about_open_criteria_list.html'
    model = OpenSpaceCriteria

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(OpenSpaceCriteriaList, self).get_context_data(**kwargs)
        query_data = OpenSpaceCriteria.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['model'] = 'OpenSpaceCriteria'
        data['url'] = 'openspace-criteria-list'
        data['user'] = user_data
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class OpenSpaceCriteriaUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = OpenSpaceCriteria
    template_name = 'about_open_criteria_update.html'
    form_class = OpenSpaceCriteriaForm
    success_message = 'About Page Header successfully  updated'

    def get_context_data(self, **kwargs):
        data = super(OpenSpaceCriteriaUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'header'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('openspace-criteria-list')


class AboutCriteriaTypeList(LoginRequiredMixin, ListView):
    template_name = 'about_criteria_type_list.html'
    model = CriteriaType

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(AboutCriteriaTypeList, self).get_context_data(**kwargs)
        query_data = CriteriaType.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['model'] = 'CriteriaType'
        data['url'] = 'about-criteria-type-list'
        data['user'] = user_data
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class AboutCriteriaTypeUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = CriteriaType
    template_name = 'about_criteria_type_update.html'
    form_class = CriteriaTypeForm
    success_message = 'Criteria Type successfully  updated'

    def get_context_data(self, **kwargs):
        data = super(AboutCriteriaTypeUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'criteria_type'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('about-criteria-type-list')


class AboutCriteriaTypeCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = CriteriaType
    template_name = 'about_criteria_type_add.html'
    form_class = CriteriaTypeForm
    success_message = 'Criteria Type successfully created'

    def get_context_data(self, **kwargs):
        data = super(AboutCriteriaTypeCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'criteria_type'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('about-criteria-type-list')


class AboutCriteriaTypeDescriptionList(LoginRequiredMixin, ListView):
    template_name = 'about_criteria_type_description_list.html'
    model = CriteriaDescription

    def get_context_data(self, **kwargs):
        data = super(AboutCriteriaTypeDescriptionList, self).get_context_data(**kwargs)
        query_data = CriteriaDescription.objects.filter(type__title=self.kwargs['criteria_type'])
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        c_type = CriteriaType.objects.get(title=self.kwargs['criteria_type'])
        data['list'] = query_data
        data['model'] = 'CriteriaDescription'
        url = 'about_criteria_type_description_list/' + str(self.kwargs['criteria_type'])
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        # print(base64_url)
        data['url'] = base64_url
        data['type'] = c_type
        data['user'] = user_data
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class AboutCriteriaTypeDescriptionUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = CriteriaDescription
    template_name = 'about_criteria_type_description_update.html'
    form_class = CriteriaDescriptionForm
    success_message = 'Criteria Type Description successfully  updated'

    def get_context_data(self, **kwargs):
        data = super(AboutCriteriaTypeDescriptionUpdate, self).get_context_data(**kwargs)
        type = CriteriaType.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'criteria_type'
        data['types'] = type
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/about_criteria_type_description_list/' + str(self.kwargs['criteria_type'])


class AboutCriteriaTypeDescriptionCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = CriteriaDescription
    template_name = 'about_criteria_type_description_add.html'
    form_class = CriteriaDescriptionForm
    success_message = 'Criteria Type description successfully created'

    def get_context_data(self, **kwargs):
        data = super(AboutCriteriaTypeDescriptionCreate, self).get_context_data(**kwargs)
        user = self.request.user
        c_type = CriteriaType.objects.get(title=self.kwargs['criteria_type'])
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'criteria_type'
        data['type'] = c_type
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/about_criteria_type_description_list/' + str(self.kwargs['criteria_type'])


class SliderUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Slider
    template_name = 'slider_edit.html'
    form_class = SliderForm
    success_message = 'Slider Successfully updated'

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(SliderUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'header'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('slider-list')


class ResourceCategoryUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ResourceCategory
    template_name = 'resourcecategory_edit.html'
    form_class = ResourceCategoryForm
    success_message = 'Resource Category successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ResourceCategoryUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'resource'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('resource-category-list')


class ResourceDocumentTypeUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ResourceDocumentType
    template_name = 'resourcedocument_edit.html'
    form_class = ResourceDocumentTypeForm
    success_message = 'Resource Document Type successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ResourceDocumentTypeUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'resource'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('resource-document-list')


class SliderCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Slider
    template_name = 'slider_add.html'
    form_class = SliderForm
    success_message = 'Slider instance successfully Created'

    def get_context_data(self, **kwargs):
        data = super(SliderCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'slider'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('slider-list')


class OpenSpaceDefinitionList(LoginRequiredMixin, ListView):
    template_name = 'openspace_defination_list.html'
    model = OpenSpaceDef

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(OpenSpaceDefinitionList, self).get_context_data(**kwargs)
        query_data = OpenSpaceDef.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['user'] = user_data
        data['active'] = 'open_def'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class OpenSpaceDefinitionUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = OpenSpaceDef
    template_name = 'openspace_defination_edit.html'
    form_class = OpenSpaceDefForm
    success_message = 'Open Space Definition Successfully updated'

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(OpenSpaceDefinitionUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'open_def'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('openspace-definition-list')


class OpenSpaceIdentificationList(LoginRequiredMixin, ListView):
    template_name = 'openspace_identification_list.html'
    model = OpenSpaceIde

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(OpenSpaceIdentificationList, self).get_context_data(**kwargs)
        query_data = OpenSpaceIde.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['user'] = user_data
        data['active'] = 'open_ide'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class OpenSpaceIdentificationUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = OpenSpaceIde
    template_name = 'openspace_identification_edit.html'
    form_class = OpenSpaceIdeForm
    success_message = 'Open Space Identification Successfully Updated'

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(OpenSpaceIdentificationUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'open_ide'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('openspace-identification-list')


class OpenSpaceIdentificationProcessList(LoginRequiredMixin, ListView):
    template_name = 'open_space_identification_process_list.html'
    model = CreateOpenSpace

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(OpenSpaceIdentificationProcessList, self).get_context_data(**kwargs)
        query_data = CreateOpenSpace.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['model'] = 'CreateOpenSpace'
        data['url'] = 'openspace-identification-process-list'
        data['user'] = user_data
        data['active'] = 'open_ide_process'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class OpenSpaceIdentificationProcessUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = CreateOpenSpace
    template_name = 'open_space_identification_process_edit.html'
    form_class = CreateOpenSpaceForm
    success_message = 'Open Space Identification Process Successfully Updated'

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(OpenSpaceIdentificationProcessUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'open_ide_process'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('openspace-identification-process-list')


class OpenSpaceIdentificationProcessCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = CreateOpenSpace
    template_name = 'open_space_identification_process_add.html'
    form_class = CreateOpenSpaceForm
    success_message = 'Open Space Identification Process Successfully Created'

    def get_context_data(self, **kwargs):
        data = super(OpenSpaceIdentificationProcessCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'open_ide_process'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('openspace-identification-process-list')


class OpenSpaceIdentificationPointList(LoginRequiredMixin, ListView):
    template_name = 'open_space_identification_point_list.html'
    model = CreateOpenSpacePoints

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(OpenSpaceIdentificationPointList, self).get_context_data(**kwargs)
        query_data = CreateOpenSpacePoints.objects.filter(steps__title=self.kwargs['title'])
        step = CreateOpenSpace.objects.get(title=self.kwargs['title'])
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'open_space_identification_points_list/' + str(self.kwargs['title'])
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['list'] = query_data
        data['model'] = 'CreateOpenSpacePoints'
        data['url'] = url
        data['user'] = user_data
        data['active'] = 'open_ide_points'
        data['step'] = step
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class OpenSpaceIdentificationPointsUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = CreateOpenSpacePoints
    template_name = 'open_space_identification_point_update.html'
    form_class = CreateOpenSpacePointsForm
    success_message = 'Open Space Identification Process sub steps Successfully Updated'

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(OpenSpaceIdentificationPointsUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'open_ide_process'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/open_space_identification_points_list/' + str(self.kwargs['title'])


class OpenSpaceIdentificationPointsCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = CreateOpenSpacePoints
    template_name = 'open_space_identification_point_add.html'
    form_class = CreateOpenSpacePointsForm
    success_message = 'Open Space Identification Process sub steps Successfully Created'

    def get_context_data(self, **kwargs):
        data = super(OpenSpaceIdentificationPointsCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        step = CreateOpenSpace.objects.get(title=self.kwargs['title'])
        data['user'] = user_data
        data['active'] = 'open_ide_process_point'
        data['step'] = step
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return '/dashboard/open_space_identification_points_list/' + str(self.kwargs['title'])


class FooterList(LoginRequiredMixin, ListView):
    template_name = 'footer_list.html'
    model = Contact

    def get_context_data(self, **kwargs):
        print('footer')
        data = super(FooterList, self).get_context_data(**kwargs)
        query_data = Contact.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['user'] = user_data
        data['active'] = 'footer'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class FooterUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'footer_edit.html'
    form_class = ContactForm
    success_message = 'Contact Successfully Updated'

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(FooterUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'footer'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('footer-list')


class AppList(LoginRequiredMixin, ListView):
    template_name = 'app_list.html'
    model = OpenSpaceApp

    def get_context_data(self, **kwargs):
        print('footer')
        data = super(AppList, self).get_context_data(**kwargs)
        query_data = OpenSpaceApp.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['model'] = 'OpenSpaceApp'
        data['url'] = 'app-list'
        data['user'] = user_data
        data['active'] = 'app'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        print(data)
        return data


class AppUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = OpenSpaceApp
    template_name = 'app_edit.html'
    form_class = OpenSpaceAppForm
    success_message = 'App Successfully Updated'

    def get_context_data(self, **kwargs):
        print('abc')
        data = super(AppUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'app'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('app-list')


class AppCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = OpenSpaceApp
    template_name = 'app_add.html'
    form_class = OpenSpaceAppForm
    success_message = 'App Created'

    def get_context_data(self, **kwargs):
        data = super(AppCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'open_ide_process'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data

    def get_success_url(self):
        return reverse_lazy('app-list')


class OpenSpaceMuniList(LoginRequiredMixin, ListView):
    template_name = 'open_muni_list.html'
    model = OpenSpace

    def get_context_data(self, **kwargs):
        print('footer')
        data = super(OpenSpaceMuniList, self).get_context_data(**kwargs)
        municipality = OpenSpace.objects.values('municipality__name', 'province__name', 'municipality__hlcit_code').order_by('municipality__name').distinct()
        # print(municipality)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        # open_space = OpenSpace.objects.filter(municipality__id=self.kwargs['id'])
        data['list'] = municipality
        data['model'] = 'OpenSpaceApp'
        data['url'] = 'app-list'
        data['user'] = user_data
        data['active'] = 'app'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


def CreateUser(request, **kwargs):
    pen_count = Report.objects.filter(status='pending').count()
    user = request.user
    user_data = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.is_active = False
            # user.save()
            group = Group.objects.get(name='admin')
            user.groups.add(group)
            UserProfile.objects.create(user=user, name=request.POST['name'], email=request.POST['email'],
                                       municipality_id=int(request.POST['municipality']), )

            return render(request, 'registered_message.html', {'user': request.POST['name'], 'pending': pen_count,})
        else:

            municipality = Municipality.objects.select_related('province', 'district', ).all()
            return render(request, 'create_user.html', {'form': form, 'municipalities': municipality, 'pending': pen_count})

    form = UserCreationForm()
    municipality = Municipality.objects.select_related('province', 'district', ).all()

    return render(request, 'create_user.html', {'form': form, 'municipalities': municipality, 'pending': pen_count, 'user': user_data})


def create_agency(request, **kwargs):
    pen_count = Report.objects.filter(status='pending').count()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserAgency.objects.create(user=user, agency_name=request.POST['agency_name'], email=request.POST['email'],
                                      address=request.POST['address'], contact=request.POST['contact'])

            return redirect('/dashboard/agency_list/')
        else:
            return render(request, 'create_agency.html', {'form':form, 'pending': pen_count})

    else:
        return render(request, 'create_agency.html', {'pending': pen_count})


def report_reply(request, **kwargs):
    if request.method == 'POST':
        data = FCMDevice.objects.filter(device_id=request.POST['id'])
        if data.count() < 1:
            FCMDevice.objects.create(name=request.POST['name'], device_id=request.POST['id'],
                                     registration_id=request.POST['token'], type='android')

        device = FCMDevice.objects.get(device_id=request.POST['id'])

        print('aaaaaaaaaaaaaaaaaaaaa', device)
        device.send_message(request.POST['title'], request.POST['reply'])
        Report.objects.filter(id=request.POST['id']).update(reply=request.POST['reply'], status="replied")
        return redirect('/dashboard/report-list')
    else:
        return redirect('/dashboard/report-list')


class AmenityTypeList(LoginRequiredMixin, ListView):
    template_name = 'amenity_type_list.html'
    model = AvailableType

    def get_context_data(self, **kwargs):
        data = super(AmenityTypeList, self).get_context_data(**kwargs)
        query_data = AvailableType.objects.all()
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        data['model'] = 'AvailableType'
        data['url'] = 'amenity_type'
        data['user'] = user_data
        data['active'] = 'amenity_type'
        data['hlcit_code'] = self.kwargs['hlcit_code']
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class AvailableAmenityFacilityList(LoginRequiredMixin, ListView):
    template_name = 'available_amenity_list.html'
    model = AvailableFacility

    def get_context_data(self, **kwargs):
        data = super(AvailableAmenityFacilityList, self).get_context_data(**kwargs)
        query_data = AvailableFacility.objects.filter(available_type__title=self.kwargs['title'],
                                                      municipality__hlcit_code=self.kwargs['hlcit_code']).\
            values('id', 'name', 'available_type__title', 'district__name', 'municipality__name', 'address', 'email',
                   'phone_number', 'opening_hours', 'operator_type').order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)

        url = 'available_ameni_list/' + self.kwargs['title'] + '/' + self.kwargs['hlcit_code']
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['list'] = query_data
        data['model'] = 'AvailableFacility'
        data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'available'
        data['hlcit_code'] = self.kwargs['hlcit_code']
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count

        return data


class AvailableAmenityCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = AvailableType
    template_name = 'amenity_type_add.html'
    form_class = AvailableTypeForm
    success_message = 'Amenity type Created'

    def get_context_data(self, **kwargs):
        data = super(AvailableAmenityCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'amenity_type'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count
        return data

    def get_success_url(self):
        return reverse_lazy('amenity_type')


class AvailableAmenityUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AvailableType
    template_name = 'amenity_type_update.html'
    form_class = AvailableTypeForm
    success_message = 'Amenity type successfully updated'

    def get_context_data(self, **kwargs):
        data = super(AvailableAmenityUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'amenity_type'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count
        return data

    def get_success_url(self):
        return reverse_lazy('amenity_type')


# class AgencyLogIn(LoginRequiredMixin,)

class AgencyMessageList(LoginRequiredMixin, ListView):
    template_name = 'messages_list.html'
    model = AgencyMessage

    def get_context_data(self, **kwargs):
        data = super(AgencyMessageList, self).get_context_data(**kwargs)
        user = self.request.user
        try:
            if user.agency:
                query_data = AgencyMessage.objects.filter(agency__user=user)
                data['user'] = user
        except:
            query_data = AgencyMessage.objects.all()
            user_data = UserProfile.objects.get(user=user)
            data['user'] = user_data
        url = 'agency_message/'
        # url_bytes = url.encode('ascii')
        # base64_bytes = base64.b64encode(url_bytes)
        # base64_url = base64_bytes.decode('ascii')
        data['list'] = query_data
        data['model'] = 'AgencyMessage'
        # data['url'] = base64_url
        data['url'] = 'agency_message'
        data['active'] = 'agency_message'
        pen_count = Report.objects.filter(status='pending').count()
        data['pending'] = pen_count
        return data


class AgencyMessageCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = AgencyMessage
    template_name = 'agency_add_message.html'
    form_class = AgencyMessageForm
    success_message = 'Message Successfully Added'

    def get_context_data(self, **kwargs):
        data = super(AgencyMessageCreate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        agency = UserAgency.objects.get(user=user)
        municipality = Municipality.objects.all()
        open_space = OpenSpace.objects.all()
        # data['user'] = user_data
        data['agencies'] = agency
        data['open_spaces'] = open_space
        data['municipalities'] = municipality
        data['active'] = 'agency_message'
        return data

    def get_success_url(self):
        return reverse_lazy('agency_message')


class AgencyMessageUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AgencyMessage
    template_name = 'agency_update_message.html'
    form_class = AgencyMessageForm
    success_message = 'Message successfully updated'

    def get_context_data(self, **kwargs):
        data = super(AgencyMessageUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        # agency = UserAgency.objects.get(user=user)
        municipality = Municipality.objects.all()
        open_space = OpenSpace.objects.all()
        # data['user'] = user_data
        # data['agencies'] = agency
        data['open_spaces'] = open_space
        data['municipalities'] = municipality
        data['active'] = 'agency_message'
        return data

    def get_success_url(self):
        return reverse_lazy('agency_message')



def deleteData(request, **kwargs):
    model = apps.get_model(app_label='core', model_name=kwargs['model'])
    delete = model.objects.filter(id=kwargs['id']).delete()
    messages.success(request, "Deleted SuccessFully")
    base64_url = kwargs['url']
    base64_bytes = base64_url.encode('ascii')
    url_bytes = base64.b64decode(base64_bytes)
    url = url_bytes.decode('ascii')
    return redirect('/dashboard/' + url)


def deleteDataFront(request, **kwargs):
    model = apps.get_model(app_label='front', model_name=kwargs['model'])
    delete = model.objects.filter(id=kwargs['id']).delete()
    messages.success(request, "Deleted SuccessFully")
    return redirect(kwargs['url'])
    # print(model)


def deleteDataDashboard(request, **kwargs):
    model = apps.get_model(app_label='dashboard', model_name=kwargs['model'])
    delete = model.objects.filter(id=kwargs['id']).delete()
    messages.success(request, "Deleted SuccessFully")
    return redirect(kwargs['url'])


@login_required
def homePageListView(request):
    user = request.user
    user_data = UserProfile.objects.get(user=user)
    pen_count = Report.objects.filter(status='pending').count()
    return render(request, 'home_page_list.html', {'user': user_data, 'pending': pen_count})


@login_required
def aboutPageListView(request):
    user = request.user
    user_data = UserProfile.objects.get(user=user)
    pen_count = Report.objects.filter(status='pending').count()
    return render(request, 'about_page_list.html', {'user': user_data, 'pending': pen_count})


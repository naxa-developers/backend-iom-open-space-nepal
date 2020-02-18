from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.models import OpenSpace, AvailableFacility, Report, QuestionList, QuestionsData, ServiceData, ServiceList, \
    SuggestedUseList, SuggestedUseData, Resource, ResourceCategory, ResourceDocumentType, Province, District, \
    Municipality, Slider, CreateOpenSpace, Gallery
from .models import UserProfile
import json
import random
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import OpenSpaceForm, AvailableFacilityForm, QuestionForm, QuestionDataForm, SuggestedForm, \
    SuggestedDataForm, ServiceForm, ServiceDataForm, ResourceCategoryForm, HeaderForm, SliderForm, OpenSpaceDefForm, \
    OpenSpaceIdeForm, OpenSpaceAppForm, ContactForm, CreateOpenSpaceForm, GalleryForm, ImportShapefileForm, \
    ResourceDocumentTypeForm, ResourceForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission
from front.models import Header, OpenSpaceDef, OpenSpaceIde, OpenSpaceApp, Contact
from django.apps import apps
from django.contrib import messages
import base64
import os
from django.contrib.gis.utils import LayerMapping
from django.shortcuts import render_to_response
from dashboard import shapefileIO
from django.contrib.gis.gdal import DataSource
from fcm_django.models import FCMDevice


# Create your views here.
class HomePage(TemplateView):

    def get(self, request, *args, **kwargs):
        # category = ProductCategory.objects.order_by('id')
        # product = Product.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
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
        # print(service_open)
        pen_count = Report.objects.filter(status='pending').count()
        com_count = Report.objects.filter(status='replied').count()
        return render(request, 'dashboard.html',
                      {'data_list1': data_list1, 'data_list2': data_listt2, 'open_space_name': open_spaces,
                       'pie_count': columns, 'pie_name': columns_dict, 'pie_color': color_dict, 'group': group.name,
                       'mun_id': mun_id, 'user': user_data, 'pending': pen_count, 'completed': com_count})


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


class OpenSpaceList(LoginRequiredMixin, ListView):
    template_name = 'openspace_list.html'
    model = OpenSpace

    def get_context_data(self, **kwargs):
        data = super(OpenSpaceList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        print(user_data)
        if group.name == "admin":
            query_data = OpenSpace.objects.filter(municipality__id=user_data.municipality.id).select_related('province',
                                                                                                             'district',
                                                                                                             'municipality').order_by(
                'id')
        else:
            query_data = OpenSpace.objects.select_related('province', 'district', 'municipality').order_by('id')

        url = 'openspace-list/'
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        data['list'] = query_data
        data['model'] = 'OpenSpace'
        data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'openspace'
        return data


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
        return data


class ReportList(LoginRequiredMixin, ListView):
    template_name = 'reports_list.html'
    model = Report

    def get_context_data(self, **kwargs):
        data = super(ReportList, self).get_context_data(**kwargs)
        query_data = Report.objects.select_related('open_space', ).order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        url = 'report-list/'

        data['list'] = query_data
        data['model'] = 'Report'
        # data['url'] = base64_url
        data['user'] = user_data
        data['active'] = 'available'
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
        return data

    def get_success_url(self):
        return reverse_lazy('resource-list')


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
        return data


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
        return data

    def get_success_url(self):
        return reverse_lazy('openspace-identification-list')


class OpenSpaceIdentificationProcessList(LoginRequiredMixin, ListView):
    print('abc')
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
        return data

    def get_success_url(self):
        return reverse_lazy('openspace-identification-process-list')


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
        return data

    def get_success_url(self):
        return reverse_lazy('app-list')


def CreateUser(request, **kwargs):
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

            return render(request, 'registered_message.html', {'user': request.POST['name']})
        else:

            municipality = Municipality.objects.select_related('province', 'district', ).all()
            return render(request, 'create_user.html', {'form': form, 'municipalities': municipality})

    form = UserCreationForm()
    municipality = Municipality.objects.select_related('province', 'district', ).all()
    return render(request, 'create_user.html', {'form': form, 'municipalities': municipality})


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

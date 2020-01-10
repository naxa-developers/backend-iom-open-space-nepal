from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.models import OpenSpace, AvailableFacility, Report, QuestionList, QuestionsData, ServiceData, ServiceList, \
    SuggestedUseList, SuggestedUseData, Resource, ResourceCategory, ResourceDocumentType
import json
import random
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import OpenSpaceForm, AvailableFacilityForm, QuestionForm, QuestionDataForm, SuggestedForm


# Create your views here.
class HomePage(TemplateView):

    def get(self, request, *args, **kwargs):
        # category = ProductCategory.objects.order_by('id')
        # product = Product.objects.order_by('id')

        data_list1 = []
        data_list2 = []
        open_space_total = list(OpenSpace.objects.filter(municipality__id=96).values_list('total_area', flat=True))
        open_space_usable = list(OpenSpace.objects.filter(municipality__id=96).values_list('usable_area', flat=True))
        open_space_name = list(OpenSpace.objects.filter(municipality__id=96).values_list('title', flat=True))
        service_list = ServiceList.objects.order_by('id')

        columns = []
        columns_dict = {}
        color_dict = {}

        for l in service_list:
            count = ServiceData.objects.filter(open_space__municipality=96, service__id=l.id).count()
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

        return render(request, 'dashboard.html',
                      {'data_list1': data_list1, 'data_list2': data_listt2, 'open_space_name': open_spaces,
                       'pie_count': columns, 'pie_name': columns_dict, 'pie_color': color_dict})


class OpenSpaceList(LoginRequiredMixin, ListView):
    template_name = 'openspace_list.html'
    model = OpenSpace

    def get_context_data(self, **kwargs):
        data = super(OpenSpaceList, self).get_context_data(**kwargs)
        query_data = OpenSpace.objects.select_related('province', 'district', 'municipality').order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'openspace'
        return data


class AvailableFacilityList(LoginRequiredMixin, ListView):
    template_name = 'available_list.html'
    model = AvailableFacility

    def get_context_data(self, **kwargs):
        data = super(AvailableFacilityList, self).get_context_data(**kwargs)
        query_data = AvailableFacility.objects.select_related('province', 'district', 'municipality').order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'available'
        return data


class ReportList(LoginRequiredMixin, ListView):
    template_name = 'reports_list.html'
    model = Report

    def get_context_data(self, **kwargs):
        data = super(ReportList, self).get_context_data(**kwargs)
        query_data = Report.objects.select_related('open_space', ).order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'available'
        return data


class QuestionsList(LoginRequiredMixin, ListView):
    template_name = 'question_list.html'
    model = QuestionList

    def get_context_data(self, **kwargs):
        data = super(QuestionsList, self).get_context_data(**kwargs)
        query_data = QuestionList.objects.order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'available'
        return data


class QuestionData(LoginRequiredMixin, ListView):
    template_name = 'questiondata_list.html'
    model = QuestionsData

    def get_context_data(self, **kwargs):
        data = super(QuestionData, self).get_context_data(**kwargs)
        query_data = QuestionsData.objects.select_related('open_space', 'question', ).order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'available'
        return data


class SuggestedUseLists(LoginRequiredMixin, ListView):
    template_name = 'suggest_list.html'
    model = SuggestedUseList

    def get_context_data(self, **kwargs):
        data = super(SuggestedUseLists, self).get_context_data(**kwargs)
        query_data = SuggestedUseList.objects.order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'available'
        return data


class SuggestedUseDataList(LoginRequiredMixin, ListView):
    template_name = 'suggestdata_list.html'
    model = SuggestedUseData

    def get_context_data(self, **kwargs):
        data = super(SuggestedUseDataList, self).get_context_data(**kwargs)
        query_data = SuggestedUseData.objects.select_related('open_space', 'suggested_use', ).order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'available'
        return data


class ServiceLists(LoginRequiredMixin, ListView):
    template_name = 'service_list.html'
    model = ServiceList

    def get_context_data(self, **kwargs):
        data = super(ServiceLists, self).get_context_data(**kwargs)
        query_data = ServiceList.objects.order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'available'
        return data


class ServiceDataList(LoginRequiredMixin, ListView):
    template_name = 'servicedata_list.html'
    model = ServiceData

    def get_context_data(self, **kwargs):
        data = super(ServiceDataList, self).get_context_data(**kwargs)
        query_data = ServiceData.objects.select_related('open_space', 'service', ).order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'available'
        return data


class ResourceList(LoginRequiredMixin, ListView):
    template_name = 'resource_list.html'
    model = Resource

    def get_context_data(self, **kwargs):
        data = super(ResourceList, self).get_context_data(**kwargs)
        query_data = Resource.objects.select_related('category', 'document_type', ).order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'resource'
        return data


class ResourceCategoryList(LoginRequiredMixin, ListView):
    template_name = 'resource_category_list.html'
    model = ResourceCategory

    def get_context_data(self, **kwargs):
        data = super(ResourceCategoryList, self).get_context_data(**kwargs)
        query_data = ResourceCategory.objects.order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
        data['active'] = 'resource'
        return data


class ResourceDocumentList(LoginRequiredMixin, ListView):
    template_name = 'resource_document_list.html'
    model = ResourceDocumentType

    def get_context_data(self, **kwargs):
        data = super(ResourceDocumentList, self).get_context_data(**kwargs)
        query_data = ResourceDocumentType.objects.order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = query_data
        # data['user'] = user_data
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
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        data['active'] = 'openspace'
        return data

    def get_success_url(self):
        return reverse_lazy('openspace-list')


class AvailableFacilityCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = AvailableFacility
    template_name = 'available_facility_add.html'
    form_class = AvailableFacilityForm
    success_message = 'Available Facility successfully Created'

    def get_context_data(self, **kwargs):
        data = super(AvailableFacilityCreate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        data['active'] = 'available'
        return data

    def get_success_url(self):
        return reverse_lazy('available-list')


class QuestionCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = QuestionsList
    template_name = 'question_add.html'
    form_class = QuestionForm
    success_message = 'Question Facility successfully Created'

    def get_context_data(self, **kwargs):
        data = super(QuestionCreate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        data['active'] = 'question'
        return data

    def get_success_url(self):
        return reverse_lazy('question-list')


class QuestionUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = QuestionList
    template_name = 'question_edit.html'
    form_class = QuestionForm
    success_message = 'Question successfully  updated'

    def get_context_data(self, **kwargs):
        data = super(QuestionUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
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
        data['open_space'] = OpenSpace.objects.select_related('province', 'district', 'municipality').order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        data['active'] = 'question'
        return data

    def get_success_url(self):
        return reverse_lazy('questiondata-list')


class QuestionDataUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = QuestionsData
    template_name = 'questiondata_edit.html'
    form_class = QuestionDataForm
    success_message = 'Question Data successfully  updated'

    def get_context_data(self, **kwargs):
        data = super(QuestionDataUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        data['question'] = QuestionList.objects.order_by('id')
        data['open_space'] = OpenSpace.objects.select_related('province', 'district', 'municipality').order_by('id')
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        data['active'] = 'question'
        return data

    def get_success_url(self):
        return reverse_lazy('questiondata-list')


class SuggestedCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = SuggestedUseList
    template_name = 'suggest_add.html'
    form_class = SuggestedForm
    success_message = 'Suggested successfully Created'

    def get_context_data(self, **kwargs):
        data = super(SuggestedCreate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        data['active'] = 'suggest'
        return data

    def get_success_url(self):
        return reverse_lazy('suggest-list')


class SuggestedUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SuggestedUseList
    template_name = 'suggest_edit.html'
    form_class = SuggestedForm
    success_message = 'Suggested successfully Edited'

    def get_context_data(self, **kwargs):
        data = super(SuggestedUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        data['active'] = 'suggest'
        return data

    def get_success_url(self):
        return reverse_lazy('suggest-list')

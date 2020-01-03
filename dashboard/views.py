from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.models import OpenSpace, AvailableFacility, Report, QuestionList, QuestionsData, ServiceData, ServiceList, \
    SuggestedUseList, SuggestedUseData
import json
import random


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
            print(l.name)
            print(count)
            columns_dict.update({'data' + str(l.id): l.name})
            service = ['data' + str(l.id), count]
            columns.append(service)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            rgb = 'rgb' + str((r, g, b))
            color_dict.update({'data' + str(l.id): rgb})

        print(columns)
        print(columns_dict)
        print(color_dict)
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

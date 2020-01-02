from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.models import OpenSpace, AvailableFacility, Report, QuestionList, QuestionsData


# Create your views here.
class HomePage(TemplateView):

    def get(self, request, *args, **kwargs):
        # category = ProductCategory.objects.order_by('id')
        # product = Product.objects.order_by('id')
        return render(request, 'dashboard.html', {'categories': 'category', 'products': 'product', })


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

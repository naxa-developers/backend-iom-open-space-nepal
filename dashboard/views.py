from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.models import OpenSpace, AvailableFacility, Report


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
        marker_list = OpenSpace.objects.select_related('province', 'district', 'municipality').order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = marker_list
        # data['user'] = user_data
        data['active'] = 'openspace'
        return data


class AvailableFacilityList(LoginRequiredMixin, ListView):
    template_name = 'available_list.html'
    model = AvailableFacility

    def get_context_data(self, **kwargs):
        data = super(AvailableFacilityList, self).get_context_data(**kwargs)
        marker_list = AvailableFacility.objects.select_related('province', 'district', 'municipality').order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = marker_list
        # data['user'] = user_data
        data['active'] = 'available'
        return data


class ReportList(LoginRequiredMixin, ListView):
    template_name = 'reports_list.html'
    model = Report

    def get_context_data(self, **kwargs):
        data = super(ReportList, self).get_context_data(**kwargs)
        marker_list = Report.objects.select_related('open_space', ).order_by('id')
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        data['list'] = marker_list
        # data['user'] = user_data
        data['active'] = 'available'
        return data

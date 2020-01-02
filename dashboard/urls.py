from django.contrib import admin
from django.urls import path, include
from dashboard import views

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),
    path('openspace-list/', views.OpenSpaceList.as_view(), name='openspace-list'),
    path('available-list/', views.AvailableFacilityList.as_view(), name='available-list'),

]

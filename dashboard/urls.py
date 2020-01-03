from django.contrib import admin
from django.urls import path, include
from dashboard import views

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),
    path('openspace-list/', views.OpenSpaceList.as_view(), name='openspace-list'),
    path('available-list/', views.AvailableFacilityList.as_view(), name='available-list'),
    path('report-list/', views.ReportList.as_view(), name='report-list'),
    path('question-list/', views.QuestionsList.as_view(), name='question-list'),
    path('questiondata-list/', views.QuestionData.as_view(), name='questiondata-list'),
    path('suggest-list/', views.SuggestedUseLists.as_view(), name='suggest-list'),

]

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
    path('suggestdata-list/', views.SuggestedUseDataList.as_view(), name='suggestdata-list'),
    path('service-list/', views.ServiceLists.as_view(), name='service-list'),
    path('servicedata-list/', views.ServiceDataList.as_view(), name='servicedata-list'),
    path('resource-list/', views.ResourceList.as_view(), name='resource-list'),
    path('resource-category-list/', views.ResourceCategoryList.as_view(), name='resource-category-list'),
    path('resource-document-list/', views.ResourceDocumentList.as_view(), name='resource-document-list'),

]

from django.contrib import admin
from django.urls import path, include
from dashboard import views

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),
    path('create-user/', views.CreateUser, name='create-user'),

    path('openspace-list/', views.OpenSpaceList.as_view(), name='openspace-list'),
    path('openspace-add/', views.OpenSpaceCreate.as_view(), name='openspace-add'),

    path('available-list/', views.AvailableFacilityList.as_view(), name='available-list'),
    path('available-add/', views.AvailableFacilityCreate.as_view(), name='available-add'),

    path('report-list/', views.ReportList.as_view(), name='report-list'),

    path('question-list/', views.QuestionsList.as_view(), name='question-list'),
    path('question-add/', views.QuestionCreate.as_view(), name='question-add'),
    path('question-edit/<int:pk>', views.QuestionUpdate.as_view(), name='question-edit'),

    path('questiondata-list/', views.QuestionData.as_view(), name='questiondata-list'),
    path('questiondata-add/', views.QuestionDataCreate.as_view(), name='questiondata-add'),
    path('questiondata-edit/<int:pk>', views.QuestionDataUpdate.as_view(), name='questiondata-edit'),

    path('suggest-list/', views.SuggestedUseLists.as_view(), name='suggest-list'),
    path('suggest-add/', views.SuggestedCreate.as_view(), name='suggest-add'),
    path('suggest-edit/<int:pk>', views.SuggestedUpdate.as_view(), name='suggest-edit'),

    path('suggestdata-list/', views.SuggestedUseDataList.as_view(), name='suggestdata-list'),
    path('suggestdata-add/', views.SuggestedDataCreate.as_view(), name='suggestdata-add'),
    path('suggestdata-edit/<int:pk>', views.SuggestedDataUpdate.as_view(), name='suggestdata-edit'),

    path('service-list/', views.ServiceLists.as_view(), name='service-list'),
    path('service-add/', views.ServiceCreate.as_view(), name='service-add'),
    path('service-edit/<int:pk>', views.ServiceUpdate.as_view(), name='service-edit'),

    path('servicedata-list/', views.ServiceDataList.as_view(), name='servicedata-list'),
    path('servicedata-add/', views.ServiceDataCreate.as_view(), name='servicedata-add'),
    path('servicedata-edit/<int:pk>', views.ServiceDataUpdate.as_view(), name='servicedata-edit'),

    path('resource-list/', views.ResourceList.as_view(), name='resource-list'),

    path('resource-category-list/', views.ResourceCategoryList.as_view(), name='resource-category-list'),
    path('resource-category-add/', views.ResourceCategoryCreate.as_view(), name='resource-category-add'),

    path('resource-document-list/', views.ResourceDocumentList.as_view(), name='resource-document-list'),
    path('header-list/', views.HeaderList.as_view(), name='header-list'),
    path('header-update/<int:pk>', views.HeaderUpdate.as_view(), name='header-update'),

]

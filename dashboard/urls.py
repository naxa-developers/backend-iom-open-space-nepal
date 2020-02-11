from django.contrib import admin
from django.urls import path, include
from dashboard import views

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),
    path('create-user/', views.CreateUser, name='create-user'),
    path('reply-report/', views.report_reply, name='reply-report'),
    path('user-list/', views.UserList.as_view(), name='user-list'),
    path('activate/<int:id>', views.activate_user, name='activate'),
    path('delete/<str:model>/<int:id>/<str:url>', views.deleteData, name='delete'),
    path('delete_front/<str:model>/<int:id>/<str:url>', views.deleteDataFront, name='delete'),

    path('upload-shapefile/', views.importShapefile, name='upload-shapefile'),
    path('openspace-list/', views.OpenSpaceList.as_view(), name='openspace-list'),
    path('openspace-add/', views.OpenSpaceCreate.as_view(), name='openspace-add'),
    path('openspace-edit/<int:pk>', views.OpenSpaceUpdate.as_view(), name='openspace-edit'),

    path('available-list/', views.AvailableFacilityList.as_view(), name='available-list'),
    path('available-add/', views.AvailableFacilityCreate.as_view(), name='available-add'),

    path('report-list/', views.ReportList.as_view(), name='report-list'),

    path('gallery-list/<int:id>', views.GalleryLists.as_view(), name='gallery-list'),
    path('gallery-add/<int:id>', views.GalleryCreate.as_view(), name='gallery-add'),
    path('gallery-edit/<int:pk>/<int:id>', views.GalleryUpdate.as_view(), name='gallery-edit'),

    path('question-list/', views.QuestionsList.as_view(), name='question-list'),
    path('question-add/', views.QuestionCreate.as_view(), name='question-add'),
    path('question-edit/<int:pk>', views.QuestionUpdate.as_view(), name='question-edit'),

    path('questiondata-list/<int:id>', views.QuestionData.as_view(), name='questiondata-list'),
    path('questiondata-add/<int:id>', views.QuestionDataCreate.as_view(), name='questiondata-add'),
    path('questiondata-edit/<int:pk>/<int:id>', views.QuestionDataUpdate.as_view(), name='questiondata-edit'),

    path('suggest-list/', views.SuggestedUseLists.as_view(), name='suggest-list'),
    path('suggest-add/', views.SuggestedCreate.as_view(), name='suggest-add'),
    path('suggest-edit/<int:pk>', views.SuggestedUpdate.as_view(), name='suggest-edit'),

    path('suggestdata-list/<int:id>', views.SuggestedUseDataList.as_view(), name='suggestdata-list'),
    path('suggestdata-add/<int:id>', views.SuggestedDataCreate.as_view(), name='suggestdata-add'),
    path('suggestdata-edit/<int:pk>/<int:id>', views.SuggestedDataUpdate.as_view(), name='suggestdata-edit'),

    path('service-list/', views.ServiceLists.as_view(), name='service-list'),
    path('service-add/', views.ServiceCreate.as_view(), name='service-add'),
    path('service-edit/<int:pk>', views.ServiceUpdate.as_view(), name='service-edit'),

    path('servicedata-list/<int:id>', views.ServiceDataList.as_view(), name='servicedata-list'),
    path('servicedata-add/<int:id>', views.ServiceDataCreate.as_view(), name='servicedata-add'),
    path('servicedata-edit/<int:pk>/<int:id>', views.ServiceDataUpdate.as_view(), name='servicedata-edit'),

    path('resource-list/', views.ResourceList.as_view(), name='resource-list'),

    path('resource-category-list/', views.ResourceCategoryList.as_view(), name='resource-category-list'),
    path('resource-category-add/', views.ResourceCategoryCreate.as_view(), name='resource-category-add'),
    path('resource-category-edit/<int:pk>', views.ResourceCategoryUpdate.as_view(), name='resource-category-edit'),

    path('resource-document-list/', views.ResourceDocumentList.as_view(), name='resource-document-list'),
    path('resource-document-add/', views.ResourceDocumentTypeCreate.as_view(), name='resource-document-add'),
    path('resource-document-edit/<int:pk>', views.ResourceDocumentTypeUpdate.as_view(), name='resource-document-edit'),

    path('header-list/', views.HeaderList.as_view(), name='header-list'),
    path('header-update/<int:pk>', views.HeaderUpdate.as_view(), name='header-update'),
    path('slider-list/', views.SliderList.as_view(), name='slider-list'),
    path('slider-update/<int:pk>', views.SliderUpdate.as_view(), name='slider-update'),
    path('slider-add/', views.SliderCreate.as_view(), name='slider-create'),

    path('openspace-definition-list/', views.OpenSpaceDefinitionList.as_view(), name='openspace-definition-list'),
    path('openspace-definition-update/<int:pk>', views.OpenSpaceDefinitionUpdate.as_view(),
         name='openspace-definition-update'),

    path('openspace-identification-list/', views.OpenSpaceIdentificationList.as_view(),
         name='openspace-identification-list'),
    path('openspace-identification-update/<int:pk>', views.OpenSpaceIdentificationUpdate.as_view(),
         name='openspace-identification-update'),

    path('openspace-identification-process-list/', views.OpenSpaceIdentificationProcessList.as_view(),
         name='openspace-identification-process-list'),
    path('openspace-identification-process-update/<int:pk>', views.OpenSpaceIdentificationProcessUpdate.as_view(),
         name='openspace-identification-process-update'),
    path('openspace-identification-process-create/', views.OpenSpaceIdentificationProcessCreate.as_view(),
         name='openspace-identification-process-create'),

    path('footer-list/', views.FooterList.as_view(), name='footer-list'),
    path('footer-update/<int:pk>', views.FooterUpdate.as_view(), name='footer-update'),

    path('app-list/', views.AppList.as_view(), name='app-list'),
    path('app-add/', views.AppCreate.as_view(), name='app-add'),
    path('app-update/<int:pk>', views.AppUpdate.as_view(), name='app-update'),

]

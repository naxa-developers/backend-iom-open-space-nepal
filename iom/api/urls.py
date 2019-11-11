from rest_framework.routers import DefaultRouter
from api.viewsets import core_viewsets
from django.urls import path, include
from api.viewsets import core_viewsets
from api.viewsets import front_viewset

router = DefaultRouter()
router.register(r'slider', core_viewsets.SliderViewSet)
router.register(r'identify_open_space', core_viewsets.CreateOpenSpaceViewSet)
router.register(r'resource', core_viewsets.ResourceViewSet)
router.register(r'province', core_viewsets.ProvinceViewSet)
router.register(r'district', core_viewsets.DistrictViewSet)
router.register(r'municipality', core_viewsets.MunicipalityViewSet)

router.register(r'suggested_use', core_viewsets.SuggestedUseViewSet)
router.register(r'service', core_viewsets.ServiceViewSet)
router.register(r'question', core_viewsets.QuestionViewSet)
router.register(r'open_space', core_viewsets.OpenSpaceViewSet)
router.register(r'report', core_viewsets.ReportViewSet)

router.register(r'header', front_viewset.HeaderViewSet)
router.register(r'open_space_ide', front_viewset.OpenSpaceIdeViewSet)
router.register(r'open_space_def', front_viewset.OpenSpaceDefViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dummy_api', core_viewsets.dummy_api_view),
    path('open_space_landing', core_viewsets.OpenSpaceLandingApi.as_view()),
    path('district_api', core_viewsets.DistrictApi.as_view()),
    path('municipality_api', core_viewsets.MunicipalityApi.as_view()),
    path('province_api', core_viewsets.ProvinceApi.as_view())
]

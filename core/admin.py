from django.contrib import admin
from core.models import Slider, Province, District, Municipality,\
    SuggestedUseData, OpenSpace, Report, CreateOpenSpace, Resource, \
    QuestionList, QuestionsData, AvailableFacility, Gallery, \
    SuggestedUseList, ServiceData, ServiceList, ResourceCategory, ResourceDocumentType, \
    AvailableType, AvailableSubType, CreateOpenSpacePoints, CommunitySpace

# Register your models here.


admin.site.register(Slider)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(Municipality)
admin.site.register(SuggestedUseList)
admin.site.register(SuggestedUseData)
admin.site.register(QuestionList)
admin.site.register(QuestionsData)
admin.site.register(OpenSpace)
admin.site.register(Resource)
admin.site.register(Report)
admin.site.register(AvailableFacility)
admin.site.register(CreateOpenSpace)
admin.site.register(Gallery)
admin.site.register(ServiceData)
admin.site.register(ServiceList)
admin.site.register(ResourceCategory)
admin.site.register(ResourceDocumentType)
admin.site.register(AvailableType)
admin.site.register(AvailableSubType)
admin.site.register(CreateOpenSpacePoints)
admin.site.register(CommunitySpace)


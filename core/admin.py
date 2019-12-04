from django.contrib import admin
from core.models import Slider, Province, District, Municipality,\
    SuggestedUseData, Services, OpenSpace, Report, CreateOpenSpace,\
    NearbyAmenities, EducationFacility, HealthFacility, Resource, \
    QuestionList, QuestionsData, AvailableFacility, Gallery , ProvinceDummy, SuggestedUseList

# Register your models here.


admin.site.register(Slider)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(Municipality)
admin.site.register(SuggestedUseList)
admin.site.register(SuggestedUseData)
admin.site.register(Services)
admin.site.register(QuestionList)
admin.site.register(QuestionsData)
admin.site.register(OpenSpace)
admin.site.register(Resource)
admin.site.register(Report)
admin.site.register(AvailableFacility)
admin.site.register(CreateOpenSpace)
admin.site.register(NearbyAmenities)
admin.site.register(EducationFacility)
admin.site.register(HealthFacility)
admin.site.register(Gallery)
admin.site.register(ProvinceDummy)

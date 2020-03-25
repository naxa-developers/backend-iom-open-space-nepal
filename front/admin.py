from django.contrib import admin
from front.models import Header, OpenSpaceDef, OpenSpaceIde, Contact,\
    OpenSpaceApp, AboutHeader, CriteriaDescription, CriteriaDescription, OpenSpaceCriteria, WhyMapOpenIcon, WhyMapOpenSpace

# Register your models here.

admin.site.register(Header)
admin.site.register(OpenSpaceIde)
admin.site.register(OpenSpaceDef)
admin.site.register(Contact)
admin.site.register(OpenSpaceApp)
admin.site.register(AboutHeader)
admin.site.register(CriteriaDescription)
admin.site.register(OpenSpaceCriteria)
admin.site.register(WhyMapOpenIcon)
admin.site.register(WhyMapOpenSpace)

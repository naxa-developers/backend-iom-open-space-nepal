from django.contrib import admin
from front.models import Header, OpenSpaceDef, OpenSpaceIde, Contact,\
    OpenSpaceApp

# Register your models here.

admin.site.register(Header)
admin.site.register(OpenSpaceIde)
admin.site.register(OpenSpaceDef)
admin.site.register(Contact)
admin.site.register(OpenSpaceApp)

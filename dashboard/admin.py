from django.contrib import admin
from dashboard.models import UserProfile, AgencyMessage, UserAgency
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserAgency)
admin.site.register(AgencyMessage)

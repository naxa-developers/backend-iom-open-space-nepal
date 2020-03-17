from django.db import models
from django.contrib.auth.models import User
from core.models import Province, District, Municipality, OpenSpace


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)
    # Province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='Province', null=True, blank=True)
    # District = models.ForeignKey(District, on_delete=models.CASCADE, related_name='District', null=True, blank=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='Municipality', null=True,
                                     blank=True)
    image = models.ImageField(upload_to='upload/profile/', null=True, blank=True)

    def __str__(self):
        return self.name


class UserAgency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agency')
    agency_name = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    contact = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.agency_name


class AgencyMessage(models.Model):
    agency = models.ForeignKey(UserAgency, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='user_agency')
    open_space = models.ForeignKey(OpenSpace, on_delete=models.CASCADE, related_name='user_agency')
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.agency.agency_name

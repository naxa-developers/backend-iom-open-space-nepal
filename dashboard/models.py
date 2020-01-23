from django.db import models
from django.contrib.auth.models import User
from core.models import Province, District, Municipality


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

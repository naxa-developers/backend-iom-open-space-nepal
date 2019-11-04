from django.db import models
from django.conf import settings
from django.contrib.gis.db.models import PointField, PolygonField

# Create your models here.


class Slider(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='slider', blank=True, null=True)

    def __str__(self):
        return self.title


class Province(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey('Province', related_name='district',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=50)
    district = models.ForeignKey('District', related_name='municipality',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ward(models.Model):
    ward_num = models.IntegerField()
    municipality = models.ForeignKey('Municipality',
                                     related_name='ward',
                                     on_delete=models.CASCADE)

    def __str__(self):
        return self.ward_num


class SuggestedUse(models.Model):
    name = models.CharField(max_length=100)
    open_space = models.ForeignKey('OpenSpace', related_name='suggested_use',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=100)
    open_space = models.ForeignKey('OpenSpace', related_name='services',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.TextField()
    ans = models.BooleanField(default=True)
    open_space = models.ForeignKey('OpenSpace', related_name='questions',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class OpenSpace(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    current_land_use = models.TextField(blank=True, null=True)
    catchment_area = models.CharField(max_length=200, blank=True, null=True)
    ownership = models.CharField(max_length=100, blank=True, null=True)
    elevation = models.DecimalField(max_digits=15, decimal_places=10)
    access_to_site = models.CharField(max_length=100)
    special_feature = models.TextField(blank=True, null=True)

    address = models.CharField(max_length=200, blank=True, null=True)
    province = models.ForeignKey('Province', related_name='open_space',
                                 on_delete=models.SET_NULL, blank=True,
                                 null=True)
    district = models.ForeignKey('District', related_name='open_space',
                                 on_delete=models.SET_NULL, blank=True,
                                 null=True)
    municipality = models.ForeignKey('Municipality', related_name='open_space',
                                     on_delete=models.SET_NULL, blank=True,
                                     null=True)
    ward = models.ForeignKey('Ward', related_name='open_space',
                             on_delete=models.SET_NULL, blank=True, null=True)
    capacity = models.BigIntegerField(blank=True, null=True)
    total_area = models.IntegerField(blank=True, null=True)
    usable_area = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='space',
                              blank=True, null=True)
    maps = models.ImageField(upload_to='maps', blank=True, null=True)
    location = PointField(geography=True, srid=4326, blank=True, null=True)
    polygon = PolygonField(null=True, blank=True)

    @property
    def latitude(self):
        if self.location:
            return self.location.y

    @property
    def longitude(self):
        if self.location:
            return self.location.x

    def __str__(self):
        return self.title


class Report(models.Model):
    URGENCY_CHOICES = (
        (0, 'High'),
        (1, 'Medium'),
        (2, 'Low')
    )

    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Replied')
    )

    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    urgency = models.IntegerField(choices=URGENCY_CHOICES, default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    open_space = models.ForeignKey('OpenSpace', on_delete=models.CASCADE,
                                   related_name='report')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="reported_by",
                                    on_delete=models.SET_NULL,
                                    blank=True, null=True)
    image = models.ImageField(upload_to='space',
                              blank=True, null=True)
    location = PointField(geography=True, srid=4326, blank=True, null=True)

    @property
    def latitude(self):
        if self.location:
            return self.location.y

    @property
    def longitude(self):
        if self.location:
            return self.location.x

    def __str__(self):
        return self.title


# class Resource(models.Model):
#     audio = models.FileField(upload_to='audio', null=True, blank=True)
#     video = models.FileField(upload_to='video', null=True, blank=True)
#     animation = models.FileField(upload_to='animation', null=True, blank=True)










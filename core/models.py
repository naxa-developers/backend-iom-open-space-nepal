from django.db import models
from django.conf import settings
from django.contrib.gis.db.models import PointField, MultiPolygonField


# Create your models here.


class Slider(models.Model):
    title = models.CharField(max_length=100)
    title_nep = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='slider', blank=True, null=True)

    def __str__(self):
        return self.title


class Province(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(null=True, blank=True)
    province = models.ForeignKey('Province', related_name='district',
                                 on_delete=models.CASCADE)
    boundary = MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=50)
    district = models.ForeignKey('District', related_name='municipality',
                                 on_delete=models.CASCADE)
    hlcit_code = models.CharField(max_length=100, blank=True, null=True)
    boundary = MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


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


class QuestionList(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title


class QuestionsData(models.Model):
    question = models.ForeignKey('QuestionList', on_delete=models.CASCADE,
                                 blank=True, null=True)
    ans = models.BooleanField(default=True)
    open_space = models.ForeignKey('OpenSpace', on_delete=models.CASCADE,
                                   blank=True, null=True,
                                   related_name='question_data')

    def __str__(self):
        return self.question.title


class Gallery(models.Model):
    image = models.ImageField(upload_to='open_image',
                              blank=True, null=True)
    maps = models.ImageField(upload_to='open_maps',
                             blank=True, null=True)
    open_space = models.ForeignKey('OpenSpace', on_delete=models.CASCADE,
                                   blank=True, null=True,
                                   related_name='gallery')


class OpenSpace(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    current_land_use = models.TextField(blank=True, null=True)
    catchment_area = models.CharField(max_length=200, blank=True, null=True)
    ownership = models.CharField(max_length=100, blank=True, null=True)
    elevation = models.DecimalField(max_digits=15, decimal_places=10,
                                    null=True, blank=True)
    access_to_site = models.CharField(max_length=100, null=True, blank=True)
    special_feature = models.TextField(blank=True, null=True)

    address = models.CharField(max_length=200, blank=True, null=True)
    province = models.ForeignKey('Province', related_name='open_province',
                                 on_delete=models.SET_NULL, blank=True,
                                 null=True)
    district = models.ForeignKey('District', related_name='district',
                                 on_delete=models.SET_NULL, blank=True,
                                 null=True)
    municipality = models.ForeignKey('Municipality',
                                     related_name='municipality',
                                     on_delete=models.SET_NULL,
                                     blank=True, null=True)
    ward = models.IntegerField(blank=True, null=True)
    capacity = models.DecimalField(max_digits=20, decimal_places=3,
                                   blank=True, null=True)
    total_area = models.DecimalField(max_digits=20, decimal_places=3,
                                     blank=True, null=True)
    usable_area = models.DecimalField(max_digits=20, decimal_places=3,
                                      blank=True, null=True)
    image = models.ImageField(upload_to='space',
                              blank=True, null=True)
    location = PointField(geography=True, srid=4326, blank=True, null=True)
    polygons = MultiPolygonField(null=True, blank=True)

    @property
    def latitude(self):
        if self.location:
            return self.location.y

    @property
    def longitude(self):
        if self.location:
            return self.location.x

    @property
    def centroid(self):
        center = []
        long = self.polygons.centroid.x
        lat = self.polygons.centroid.y
        center.append(long)
        center.append(lat)
        return center

    def __str__(self):
        return self.title


class Report(models.Model):
    URGENCY_CHOICES = (
        ('high', 'HIGH'),
        ('medium', 'MEDIUM'),
        ('low', 'LOW')
    )

    STATUS_CHOICES = (
        ('pending', 'PENDING'),
        ('replied', 'REPLIED')
    )

    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True,  null=True, blank=True)
    urgency = models.CharField(choices=URGENCY_CHOICES, max_length=15, default='high')
    status = models.CharField(choices=STATUS_CHOICES, max_length=15, default='pending')
    open_space = models.ForeignKey('OpenSpace', on_delete=models.CASCADE,
                                   related_name='report', blank=True, null=True)
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
        return self.name


class CreateOpenSpace(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='identify_open_space')


class NearbyAmenities(models.Model):
    title = models.CharField(max_length=100)
    open_space = models.ForeignKey('OpenSpace', on_delete=models.CASCADE,
                                   related_name='amenities')

    def __str__(self):
        return self.title


class EducationFacility(models.Model):
    name = models.CharField(max_length=100)
    amenity = models.ForeignKey('NearbyAmenities', on_delete=models.CASCADE,
                                related_name='education_facility')
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
        return self.name


class HealthFacility(models.Model):
    name = models.CharField(max_length=100)
    amenity = models.ForeignKey('NearbyAmenities', on_delete=models.CASCADE,
                                related_name='health_facility')
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
        return self.name


class Resource(models.Model):
    CATEGORY_CHOICES = (
        (0, 'Plans and Policies'),
        (1, 'Research'),
        (2, 'Multimedia')
    )

    DOCUMENT_TYPE_CHOICES = (
        (0, 'publication'),
        (1, 'audio'),
        (2, 'video')

    )
    title = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='resource_image',
                              null=True, blank=True)
    audio = models.FileField(upload_to='audio', null=True, blank=True)
    video = models.FileField(upload_to='video', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    publication = models.FileField(upload_to='publication', null=True,
                                   blank=True)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=0)
    document_type = models.IntegerField(choices=DOCUMENT_TYPE_CHOICES,
                                        default=0)

    def __str__(self):
        return self.title


class AvailableFacility(models.Model):
    TYPE_CHOICES = (
        (1, 'Health Facility'),
        (2, 'Education Facility'),
        (3, 'Security Force'),
        (4, 'Place Of Worship'),
        (5, 'Financial Institution')
    )
    EDUCATION_TYPE_CHOICES = (
        (1, 'School'),
        (2, 'College'),
        (3, 'Kinder Garden'),
        (4, 'Driving School')
    )

    FINANCIAL_INSTITUTION_CHOICES = (
        (1, 'bank'),
        (2, 'atm'),
        (3, 'bureau_de_change')
    )

    HEALTH_FACILITY_CHOICES = (
        (1, 'Hospital'),
        (2, 'Veterinary'),
        (3, 'Clinic'),
        (4, 'Dentist'),
        (5, 'Pharmacy'),
        (6, 'Health Post'),
        (7, 'Social Facility'),
        (8, 'Doctors')
    )

    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=TYPE_CHOICES, default=0)
    address = models.TextField(null=True, blank=True)
    location = PointField(geography=True, srid=4326, blank=True, null=True)
    province = models.ForeignKey('Province', related_name='facility_province',
                                 on_delete=models.SET_NULL, blank=True,
                                 null=True)
    district = models.ForeignKey('District', related_name='facility_district',
                                 on_delete=models.SET_NULL, blank=True,
                                 null=True)
    email = models.EmailField(blank=True,null=True)
    municipality = models.ForeignKey('Municipality',
                                     related_name='facility_municipality',
                                     on_delete=models.SET_NULL,
                                     blank=True, null=True)
    opening_hours = models.CharField(max_length=200, null=True, blank=True)
    education_type = models.IntegerField(choices=EDUCATION_TYPE_CHOICES,
                                         null=True, blank=True)
    financial_type = models.IntegerField(choices=FINANCIAL_INSTITUTION_CHOICES,
                                         null=True, blank=True)
    health_type = models.IntegerField(choices=HEALTH_FACILITY_CHOICES,
                                      null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)

    @property
    def latitude(self):
        if self.location:
            return self.location.y

    @property
    def longitude(self):
        if self.location:
            return self.location.x

    def __str__(self):
        return self.name

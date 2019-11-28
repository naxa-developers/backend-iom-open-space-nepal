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
    boundary = MultiPolygonField(null=True, blank=True)

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
    province = models.ForeignKey('Province', related_name='municipality',
                                 on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey('District', related_name='municipality',
                                 on_delete=models.CASCADE)
    hlcit_code = models.CharField(max_length=100, blank=True, null=True)
    boundary = MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


class SuggestedUse(models.Model):
    name = models.CharField(max_length=500)
    open_space = models.ForeignKey('OpenSpace', related_name='suggested_use',
                                   on_delete=models.CASCADE)
    icon = models.FileField(upload_to='suggest', blank=True, null=True)

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    open_space = models.ForeignKey('OpenSpace', related_name='services',
                                   on_delete=models.CASCADE)
    icon = models.FileField(upload_to='service', blank=True, null=True)

    def __str__(self):
        return self.name


class QuestionList(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title


class QuestionsData(models.Model):
    question = models.ForeignKey('QuestionList', on_delete=models.CASCADE,
                                 blank=True, null=True)
    ans = models.CharField(blank=True, null=True, max_length=100)
    open_space = models.ForeignKey('OpenSpace', on_delete=models.CASCADE,
                                   blank=True, null=True,
                                   related_name='question_data')

    def __str__(self):
        return self.question.title


class Gallery(models.Model):
    TYPE_CHOICES = (
        ('map', 'Map'),
        ('image', 'Image')
    )
    image = models.ImageField(upload_to='open_image',
                              blank=True, null=True)
    type = models.CharField(choices=TYPE_CHOICES, max_length=15, blank=True, null=True)
    open_space = models.ForeignKey('OpenSpace', on_delete=models.CASCADE,
                                   blank=True, null=True,
                                   related_name='gallery')


class OpenSpace(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    issue = models.TextField(blank=True, null=True)
    current_land_use = models.TextField(blank=True, null=True)
    catchment_area = models.CharField(max_length=500, blank=True, null=True)
    ownership = models.CharField(max_length=500, blank=True, null=True)
    elevation = models.DecimalField(max_digits=15, decimal_places=10,
                                    null=True, blank=True)
    access_to_site = models.CharField(max_length=500, null=True, blank=True)
    special_feature = models.TextField(blank=True, null=True)

    address = models.CharField(max_length=500, blank=True, null=True)
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

    def __str__(self):
        return self.title


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
        ('health facility', 'Health Facility'),
        ('education facility', 'Education Facility'),
        ('security force', 'Security Force'),
        ('place of worship', 'Place Of Worship'),
        ('financial institution', 'Financial Institution')
    )
    EDUCATION_TYPE_CHOICES = (
        ('school', 'School'),
        ('college', 'College'),
        ('kindergarten', 'Kinder Garten'),
        ('driving_school', 'Driving School'),
        ('library', 'Library')
    )

    OPERATOR_TYPE = (
        ('private', 'Private'),
        ('community', 'Community'),
        ('government', 'Government'),
        ('public', 'Public')
    )

    FINANCIAL_INSTITUTION_CHOICES = (
        ('bank', 'bank'),
        ('atm', 'atm'),
        ('bureau_de_change', 'bureau_de_change')
    )

    HEALTH_FACILITY_CHOICES = (
        ('hospital', 'Hospital'),
        ('veterinary', 'Veterinary'),
        ('clinic', 'Clinic'),
        ('dentist', 'Dentist'),
        ('pharmacy', 'Pharmacy'),
        ('health post', 'Health Post'),
        ('social facility', 'Social Facility'),
        ('doctors', 'Doctors')
    )

    BANK_TYPE = (
        ('development', 'Development'),
        ('commercial', 'Commercial'),
        ('finance companies', 'Finance Companies'),
        ('micro finance', 'Micro Finance'),
        ('co-operative', 'Co-operative')
    )

    name = models.CharField(max_length=100)
    type = models.CharField(choices=TYPE_CHOICES, max_length=30,
                            null=True, blank=True)
    operator_type = models.CharField(choices=OPERATOR_TYPE,
                                     max_length=30, null=True, blank=True)
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
    education_type = models.CharField(choices=EDUCATION_TYPE_CHOICES,
                                      max_length=30, null=True, blank=True)
    financial_type = models.CharField(choices=FINANCIAL_INSTITUTION_CHOICES,
                                      max_length=30, null=True, blank=True)
    bank_type = models.CharField(choices=BANK_TYPE, max_length=30,
                                 null=True, blank=True)
    health_type = models.CharField(choices=HEALTH_FACILITY_CHOICES,
                                   max_length=30, null=True, blank=True)

    phone_number = models.CharField(max_length=300, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    bank_network = models.CharField(max_length=500, blank=True, null=True)
    icon = models.FileField(upload_to='facility', blank=True, null=True)
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


class ProvinceDummy(models.Model):
    province_id = models.IntegerField(blank=True, null=True)
    geom_char = models.TextField(blank=True, null=True)


from django.db import models
from django.conf import settings
from django.contrib.gis.db.models import PointField, MultiPolygonField
from decimal import Decimal
import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


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

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(null=True, blank=True)
    province = models.ForeignKey('Province', related_name='district',
                                 on_delete=models.CASCADE)
    boundary = MultiPolygonField(null=True, blank=True)

    class Meta:
        ordering = ['name']

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

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class SuggestedUseList(models.Model):
    name = models.CharField(max_length=1000)
    icon = models.FileField(upload_to='suggest', blank=True, null=True)

    def __str__(self):
        return self.name


class SuggestedUseData(models.Model):
    open_space = models.ForeignKey('OpenSpace', related_name='suggested_use',
                                   on_delete=models.CASCADE)
    suggested_use = models.ForeignKey('SuggestedUseList', related_name='suggested_use',
                                      on_delete=models.CASCADE)

    def __str__(self):
        return self.suggested_use.name


class ServiceList(models.Model):
    name = models.CharField(max_length=500)
    icon = models.FileField(upload_to='service', blank=True, null=True)

    def __str__(self):
        return self.name


class ServiceData(models.Model):
    Available = (
        ('yes', 'YES'),
        ('no', 'NO')
    )
    is_available = models.CharField(choices=Available, max_length=15, default='no', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    open_space = models.ForeignKey('OpenSpace', related_name='services',
                                   on_delete=models.CASCADE)
    service = models.ForeignKey('ServiceList', related_name='services', on_delete=models.CASCADE)

    def __str__(self):
        return self.service.name


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
    thumbnail = models.ImageField(upload_to='thumbs', editable=False, null=True, blank=True)
    gallery_update = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Gallery, self).save(*args, **kwargs)

    def make_thumbnail(self):

        image = Image.open(self.image)
        image.thumbnail((600, 400), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


class OpenSpace(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    issue = models.CharField(max_length=1000, blank=True, null=True)
    current_land_use = models.TextField(blank=True, null=True)
    catchment_area = models.CharField(max_length=1000, blank=True, null=True)
    ownership = models.CharField(max_length=1000, blank=True, null=True)
    elevation = models.CharField(max_length=1000,
                                 null=True, blank=True)
    access_to_site = models.CharField(max_length=1000, null=True, blank=True)
    special_feature = models.TextField(blank=True, null=True)

    address = models.CharField(max_length=1000, blank=True, null=True)
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
    ward = models.CharField(max_length=1000, blank=True, null=True)
    capacity = models.FloatField(blank=True, null=True, default=Decimal('0.0000'))
    # capacity = models.CharField(max_length=100, blank=True, null=True)
    total_area = models.FloatField(blank=True, null=True, default=0)
    # total_area = models.CharField(max_length=100,
    #                                  blank=True, null=True)
    usable_area = models.CharField(max_length=1000, blank=True, null=True, default=0)
    image = models.ImageField(upload_to='space', blank=True, null=True)
    location = PointField(geography=True, srid=4326, blank=True, null=True)
    polygons = MultiPolygonField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbs', editable=False, null=True, blank=True)
    geoserver_url = models.CharField(max_length=500, blank=True, null=True)
    layername = models.CharField(max_length=500, blank=True, null=True)
    workspace = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['title']

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

    def make_thumbnail(self):
        if self.image:
            image = Image.open(self.image)
            image.thumbnail((600, 400), Image.ANTIALIAS)

            thumb_name, thumb_extension = os.path.splitext(self.image.name)
            thumb_extension = thumb_extension.lower()

            thumb_filename = thumb_name + '_thumb' + thumb_extension

            if thumb_extension in ['.jpg', '.jpeg']:
                FTYPE = 'JPEG'
            elif thumb_extension == '.gif':
                FTYPE = 'GIF'
            elif thumb_extension == '.png':
                FTYPE = 'PNG'
            else:
                return False  # Unrecognized file type

            # Save thumbnail to in-memory file as StringIO
            temp_thumb = BytesIO()
            image.save(temp_thumb, FTYPE)
            temp_thumb.seek(0)

            # set save=False, otherwise it will run in an infinite loop
            self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()
        else:
            pass
        return True

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')
        if self.ward:
            self.address = 'Ward' + ' ' + str(self.ward) + ',' + self.municipality.name
        else:
            if self.ward:
                self.address = self.municipality.name

        super(OpenSpace, self).save(*args, **kwargs)

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
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    urgency = models.CharField(choices=URGENCY_CHOICES, max_length=15, default='high')
    status = models.CharField(choices=STATUS_CHOICES, max_length=15, default='pending')
    open_space = models.ForeignKey('OpenSpace', on_delete=models.CASCADE,
                                   related_name='report', blank=True, null=True)
    reported_by = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='space',
                              blank=True, null=True)
    reply = models.TextField(null=True, blank=True)
    token = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.name = self.open_space.title
        super(Report, self).save(*args, **kwargs)


class CreateOpenSpace(models.Model):
    title = models.CharField(max_length=100)
    title_nep = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='identify_open_space')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class CreateOpenSpacePoints(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    title_nep = models.CharField(max_length=500, blank=True, null=True)
    steps = models.ForeignKey('CreateOpenSpace', on_delete=models.CASCADE, related_name='create_open')


class ResourceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ResourceDocumentType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Resource(models.Model):
    title = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='resource_image',
                              null=True, blank=True)
    audio = models.FileField(upload_to='audio', null=True, blank=True)
    # video = models.FileField(upload_to='video', null=True, blank=True)
    video = models.CharField(max_length=300, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    publication = models.FileField(upload_to='publication', null=True,
                                   blank=True)
    category = models.ForeignKey('ResourceCategory', on_delete=models.CASCADE, related_name='resource')
    document_type = models.ForeignKey('ResourceDocumentType', on_delete=models.CASCADE, related_name='resource')

    def __str__(self):
        return self.title


class AvailableType(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class AvailableSubType(models.Model):
    title = models.CharField(max_length=100)
    type = models.ForeignKey('AvailableType', on_delete=models.CASCADE, related_name='available_sub_type',
                             blank=True, null=True)

    def __str__(self):
        return self.title


class AvailableFacility(models.Model):
    # TYPE_CHOICES = (
    #     ('health facility', 'Health Facility'),
    #     ('education facility', 'Education Facility'),
    #     ('security force', 'Security Force'),
    #     ('place of worship', 'Place Of Worship'),
    #     ('financial institution', 'Financial Institution'),
    #     ('helipad', 'Helipad'),
    #     ('fire', 'Fire')
    # )
    # EDUCATION_TYPE_CHOICES = (
    #     ('school', 'School'),
    #     ('college', 'College'),
    #     ('kindergarten', 'Kinder Garten'),
    #     ('higher_secondary', 'Higher Secondary'),
    #     ('lower_secondary', 'Lower Secondary'),
    #     ('driving_school', 'Driving School'),
    #     ('primary', 'Primary'),
    #     ('secondary', 'Secondary'),
    #     ('library', 'Library')
    # )

    OPERATOR_TYPE = (
        ('private', 'Private'),
        ('community', 'Community'),
        ('government', 'Government'),
        ('public', 'Public')
    )

    # FINANCIAL_INSTITUTION_CHOICES = (
    #     ('bank', 'bank'),
    #     ('atm', 'atm'),
    #     ('bureau_de_change', 'bureau_de_change')
    # )

    # HEALTH_FACILITY_CHOICES = (
    #     ('hospital', 'Hospital'),
    #     ('veterinary', 'Veterinary'),
    #     ('clinic', 'Clinic'),
    #     ('dentist', 'Dentist'),
    #     ('pharmacy', 'Pharmacy'),
    #     ('health post', 'Health Post'),
    #     ('social facility', 'Social Facility'),
    #     ('doctors', 'Doctors')
    # )

    BANK_TYPE = (
        ('development', 'Development'),
        ('commercial', 'Commercial'),
        ('finance companies', 'Finance Companies'),
        ('micro finance', 'Micro Finance'),
        ('co-operative', 'Co-operative')
    )

    name = models.CharField(max_length=1000, null=True, blank=True)
    # type = models.CharField(choices=TYPE_CHOICES, max_length=30,
    #                         null=True, blank=True)
    available_type = models.ForeignKey('AvailableType', on_delete=models.CASCADE, related_name='facility_avai_type',
                                       blank=True, null=True)
    available_sub_type = models.ForeignKey('AvailableSubType', on_delete=models.CASCADE,
                                           related_name='facility_avai_sub_type', blank=True, null=True)
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
    email = models.EmailField(blank=True, null=True)
    municipality = models.ForeignKey('Municipality',
                                     related_name='facility_municipality',
                                     on_delete=models.SET_NULL,
                                     blank=True, null=True)
    ward_no = models.CharField(max_length=20, null=True, blank=True)
    opening_hours = models.CharField(max_length=200, null=True, blank=True)
    # education_type = models.CharField(choices=EDUCATION_TYPE_CHOICES,
    #                                   max_length=30, null=True, blank=True)
    # financial_type = models.CharField(choices=FINANCIAL_INSTITUTION_CHOICES,
    #                                   max_length=30, null=True, blank=True)
    bank_type = models.CharField(choices=BANK_TYPE, max_length=30,
                                 null=True, blank=True)
    # health_type = models.CharField(choices=HEALTH_FACILITY_CHOICES,
    #                                max_length=30, null=True, blank=True)

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

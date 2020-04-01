from django.db import models

# Create your models here.


class Header(models.Model):
    title1 = models.TextField(blank=True, null=True)
    title2 = models.TextField(blank=True, null=True)
    title3 = models.TextField(blank=True, null=True)
    title_nep1 = models.TextField(blank=True, null=True)
    title_nep2 = models.TextField(blank=True, null=True)
    title_nep3 = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title1


class OpenSpaceDef(models.Model):
    title = models.TextField(blank=True, null=True)
    title_nep = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)
    video = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class OpenSpaceIde(models.Model):
    title = models.TextField(blank=True, null=True)
    title_nep = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    title = models.CharField(max_length=300)
    title_nep = models.CharField(max_length=300,null=True, blank=True)
    location = models.CharField(max_length=300, null=True, blank=True)
    location_nep = models.CharField(max_length=300, null=True, blank=True)
    num1 = models.CharField(max_length=14, null=True, blank=True)
    num1_nep = models.CharField(max_length=14, null=True, blank=True)
    num2 = models.CharField(max_length=14, null=True, blank=True)
    num2_nep = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email_nep = models.EmailField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    description_nep = models.TextField(null=True, blank=True)


class OpenSpaceApp(models.Model):
    title = models.CharField(max_length=100)
    title_nep = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="app")
    icon = models.FileField(upload_to="icon")
    description = models.TextField(null=True, blank=True)
    description_nep = models.TextField(null=True, blank=True)


#about page models

class AboutHeader(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    title_nep = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title


class WhyMapOpenIcon(models.Model):
    icon = models.FileField(upload_to="icon")
    icon_class = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)


class WhyMapOpenSpace(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    title_nep = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)


class CriteriaType(models.Model):
    title = models.CharField(max_length=300, blank=True, null=True)
    title_nep = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title


class CriteriaDescription(models.Model):
    type = models.ForeignKey('CriteriaType', on_delete=models.CASCADE, related_name='criteria_description')
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class OpenSpaceCriteria(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    title_nep = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


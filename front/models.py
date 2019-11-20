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
        return self.title


class OpenSpaceDef(models.Model):
    title = models.TextField(blank=True, null=True)
    title_nep = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)
    video = models.TextField(blank=True,null=True)

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
    location = models.CharField(max_length=300, null=True, blank=True)
    num1 = models.CharField(max_length=14)
    num2 = models.CharField(max_length=14)
    email = models.EmailField()
    description = models.TextField()


class OpenSpaceApp(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="app")
    icon = models.ImageField(upload_to="icon")
    description = models.TextField()

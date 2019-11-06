from django.db import models

# Create your models here.


class Header(models.Model):
    title = models.TextField(blank=True, null=True)
    title_nep = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title



class OpenSpaceDef(models.Model):
    title = models.TextField(blank=True, null=True)
    title_nep = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='open_space_def',
                             blank=True, null=True)

    def __str__(self):
        return self.title


class OpenSpaceIde(models.Model):
    title = models.TextField(blank=True, null=True)
    title_nep = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_nep = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

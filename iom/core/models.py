from django.db import models

# Create your models here.


class Slider(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='slider', blank=True, null=True)

    def __str__(self):
        return self.title

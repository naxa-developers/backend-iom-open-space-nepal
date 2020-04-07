from django.core.management.base import BaseCommand

import pandas as pd

from core.models import AvailableFacility, OpenSpace, Municipality

from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def handle(self, *args, **kwargs):
        objects = Municipality.objects.all()
        for i in objects:
            province = i.district.province
            i.province = province
            i.save()
            print('Province successfully updated')






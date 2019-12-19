from django.core.management.base import BaseCommand

import pandas as pd

from core.models import AvailableFacility, OpenSpace

from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def handle(self, *args, **kwargs):
        objects = OpenSpace.objects.all()
        ids = []
        for i in objects:
            open = OpenSpace.objects.get(id=i.id)
            open.save()
            print('successully update')






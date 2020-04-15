from django.core.management.base import BaseCommand

import pandas as pd

from core.models import ServiceList

from django.contrib.gis.geos import Point

services = [
    'WASH_Facility',
    'Internet',
    'Boundary Wall',
    'Electricity Line',
    'Trees & Vegetation'
]


class Command(BaseCommand):
    help = 'Create Question List'

    def handle(self, *args, **kwargs):
        for i in services:
            service = ServiceList.objects.create(name=i)
            print(i, 'Successfully Created Service List')









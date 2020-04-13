from django.core.management.base import BaseCommand

import pandas as pd

from core.models import SuggestedUseList

from django.contrib.gis.geos import Point

suggested = [
    'Assembly Point for Displaced',
    'Civil Military Coordination Center',
    'Dead Body Management/Morgue',
    'Debris Collection',
    'Distribution Area',
    'Helipad',
    'Humanitarian Camp',
    'Humanitarian Coordination Area',
    'Logistics',
    'Medical Assistance Area',
    'Military Installation',
    'Multiple Use Camp',
    'Portable Water',
    'Settlement Camp',
    'Telecommunication',
    'Vulnerable Population Assistance Area',
    'Warehouse'
]


class Command(BaseCommand):
    help = 'Create Suggested Use List'

    def handle(self, *args, **kwargs):
        for i in suggested:
            suggested_use = SuggestedUseList.objects.create(name=i)
            print(i, 'Successfully Created Suggested Use List')









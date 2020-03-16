from django.core.management.base import BaseCommand

import pandas as pd

from core.models import AvailableFacility, OpenSpace, AvailableType, AvailableSubType

from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = 'Successfully change the type and the subtypes'

    def handle(self, *args, **kwargs):
        type_choices = ['health facility', 'education facility', 'security force', 'place of worship',
                        'financial institution', 'helipad', 'fire']

        edu_choice = ['school', 'college', 'kindergarten', 'higher_secondary',
                      'lower_secondary', 'driving_school', 'primary', 'secondary', 'library']

        financial_choice = ['bank', 'atm', 'bureau_de_change']

        health_choice = ['hospital', 'veterinary', 'clinic', 'dentist', 'pharmacy',
                         'health post', 'social facility', 'doctors']

        for each in type_choices:
            created = AvailableType.objects.create(title=each)

        financial_type = AvailableType.objects.get(title='financial institution')
        education_type = AvailableType.objects.get(title='education facility')
        health_type = AvailableType.objects.get(title='health facility')

        for title in financial_choice:
            sub_type = AvailableSubType.objects.create(title=title, type=financial_type)

        for title in edu_choice:
            sub_type = AvailableSubType.objects.create(title=title, type=education_type)

        for title in health_choice:
            sub_type = AvailableSubType.objects.create(title=title, type=health_type)









from django.core.management.base import BaseCommand

import pandas as pd

from core.models import AvailableFacility, OpenSpace, AvailableType, AvailableSubType

from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = 'Successfully change the type and the subtypes'

    def handle(self, *args, **kwargs):
        facilities = AvailableFacility.objects.all()

        for facility in facilities:
            available_type = None
            sub_type = []

            if facility.type == 'health facility':
                available_type = AvailableType.objects.get(title='health facility')
                health_type = facility.health_type
                sub_type = AvailableSubType.objects.filter(title=health_type)
                pass

            if facility.type == 'education facility':
                available_type = AvailableType.objects.get(title='education facility')
                education_type = facility.education_type
                sub_type = AvailableSubType.objects.filter(title=education_type)
                pass

            if facility.type == 'security force':
                available_type = AvailableType.objects.get(title='security force')
                pass

            if facility.type == 'place of worship':
                available_type = AvailableType.objects.get(title='place of worship')
                pass

            if facility.type == 'financial institution':
                available_type = AvailableType.objects.get(title='financial institution')
                financial_type = facility.financial_type
                sub_type = AvailableSubType.objects.filter(title=financial_type)
                pass

            if facility.type == 'helipad':
                available_type = AvailableType.objects.get(title='helipad')
                pass

            if facility.type == 'fire':
                available_type = AvailableType.objects.get(title='fire')
                pass

            facility.available_type = available_type
            if not sub_type:
                pass
            else:
                facility.available_sub_type = sub_type[0]
            facility.save()










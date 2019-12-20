from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Province, District, OpenSpace, Municipality, SuggestedUseData, SuggestedUseList, ServiceList, \
    ServiceData

from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_csv(path, encoding='unicode_escape').fillna('')
        upper_range = len(df)

        for row in range(0, upper_range):
            use = df['Suggested Use'][row]
            if use != '':
                try:
                    if use != '':
                        suggested_uses = use.split(',')
                        print(suggested_uses)

                except Exception as e:
                    print(e)

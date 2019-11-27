from django.core.management.base import BaseCommand

import pandas as pd

from core.models import OpenSpace

from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_csv(path)
        upper_range = len(df)

        print("Wait Data is being Loaded")

        for row in range(0, upper_range):
            try:
                open_space = OpenSpace.objects.filter(title=df['Name'][row]).update(
                    elevation=df['Elevation'][row], ward=df['Ward'][row])

                print("data is successfully updated")

            except:
                print('could not update data')

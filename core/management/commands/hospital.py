from django.core.management.base import BaseCommand

import pandas as pd

from core.models import AvailableFacility

from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_csv(path).fillna('')
        upper_range = len(df)

        print("Wait Data is being Loaded")

        for row in range(0, upper_range):

            try:
                # print(float(df['Latitude'][row]))
                # print(float(df['Longitude'][row]))
                # print(Point(float(df['Latitude'][row]), float(df['Longitude'][row])))

                q=AvailableFacility.objects.create(
                    name=df['name'][row],
                    type='health facility',
                    health_type='hospital',
                    operator_type=df['operator_t'][row],
                    location=Point(float(df['Log'][row]), float(df['Lat'][row])),
                )
                print(row, q.name)

            except Exception as e:
                print(e)


from django.core.management.base import BaseCommand

import pandas as pd

from core.models import OpenSpace, Province, District, Municipality
from django.contrib.gis.geos import GEOSGeometry

from django.contrib.gis.geos import GEOSGeometry


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
                usable_area = df['Usable Open Space Area'][row]
                total_area = df['Total Area'][row]
                capacity = df['Capacity'][row]
                open_space = OpenSpace.objects.filter(title=df['Name'][row]).update(capacity=capacity,
                                                                                    total_area=total_area,
                                                                                    usable_area=usable_area
                                                                                    )

            except Exception as e:
                print(e)
                print(row, df['Name'][row])

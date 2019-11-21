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
        df = pd.read_csv(path)
        upper_range = len(df)

        print("Wait Data is being Loaded")

        try:
            facility = [
                AvailableFacility(
                    name=df['name'][row],
                    operator_type=df['operator_type'][row],
                    opening_hours=df['opening_hours'][row],
                    phone_number=df['phone_number'][row],
                    email=df['email_address'][row],
                    comments=df['comments'][row],
                    type='education facility',
                    education_type=df['type'][row],
                    location=Point(float(df['long'][row]), df['lat'][row])

                ) for row in range(0, upper_range)

            ]

            available_data = AvailableFacility.objects.bulk_create(facility)

            if available_data:
                self.stdout.write('Successfully  updated data ..')

        except Exception as e:
            print(e)


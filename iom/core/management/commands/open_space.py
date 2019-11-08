from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Province, District, OpenSpace

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

        try:
            open_space = [
                OpenSpace(
                    # province=Province.objects.get(
                    #     province_code=(df['Province_id'][row])),
                    #
                    # district=District.objects.get(
                    #     district_code=(df['District_id'][row])),
                    #
                    # name=(df['Name'][row]).capitalize().strip(),
                    #
                    # gn_type_en=(df['Type_en'][row]).capitalize().strip(),
                    #
                    # gn_type_np=(df['Type'][row]).capitalize().strip(),
                    title=df['name'][row],
                    polygons=GEOSGeometry(df['geom'][row]),
                    # p_code=df['ADMIN2P_CODE'][row],

                ) for row in range(0, upper_range)

            ]

            open_space_data = OpenSpace.objects.bulk_create(open_space)

            if open_space_data:
                self.stdout.write('Successfully  updated data ..')

        except Exception as e:
            print(e)


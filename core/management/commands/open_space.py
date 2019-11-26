from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Province, District, OpenSpace, Municipality, SuggestedUse

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
            data = []
            # print(df['Suggested Use'][row])
            data.append(df['Suggested Use'][row])
            print(data)

        for row in range(0, upper_range)
            try:
                open_space = OpenSpace.objects.create(
                    province=Province.objects.get(
                        province_code=(df['Province'][row])),
                    #
                    district=District.objects.get(
                        district_code=(df['District'][row])),

                    municipality=Municipality.objects.get(
                        hlcit_code=(df['Municipality'][row])),
                    #
                    # name=(df['Name'][row]).capitalize().strip(),
                    #
                    # gn_type_en=(df['Type_en'][row]).capitalize().strip(),
                    #
                    # gn_type_np=(df['Type'][row]).capitalize().strip(),
                    title=df['name'][row],
                    current_land_use=df['Current Land Use'][row],
                    total_area=df['Total Area'][row],
                    usable_area=df['Usable Open Space Area'][row],
                    capacity=df['Capacity'][row],
                    catchment_area=df['Catchment Area'][row],
                    access_to_site=df['Access to Site'][row],
                    special_feature=df['Special features'][row],
                    issue=df['Issues'][row],
                    ownership=df['Ownership'][row],
                    polygons=GEOSGeometry(df['geom'][row]),
                )

                data = []
                data.append(df['Suggested Use'][row])
                for i in data:
                    SuggestedUse.objects.create(name=i, open_space=open_space.id)

                open_space_data = OpenSpace.objects.bulk_create(open_space)

                if open_space_data:
                    self.stdout.write('Successfully  updated data ..')

            except Exception as e:
                print(e)

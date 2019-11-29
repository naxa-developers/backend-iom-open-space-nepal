from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Province, District, OpenSpace, Municipality, SuggestedUse, Services

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
                open_space = OpenSpace.objects.create(
                    province=Province.objects.get(
                        code=(df['Province'][row])),
                    #
                    district=District.objects.get(
                        code=(df['District'][row])),

                    municipality=Municipality.objects.get(
                        hlcit_code=(df['Municipality'][row])),
                    # #
                    # name=(df['Name'][row]).capitalize().strip(),
                    # #
                    # # gn_type_en=(df['Type_en'][row]).capitalize().strip(),
                    # #
                    # # gn_type_np=(df['Type'][row]).capitalize().strip(),
                    title=df['Name'][row],
                    current_land_use=df['Current Land Use'][row],
                    total_area=float((df['Total Area'][row]).replace(',', '')),
                    usable_area=float((df['Usable Open Space Area'][row]).replace(',', '')),
                    capacity=float((df['Capacity'][row]).replace(',', '')),
                    catchment_area=df['Catchment Area'][row],
                    access_to_site=df['Access to Site'][row],
                    special_feature=df['Special features'][row],
                    issue=df['Issues'][row],
                    ward=df['Ward'][row],
                    elevation=df['Elevation'][row],
                    # address=df['Address'][row],
                    ownership=df['Ownership'][row],
                    polygons=GEOSGeometry(df['geom'][row]),
                )

                use = df['Suggested Use'][row]
                suggested_uses = use.split(',')
                for suggested_use in suggested_uses:
                    SuggestedUse.objects.get_or_create(name=suggested_use, open_space=open_space)

                description = df['WASH Facilities'][row]
                wash_facility = Services.objects.create(name='WASH Facilities', description=description, open_space=open_space)

                wifi_des = df['Wi-Fi'][row]
                wifi_facility = Services.objects.create(name='Wi-Fi', description=wifi_des, open_space=open_space)

                boundry_wall_des = df['Boundary Wall'][row]
                boundry_facility = Services.objects.create(name='Boundary Wall', description=boundry_wall_des, open_space=open_space)

                electricity_des = df['Electricity Line'][row]
                electricity_facility = Services.objects.create(name='Electricity Line', description=electricity_des, open_space=open_space)

                tree = df['Trees & Vegetation'][row]
                wash_facility = Services.objects.create(name='Trees & Vegetation',
                                                        description=tree,
                                                        open_space=open_space)
                print(open_space, open_space.id)

            except Exception as e:
                print(e)

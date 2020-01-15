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

        print("Wait Data is being Loaded")

        for row in range(0, upper_range):
            total_area = str(df['Total_Area'][row]).replace(',', '')
            capacity = str(df['Capacity'][row]).replace(',', '')

            open_space = OpenSpace.objects.create(
                title=df['Name'][row],
                province=Province.objects.get(
                    code=(df['Province'][row])),
                #
                district=District.objects.get(
                    code=(df['District'][row])),

                municipality=Municipality.objects.get(
                    hlcit_code=(df['Municipality/Metropolian City'][row])),
                ward=df['Ward'][row],
                address=df['Address'][row],
                elevation=df['Elevation'][row],
                total_area=total_area,
                usable_area=df['Usable_Area'][row],
                capacity=capacity,
                current_land_use=df['Current Land Use'][row],
                catchment_area=df['Catchment Area'][row],
                access_to_site=df['Access_to_Site'][row],
                ownership=df['Ownership'][row],
                special_feature=df['Special_features_of_Site'][row],
                polygons=GEOSGeometry(df['the_geom'][row]),
            )
            try:
                use = df['Suggested Use'][row]
                if use != '':
                    suggested_uses = use.split(',')
                    for suggested_use in suggested_uses:
                        a = suggested_use.lstrip()
                        b = a.rstrip()
                        try:
                            sug = SuggestedUseList.objects.get(name=b)
                            sug_data = SuggestedUseData.objects.create(open_space=open_space, suggested_use=sug)
                        except ObjectDoesNotExist:
                            pass

                else:
                    pass

                description = df['WASH_Facility'][row]
                wash_facility = ServiceList.objects.get(name='WASH Facilities')
                w_data = ServiceData.objects.create(description=description, open_space=open_space,
                                                    service=wash_facility)

                wifi_des = df['WiFi'][row]
                wifi_facility = ServiceList.objects.get(name='Wi-Fi')
                wi_data = ServiceData.objects.create(description=wifi_des, open_space=open_space,
                                                     service=wifi_facility)

                boundry_wall_des = df['Boundary_Wall'][row]
                boundry_facility = ServiceList.objects.get(name='Boundary Wall')
                bo_data = ServiceData.objects.create(description=boundry_wall_des, open_space=open_space,
                                                     service=boundry_facility)

                electricity_des = df['Electricity Line'][row]
                electricity_facility = ServiceList.objects.get(name='Electricity Line')
                el_data = ServiceData.objects.create(description=electricity_des, open_space=open_space,
                                                     service=electricity_facility)

                tree = df['Trees_&_Vegetation'][row]
                wash_facility = ServiceList.objects.get(name='Trees & Vegetation')
                el_data = ServiceData.objects.create(description=tree, open_space=open_space,
                                                     service=wash_facility)
                print(open_space, row)

            except Exception as e:
                print(e)

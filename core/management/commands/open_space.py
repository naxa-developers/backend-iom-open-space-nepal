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
        df = pd.read_csv(path).fillna('')
        upper_range = len(df)

        print("Wait Data is being Loaded")

        for row in range(0, upper_range):
            try:
                # capacity = df['Capacity'][row]
                # cap = capacity.replace(',', '')
                tot = df['Total Area'][row]
                cap = df['Capacity'][row]
                # print(df['Name'][row], type(df['Capacity'][row]), type(df['Total Area'][row]), )
                if cap != '':
                    capacities = str(df['Capacity'][row]).replace(',', '')
                    capacity = Decimal(capacities)

                if tot != '':
                    total_areas = str(df['Total Area'][row]).replace(',', '')
                    total_area = Decimal(total_areas)

                open_space = OpenSpace.objects.create(
                    province=Province.objects.get(
                        code=(df['Province'][row])),
                    #
                    district=District.objects.get(
                        code=(df['District'][row])),

                    municipality=Municipality.objects.get(
                        hlcit_code=(df['Municipality'][row])),
                    title=df['Name'][row],
                    current_land_use=df['Current Land Use'][row],
                    total_area=total_area,
                    usable_area=df['Usable Open Space Area'][row],
                    capacity=capacity,
                    catchment_area=df['Catchment Area'][row],
                    access_to_site=df['Access to Site'][row],
                    special_feature=df['Special features'][row],
                    issue=df['Issues'][row],
                    ward=df['Ward'][row],
                    elevation=df['Elevation'][row],
                    ownership=df['Ownership'][row],
                    polygons=GEOSGeometry(df['the_geom'][row]),
                )
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

                description = df['WASH Facilities'][row]
                wash_facility = ServiceList.objects.get(name='WASH Facilities')
                w_data = ServiceData.objects.create(description=description, open_space=open_space,
                                                    service=wash_facility)

                wifi_des = df['Wi-Fi'][row]
                wifi_facility = ServiceList.objects.get(name='Wi-Fi')
                wi_data = ServiceData.objects.create(description=wifi_des, open_space=open_space,
                                                     service=wifi_facility)

                boundry_wall_des = df['Boundary Wall'][row]
                boundry_facility = ServiceList.objects.get(name='Boundary Wall')
                bo_data = ServiceData.objects.create(description=boundry_wall_des, open_space=open_space,
                                                     service=boundry_facility)

                electricity_des = df['Electricity Line'][row]
                electricity_facility = ServiceList.objects.get(name='Electricity Line')
                el_data = ServiceData.objects.create(description=electricity_des, open_space=open_space,
                                                     service=electricity_facility)

                tree = df['Trees & Vegetation'][row]
                wash_facility = ServiceList.objects.get(name='Trees & Vegetation')
                el_data = ServiceData.objects.create(description=tree, open_space=open_space,
                                                     service=wash_facility)
                print(open_space, row)

            except Exception as e:
                print(e)

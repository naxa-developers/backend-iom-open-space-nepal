from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Province, District, ProvinceDummy
from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    # def add_arguments(self, parser):
    #     parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        # path = kwargs['path']
        # df = pd.read_csv(path)
        # upper_range = len(df)

        province_dummy = ProvinceDummy.objects.all()
        try:
            for i in province_dummy:
                province_update = Province.objects.filter(id=i.province_id).update(boundary=i.geom_char)

            if province_update:
                self.stdout.write('Successfully  updated data ..')

        # print("Wait Data is being Loaded")
        # try:
        #     for row in range(0, upper_range):
        #         print(df['id'][row])
        #         province_update = Province.objects.filter(id=df['id'][row]).update(
        #             boundary=GEOSGeometry(df['geom'][row]))
        #
        #     if province_update:
        #         self.stdout.write('Successfully  updated data ..')

        except Exception as e:
            print(e)

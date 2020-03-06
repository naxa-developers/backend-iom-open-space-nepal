import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Municipality, District, Province


class Command(BaseCommand):
        # help = 'load ward from LocalLevelNepal.csv file'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_csv(sys.argv[3])
        for row in range(0, 6781):
            print(row)
            district=District.objects.get(name=(df['DISTRICT'][row]).upper())
            print(district.name)
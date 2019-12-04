from django.core.management.base import BaseCommand

import pandas as pd

from core.models import SuggestedUseList, OpenSpace


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
            # open_space = OpenSpace.objects.get(title__icontains=df['Name'][row])
            suggested = df['Suggested Use'][row]
            suggested_uses = suggested.split(',')
            for name in suggested_uses:
                SuggestedUseList.objects.get_or_create(name=name)
            print(row, 'suggested use list is successfully created')

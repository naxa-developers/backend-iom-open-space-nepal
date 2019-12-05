from django.core.management.base import BaseCommand

import pandas as pd

from core.models import SuggestedUseList, OpenSpace, SuggestedUseData


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_csv(path, skipinitialspace=True).fillna('')
        upper_range = len(df)

        print("Wait Data is being Loaded")

        try:
            for row in range(0, upper_range):
                open_space = OpenSpace.objects.filter(title__icontains=df['Name'][row])
                suggested = df['Suggested Use'][row]
                if suggested != '':
                    suggested_uses = suggested.split(',')
                    for name in suggested_uses:
                        sug = SuggestedUseList.objects.filter(name=name)
                        for i in open_space:
                            for j in sug:
                                SuggestedUseData.objects.create(open_space=i, suggested_use=j)

                else:
                    pass
                print(row, 'data is successfully updated')

        except Exception as e:
            print(e)

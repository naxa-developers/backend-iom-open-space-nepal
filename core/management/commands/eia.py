from django.core.management.base import BaseCommand

import pandas as pd

from core.models import QuestionList, QuestionsData, OpenSpace

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
            open_spaces = OpenSpace.objects.get(
                            title=(df['Name'][row]))


            try:
                question = [
                        QuestionsData.objects.create(
                            question=QuestionList.objects.get(
                                id=1),
                            open_space=open_spaces,
                            ans=df['Is it a protected area?'][row],

                        )

                    ]

            except Exception as e:
                print(e)

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
                # question1 = [
                #         QuestionsData.objects.create(
                #             question=QuestionList.objects.get(
                #                 id=1),
                #             open_space=open_spaces,
                #             ans=df['Is it a protected area?'][row],
                #
                #         )
                #
                #     ]

                question2 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=2),
                        open_space=open_spaces,
                        ans=df['Is it a buffer zone of protected area?'][row],

                    )

                ]

                question3 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=3),
                        open_space=open_spaces,
                        ans=df['Is it a cultural heritage Site?'][row],

                    )

                ]

                question4 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=4),
                        open_space=open_spaces,
                        ans=df['Densely populated area?'][row],

                    )

                ]

                question5 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=5),
                        open_space=open_spaces,
                        ans=df['Special area for protection of biodiversity'][row],

                    )

                ]

                question6 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=6),
                        open_space=open_spaces,
                        ans=df['Will project require temporary or permanent support facilities?'][row],

                    )

                ]

                question7 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=7),
                        open_space=open_spaces,
                        ans=df['Are ecosystems related to project fragile or degraded?'][row],

                    )

                ]

                question8 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=8),
                        open_space=open_spaces,
                        ans=df['Will project cause impairment of ecological opportunities?'][row],

                    )

                ]

                question9 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=9),
                        open_space=open_spaces,
                        ans=df['Will project cause air, soil or water pollution?'][row],

                    )

                ]

                question10 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=10),
                        open_space=open_spaces,
                        ans=df['Will project cause soil erosion and siltation?'][row],

                    )

                ]

                question11 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=11),
                        open_space=open_spaces,
                        ans=df['Will project cause increased waste production?'][row],

                    )

                ]

                question12 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=12),
                        open_space=open_spaces,
                        ans=df['Will project cause Hazardous Waste production?'][row],

                    )

                ]

                question13 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=13),
                        open_space=open_spaces,
                        ans=df['Will project cause threat to local ecosystems due to invasive species?'][row],

                    )

                ]

                question14 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=14),
                        open_space=open_spaces,
                        ans=df['Will project cause Greenhouse Gas Emissions?'][row],

                    )

                ]

                question15 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=15),
                        open_space=open_spaces,
                        ans=df['Will project cause use of pesticides?'][row],

                    )

                ]

                question16 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=16),
                        open_space=open_spaces,
                        ans=df['Does the project encourage the use of environmentally friendly technologies?'][row],

                    )

                ]

                question17 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=17),
                        open_space=open_spaces,
                        ans=df['Other environmental issues, e.g. noise and traffic'][row],

                    )

                ]
                print('Successfully updated data')
            except Exception as e:
                print(e)

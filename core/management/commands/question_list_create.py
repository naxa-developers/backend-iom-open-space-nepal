from django.core.management.base import BaseCommand

import pandas as pd

from core.models import QuestionList

from django.contrib.gis.geos import Point

questions = [
    'Is it a protected area?',
    'Is it a buffer zone of protected area?',
    'Is it a cultural heritage Site?',
    'Densely populated area?',
    'Special area for protection of biodiversity?',
    'Will project require temporary or permanent support facilities?',
    'Are ecosystems related to project fragile or degraded?',
    'Will project cause impairment of ecological opportunities?',
    'Will project cause air, soil or water pollution?',
    'Will project cause soil erosion and siltation?',
    'Will project cause increased waste production?',
    'Will project cause Hazardous Waste production?',
    'Will project cause threat to local ecosystems due to invasive species?',
    'Will project cause Greenhouse Gas Emissions?',
    'Will project cause use of pesticides?',
    'Does the project encourage the use of environmentally friendly technologies?',
    'Other environmental issues, e.g. noise and traffic?',
    'Will the project cause increase in peak and flows? (Including from temporary or permanent water)'
]


class Command(BaseCommand):
    help = 'Create Question List'

    def handle(self, *args, **kwargs):
        for i in questions:
            question = QuestionList.objects.create(title=i)
            print(i, 'Successfully Created Questions List')









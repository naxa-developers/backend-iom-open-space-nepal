import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import MunicipalityAvailableType, Municipality, AvailableType


class Command(BaseCommand):
    help = 'Add available type in municipality'

    def add_arguments(self, parser):
        parser.add_argument('-l', '--muni_ids', nargs='+',
                            help=' python manage.py delete_site_submissions  -l ', required=True)

    def handle(self, *args, **options):

        muni_ids = options['muni_ids']
        types = AvailableType.objects.all()
        muni_available_types = []
        for muni in muni_ids:
            municipality = Municipality.objects.get(id=muni)

            for title in types:
                obj = MunicipalityAvailableType(municipality=municipality,
                                                available_type=title)
                muni_available_types.append(obj)

        MunicipalityAvailableType.objects.bulk_create(muni_available_types)

        self.stdout.write('Successfully added available types in Municipality. ')



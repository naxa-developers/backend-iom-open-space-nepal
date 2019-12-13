from decimal import Decimal

from django.core.management.base import BaseCommand
from core.models import OpenSpace


class Command(BaseCommand):
    def handle(self, *args, **options):
        open_spaces = OpenSpace.objects.all()
        ids = []
        count = 0
        try:
            for open_space in open_spaces:
                ids.append(open_space.id)
            for i in ids:
                os = OpenSpace.objects.get(id=i)
                if os.ward is None:
                    print('ward vakue is none')
                elif os.ward == '':
                    print(os.title)
                    print('emoty string')
                else:
                    if type(os.ward) == str:
                        os.ward = int(Decimal(os.ward.replace(" ", "")))
                    elif type(os.ward) == int:
                        print(os.id, 'int')
                        os.ward = os.ward
                    elif type(os.ward) == float:
                        print(os.id, 'float')
                        os.ward = int(os.ward.strip())
                    os.save()
                    print(os.id, os.title)
                    count += 1


        except Exception as e:
            print(e)
        print(len(ids))
        print(count)

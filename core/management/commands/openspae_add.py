from django.core.management.base import BaseCommand
from core.models import OpenSpace


class Command(BaseCommand):
    def handle(self, *args, **options):
        open_spaces = OpenSpace.objects.all()
        ids = []
        for open_space in open_spaces:

            # if open_space.ward:
            #     address = open_space.municipality.name + '-' + open_space.ward + ',' + open_space.district.name
            # else:
            #     address = open_space.municipality.name + ',' + open_space.district.name
            print(open_space.id)
            ids.append(open_space.id)
        for i in ids:
            os = OpenSpace.objects.get(id=i)
            print(os.id)
            if os.ward is None:
                address = os.municipality.name + ',' + os.district.name
            else:
                if type(os.ward) == str:
                    os.ward = int(float(os.ward))
                elif type(os.ward) == int:
                    os.ward = os.ward
                elif type(os.ward) == float:
                    os.ward = int(os.ward)
                os.save()
                print(os.id)
                address = os.municipality.name + '-' + str(os.ward) + ',' + os.district.name
            os.address = address
            os.save()

        print(len(ids))

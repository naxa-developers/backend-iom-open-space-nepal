from django.core.management.base import BaseCommand

import pandas as pd

from core.models import QuestionList, QuestionsData, OpenSpace, ServiceData, ServiceList, Municipality, \
    District, Province, AvailableFacility, AvailableType, AvailableSubType, SuggestedUseList, SuggestedUseData

from django.contrib.gis.geos import GEOSGeometry, Point
from dashboard import shapefileIO


def upload_eia(path):
    df = pd.read_csv(path)
    upper_range = len(df)

    print("Wait Data is being Loaded")

    for row in range(0, upper_range):
        open_spaces = OpenSpace.objects.get(
                        title=(df['Name'][row]))

        try:
            question1 = [
                    QuestionsData.objects.create(
                        question=QuestionList.objects.get(
                            id=1),
                        open_space=open_spaces,
                        ans=df['Is it a protected area?'][row],

                    )

                ]

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


def upload_openspace(path):
    df = pd.read_csv(path, encoding='unicode_escape').fillna('')
    upper_range = len(df)

    print("Wait Data is being Loaded")

    for row in range(0, upper_range):
        total_area = str(df['Total_Area'][row]).replace(',', '')
        capacity = str(df['Capacity'][row]).replace(',', '')

        open_space = OpenSpace.objects.create(
            title=df['Name'][row],
            province=Province.objects.get(
                code=(df['Province'][row])),
            #
            district=District.objects.get(
                code=(df['District'][row])),

            municipality=Municipality.objects.get(
                hlcit_code=(df['Municipality/Metropolian City'][row])),
            ward=df['Ward'][row],
            address=df['Address'][row],
            elevation=df['Elevation'][row],
            total_area=total_area,
            usable_area=df['Usable_Area'][row],
            capacity=capacity,
            # current_land_use=df['Current Land Use'][row],
            # catchment_area=df['Catchment Area'][row],
            access_to_site=df['Access_to_Site'][row],
            ownership=df['Ownership'][row],
            special_feature=df['Special_features_of_Site'][row],
            polygons=GEOSGeometry(df['the_geom'][row]),
        )
        try:
            # use = df['Suggested Use'][row]
            # if use != '':
            #     suggested_uses = use.split(',')
            #     for suggested_use in suggested_uses:
            #         a = suggested_use.lstrip()
            #         b = a.rstrip()
            #         try:
            #             sug = SuggestedUseList.objects.get(name=b)
            #             sug_data = SuggestedUseData.objects.create(open_space=open_space, suggested_use=sug)
            #         except ObjectDoesNotExist:
            #             pass
            #
            # else:
            #     pass

            description = df['WASH_Facility'][row]
            wash_facility = ServiceList.objects.get(name='WASH Facilities')
            w_data = ServiceData.objects.create(description=description, open_space=open_space,
                                                service=wash_facility)

            wifi_des = df['WiFi'][row]
            wifi_facility = ServiceList.objects.get(name='Internet')
            wi_data = ServiceData.objects.create(description=wifi_des, open_space=open_space,
                                                 service=wifi_facility)

            boundry_wall_des = df['Boundary_Wall'][row]
            boundry_facility = ServiceList.objects.get(name='Boundary Wall')
            bo_data = ServiceData.objects.create(description=boundry_wall_des, open_space=open_space,
                                                 service=boundry_facility)

            electricity_des = df['Electricity Line'][row]
            electricity_facility = ServiceList.objects.get(name='Electricity Line')
            el_data = ServiceData.objects.create(description=electricity_des, open_space=open_space,
                                                 service=electricity_facility)

            tree = df['Trees_&_Vegetation'][row]
            wash_facility = ServiceList.objects.get(name='Trees & Vegetation')
            el_data = ServiceData.objects.create(description=tree, open_space=open_space,
                                                 service=wash_facility)
            print(open_space, row)

        except Exception as e:
            print(e)


def add_open_space(open_space_file, open_space_shp_file, municipality, main_open_space):
    try:
        df = pd.read_excel(open_space_file, encoding='unicode_escape').fillna('')
    except:
        return {'error': 'Please upload file with provided formats.'}
    upper_range = len(df)
    municipality_obj = municipality
    province = municipality_obj.province
    district = municipality_obj.district
    if upper_range == 0:
        return {'error': 'Please populate data in excel file.'}
    for row in range(0, upper_range):
        try:
            location = Point(float(df['Longitude'][row]), float(df['Latitude'][row]))
        except:
            location = None
        try:
            open_space = OpenSpace.objects.create(
                main_open_space=main_open_space,
                oid=df['OID'][row],
                title=df['Name'][row],
                province=province,
                district=district,
                municipality=municipality_obj,
                ward=df['Ward'][row],
                address=df['Address'][row],
                coordinates_elevation=df['Coordinate, Elevation'][row],
                elevation=df['Elevation'][row],
                total_area=df['Total_Area'][row],
                usable_area=df['Usable_Area'][row],
                current_land_use=df['Current Land Use'][row],
                catchment_area=df['Catchment Area'][row],
                access_to_site=df['Access to Site'][row],
                ownership=df['Ownership'][row],
                special_feature=df['Special features'][row],
                capacity=df['Capacity'][row],
                issue=df['Issues'][row],
                change_remarks=df['Change_remarks'][row],
                perimeter=df['Perimeter'][row],
                usable_2013=df['Usable-2013'][row],
                area_change=df['Area Change'][row],
                health_facilities=df['Health_Facilities'][row],
                market=df['Market_Access'][row],
                security=df['Security'][row],
                helipad=df['Helipad'][row],
                educational_infrastructures=df['Educational_Infrastructures'][row],
                location=location

            )
            suggested_uses = df['Suggested Use'][row]
            if len(suggested_uses) > 0:
                suggested_uses = df['Suggested Use'][row].split(',')
                for suggest in suggested_uses:

                    suggest_obj = SuggestedUseList.objects.get_or_create(name=suggest)
                    sug_data = SuggestedUseData.objects.create(open_space=open_space,
                                                               suggested_use=suggest_obj[0])
            else:
                pass
        except Exception as e:
            return {'error': str(e)}
        try:

            description = df['WASH_Facility'][row]
            is_available_wash_facility = df['WASH Facilities_YN'][row].upper()
            wash_facility = ServiceList.objects.get(name='WASH Facilities_YN')
            w_data = ServiceData.objects.create(description=description,
                                                open_space=open_space,
                                                service=wash_facility,
                                                is_available=is_available_wash_facility
                                                )

            wifi_des = df['Internet'][row]
            is_available_wifi = df['Internet_YN'][row].upper()
            wifi_facility = ServiceList.objects.get(name='Internet')
            wi_data = ServiceData.objects.create(description=wifi_des,
                                                 open_space=open_space,
                                                 service=wifi_facility,
                                                 is_available=is_available_wifi

                                                 )

            boundry_wall_des = df['Boundary Wall'][row]
            is_available_boundry_wall = df['Boundary Wall_YN'][row].upper()
            boundry_facility = ServiceList.objects.get(name='Boundary Wall')
            bo_data = ServiceData.objects.create(description=boundry_wall_des,
                                                 open_space=open_space,
                                                 service=boundry_facility,
                                                 is_available=is_available_boundry_wall
                                                 )

            is_available_electricity = df['Electricity Line_YN'][row].upper()
            electricity_facility = ServiceList.objects.get(name='Electricity Line')
            el_data = ServiceData.objects.create(open_space=open_space,
                                                 service=electricity_facility,
                                                 is_available=is_available_electricity)

            tree = df['Trees & Vegetation'][row]
            is_available_tree = df['Trees & Vegetation_YN'][row].upper()
            wash_facility = ServiceList.objects.get(name='Trees & Vegetation')
            el_data = ServiceData.objects.create(description=tree,
                                                 open_space=open_space,
                                                 service=wash_facility,
                                                 is_available=is_available_tree
                                                 )
        except Exception as e:
            return {'error': str(e)}

        try:
            shapefileIO.importData(open_space_shp_file)
        except Exception as e:
            return {'error': str(e)}
        return {'success': 'Added successfully.'}


def upload_amenities(path):
    df = pd.read_csv(path).fillna('')
    upper_range = len(df)

    print("Wait Data is being Loaded")

    for row in range(0, upper_range):

        try:
            # print(float(df['Latitude'][row]))
            # print(float(df['Longitude'][row]))
            # print(Point(float(df['Latitude'][row]), float(df['Longitude'][row])))

            q=AvailableFacility.objects.create(
                name=df['name'][row],
                type='education facility',
                education_type=df['isced_leve'][row],
                operator_type=df['operator_t'][row],
                location=Point(float(df['log'][row]), float(df['Lat'][row])),
            )
            print(row, q.name)

        except Exception as e:
            print(e)



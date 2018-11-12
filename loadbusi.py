# import os
# os.environ.setdefault('DJANGO_SETTING_MODULE', 'DjangoTest.settings')
# import django
# django.setup()
#

from restaurant.models import Business
# import json

# file = open('business.json', 'r', encoding='utf-8')
# s = json.load(file)
# print(s[0]['name'])

import fileinput


def start():
    print('Loading business...')
    count = 0
    finput = fileinput.input("business.json")
    for line in finput:
        stateIndex = line.find('"state"')
        # print('city:', line[cityIndex + 8:stateIndex - 2])
        postalIndex = line.find('"postal_code"')
        # print('state:', line[stateIndex + 9:postalIndex - 2])
        categoriesIndex = line.find('"categories"')
        # print('attributes(as String):',line[attrIndex+13:categoriesIndex-1])
        hoursIndex = line.find('"hours"')
        # print('categories:',line[categoriesIndex+14:hoursIndex-2])

        if line[stateIndex + 9:postalIndex - 2] == 'WI' and 'Restaurant' in line[categoriesIndex + 14:hoursIndex - 2]:
            # print('---------------------')
            # print(line)
            # if count == 2000:
            #     break
            count = count + 1
            idIndex = line.find('"business_id"')
            # print("business_id:", line[idIndex:38])
            nameIndex = line.find('"name"')
            neighIndex = line.find('"neighborhood"')
            # print("name:", line[48:neighIndex - 2])
            addressIndex = line.find('"address"')
            # print('neighbor:', line[neighIndex + 16:addressIndex - 2])
            cityIndex = line.find('"city"')
            # print('address:', line[addressIndex + 11:cityIndex - 2])
            latitudeIndex = line.find('"latitude"')
            # print('postal_code:', line[postalIndex+15:latitudeIndex-2])
            longitudeIndex = line.find('"longitude"')
            # print('latitude:',line[latitudeIndex+11:longitudeIndex-1])
            starIndex = line.find('"stars"')
            # print('longitude:',line[longitudeIndex+12:starIndex-1])
            reviewcIndex = line.find('"review_count"')
            # print('stars:',line[starIndex+8:reviewcIndex-1])
            isopenIndex = line.find('"is_open"')
            # print('review_count:',line[reviewcIndex+15:isopenIndex-1])
            attrIndex = line.find('"attributes"')
            # print('is_open:',line[isopenIndex+10:attrIndex-1])

            # print('hours:', line[hoursIndex + 8:-2])

            temp = Business(business_id=line[idIndex + 15:nameIndex - 2],
                            name=line[nameIndex + 8:neighIndex - 2],
                            neighborhood=line[neighIndex + 16:addressIndex - 2],
                            address=line[addressIndex + 11:cityIndex - 2],
                            city=line[cityIndex + 8:stateIndex - 2],
                            state=line[stateIndex + 9:postalIndex - 2],
                            postal_code=line[postalIndex + 15:latitudeIndex - 2],
                            latitude=line[latitudeIndex + 11:longitudeIndex - 1],
                            longitude=line[longitudeIndex + 12:starIndex - 1],
                            stars=line[starIndex + 8:reviewcIndex - 1],
                            review_count=line[reviewcIndex + 15:isopenIndex - 1],
                            is_open=line[isopenIndex + 10:attrIndex - 1],
                            attributes=line[attrIndex + 13:categoriesIndex - 1],
                            categories=line[categoriesIndex + 14:hoursIndex - 2],
                            hours=line[hoursIndex + 8:-2])
            temp.save()

    finput.close()
    print("Finish loading.")
    print('Sample size:', count)


start()

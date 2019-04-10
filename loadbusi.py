# import os
# os.environ.setdefault('DJANGO_SETTING_MODULE', 'DjangoTest.settings')
# import django
# django.setup()
#

from restaurant.models import Business
import matplotlib.pyplot as plt
from scipy.stats import norm
# import json

# file = open('business.json', 'r', encoding='utf-8')
# s = json.load(file)
# print(s[0]['name'])

import fileinput


def start():
    print('Loading business...')
    count = 0
    finput = fileinput.input("user.json")
    lens = []
    for line in finput:
        # print(line)
        count = count+1
        # stateIndex = line.find('"state"')
        # categoriesIndex = line.find('"categories"')
        # hoursIndex = line.find('"hours"')
        # postalIndex = line.find('"postal_code"')
        #
        # if 'Restaurant' in line[categoriesIndex + 14:hoursIndex - 2] and line[stateIndex + 9:postalIndex - 2] == 'WI':
        #     # print('---------------------')
        #     # print(line)
        #     # if count == 2000:
        #     #     break
        #     reviewcIndex = line.find('"review_count"')
        #     isopenIndex = line.find('"is_open"')
        #
        #     # this code check the review #
        #     # if int(line[reviewcIndex + 15:isopenIndex - 1])>0:
        #     #     print(line[cityIndex + 8:stateIndex - 2])
        #     count = count + 1
        #     #     lens.append(int(line[reviewcIndex + 15:isopenIndex - 1]))
        #
        #     idIndex = line.find('"business_id"')
        #     nameIndex = line.find('"name"')
        #     neighIndex = line.find('"neighborhood"')
        #     addressIndex = line.find('"address"')
        #     cityIndex = line.find('"city"')
        #     latitudeIndex = line.find('"latitude"')
        #     longitudeIndex = line.find('"longitude"')
        #     starIndex = line.find('"stars"')
        #     cityIndex = line.find('"city"')
        #     attrIndex = line.find('"attributes"')
        #
        #     temp = Business(business_id=line[idIndex + 15:nameIndex - 2],
        #                     name=line[nameIndex + 8:neighIndex - 2],
        #                     neighborhood=line[neighIndex + 16:addressIndex - 2],
        #                     address=line[addressIndex + 11:cityIndex - 2],
        #                     city=line[cityIndex + 8:stateIndex - 2],
        #                     state=line[stateIndex + 9:postalIndex - 2],
        #                     postal_code=line[postalIndex + 15:latitudeIndex - 2],
        #                     latitude=line[latitudeIndex + 11:longitudeIndex - 1],
        #                     longitude=line[longitudeIndex + 12:starIndex - 1],
        #                     stars=line[starIndex + 8:reviewcIndex - 1],
        #                     review_count=int(line[reviewcIndex + 15:isopenIndex - 1]),
        #                     is_open=line[isopenIndex + 10:attrIndex - 1],
        #                     attributes=line[attrIndex + 13:categoriesIndex - 1],
        #                     categories=line[categoriesIndex + 14:hoursIndex - 2],
        #                     hours=line[hoursIndex + 8:-2])
        #     temp.save()

    finput.close()
    print("Finish loading.")
    print('Sample size:', count)
    # plt.hist(lens,edgecolor='black', bins=int(50), density=True)
    # plt.title("Density Histogram")
    # plt.xlabel("Review Count")
    # plt.ylabel("Density")
    # plt.show()


# if __name__ == '__main__':
start()

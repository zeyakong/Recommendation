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
    blist = []
    lens =[]
    finput = fileinput.input("business.json")
    for line in finput:
        # print(line)
        stateIndex = line.find('"state"')
        cityIndex = line.find('"city"')

        if line[cityIndex + 8:stateIndex - 2] == 'Las Vegas':
            # print('---------------------')
            # print(line)
            # if count == 2000:
            #     break
            reviewcIndex = line.find('"review_count"')
            isopenIndex = line.find('"is_open"')
            categoriesIndex = line.find('"categories"')
            hoursIndex = line.find('"hours"')
            if  200<int(line[reviewcIndex + 15:isopenIndex - 1])<500 and 'Restaurant' in line[categoriesIndex + 14:hoursIndex - 2]:
                count = count + 1
                if count == 1000:
                    break
                lens.append(int(line[reviewcIndex + 15:isopenIndex - 1]))
                idIndex = line.find('"business_id"')
                nameIndex = line.find('"name"')
                blist.append(line[idIndex + 15:nameIndex - 2])


            postalIndex = line.find('"postal_code"')
            neighIndex = line.find('"neighborhood"')
            addressIndex = line.find('"address"')
            cityIndex = line.find('"city"')
            latitudeIndex = line.find('"latitude"')
            longitudeIndex = line.find('"longitude"')
            starIndex = line.find('"stars"')

            attrIndex = line.find('"attributes"')

            # temp = Business(business_id=line[idIndex + 15:nameIndex - 2],
            #                 name=line[nameIndex + 8:neighIndex - 2],
            #                 neighborhood=line[neighIndex + 16:addressIndex - 2],
            #                 address=line[addressIndex + 11:cityIndex - 2],
            #                 city=line[cityIndex + 8:stateIndex - 2],
            #                 state=line[stateIndex + 9:postalIndex - 2],
            #                 postal_code=line[postalIndex + 15:latitudeIndex - 2],
            #                 latitude=line[latitudeIndex + 11:longitudeIndex - 1],
            #                 longitude=line[longitudeIndex + 12:starIndex - 1],
            #                 stars=line[starIndex + 8:reviewcIndex - 1],
            #                 review_count=line[reviewcIndex + 15:isopenIndex - 1],
            #                 is_open=line[isopenIndex + 10:attrIndex - 1],
            #                 attributes=line[attrIndex + 13:categoriesIndex - 1],
            #                 categories=line[categoriesIndex + 14:hoursIndex - 2],
            #                 hours=line[hoursIndex + 8:-2])
            # temp.save()

    print("Finish loading restaurant.")
    print('Sample size:', count)
    print('review count:', sum(lens))
    count = 0
    return
    print("\nstart loading reviews...")
    filput = fileinput.input('review.json')
    for line in filput:
        # print(line)
        business_id_index = line.find('"business_id"')
        stars_index = line.find('"stars"')
        # print(line[business_id_index + 15:stars_index - 2])
        # if count == 5000:
        #     break
        if line[business_id_index + 15:stars_index - 2] in blist:
            count = count + 1
            id_index = line.find('"review_id"')
            user_id_index = line.find('"user_id"')
            date_index = line.find('"date"')
            text_index = line.find('"text"')
            useful_index = line.find('"useful"')
            funny_index = line.find('"funny"')
            cool_index = line.find('"cool"')
            # temp = Review(review_id=line[id_index + 13:user_id_index - 2],
            #               user_id=line[user_id_index+11:business_id_index-2],
            #               business_id=line[business_id_index + 15:stars_index - 2],
            #               stars=line[stars_index + 8:date_index - 1],
            #               date=line[date_index + 8:text_index - 2],
            #               text=line[text_index + 8:useful_index - 2],
            #               useful=line[useful_index + 9:funny_index - 1],
            #               funny=line[funny_index + 8:cool_index - 1],
            #               cool=line[cool_index + 7:-2])
            # temp.save()

    print('Finish Loading reviews.')
    print('count:', count)

    # plt.hist(lens, edgecolor='black', bins=int(50), density=True)
    # plt.title("Density Histogram")
    # plt.xlabel("Review Count")
    # plt.ylabel("Density")
    # plt.show()
    finput.close()


# if __name__ == '__main__':
start()

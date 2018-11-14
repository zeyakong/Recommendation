from restaurant.models import Business, Review

import fileinput


def start():
    print('Loading reviews...')
    print('Create business_id map')
    count = 0
    blist = Business.objects.all()
    # declare list
    list = []
    for var in blist:
        list.append(var.business_id)
        # count = int(var.review_count) + count
    print('Finish creating business list')

    filput = fileinput.input('review.json')
    for line in filput:
        # print(line)
        business_id_index = line.find('"business_id"')
        stars_index = line.find('"stars"')
        # print(line[business_id_index + 15:stars_index - 2])
        # if count == 5000:
        #     break
        if list.count(line[business_id_index + 15:stars_index - 2]) != 0:
            count = count + 1
            print('Got:', count)
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

    filput.close()
    print('Finish Loading.')
    print('count:', count)


start()

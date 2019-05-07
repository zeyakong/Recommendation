from restaurant.models import Customer, Review

import fileinput


def start():
    print('Loading users...')
    print('Create user_id map')
    count = 0
    blist = Review.objects.all()
    # declare list
    list = []
    for var in blist:
        if var.user_id not in list:
            list.append(var.user_id)
        # count = int(var.review_count) + count
    print('Finish creating user list')
    print('Count:', len(list))

    filput = fileinput.input('user.json')
    for line in filput:
        # print(line)
        user_id_index = line.find('"user_id"')
        name_index = line.find('"name"')

        # print(line[user_id_index + 11:name_index - 2])
        # if count == 5000:
        #     break
        if line[user_id_index + 11:name_index - 2] in list:
            count = count + 1
            # print('Got:', count)
            review_count_index = line.find('"review_count"')
            average_stars_index = line.find('"average_stars"')
            compliment_hot_index = line.find('"compliment_hot"')
            temp = Customer(user_id=line[user_id_index + 11:name_index - 2],
                            name=line[name_index+8:review_count_index-2],
                            average_stars=line[average_stars_index+16:compliment_hot_index-1])
            temp.save()
        # print(line[id_index + 13:user_id_index - 2])
        # print(line[user_id_index + 11:business_id_index - 2])
        # print(line[business_id_index + 15:stars_index - 2])
        # print(line[stars_index + 8:date_index - 1])
        # print(line[date_index + 8:text_index - 2])
        # print(line[text_index + 8:useful_index - 2])
        # print('useful:', line[useful_index + 9:funny_index - 1])
        # print(line[funny_index + 8:cool_index - 1])
        # print(line[cool_index + 7:-2])

    filput.close()
    print('Finish Loading.')
    print('count:', count)


start()

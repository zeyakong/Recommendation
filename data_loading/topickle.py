# coding:utf-8
import numpy as np
from restaurant.models import Business, Customer, Review
from django.db.models import Q

import pickle


def save():
    # q = Q()
    #
    # for var in category_list:
    #     q = Q(categories=var) | q

    # get all this categories business
    business_list = Business.objects.all()
    # user_list = Customer.objects.all()
    review_list = Review.objects.all()

    blist = []
    for var in business_list:
        blist.append(var.business_id)

    ulist = []
    for var in review_list:
        if var.user_id not in ulist:
            ulist.append(var.user_id)
    # print(blist)

    user_count = len(ulist)
    business_count = len(business_list)

    matrix = np.zeros([business_count, user_count])
    # print(n)
    print("Creating the business-user rating matrix...")
    for var in review_list:
        # print(var.stars)
        business_index = blist.index(var.business_id)
        user_index = ulist.index(var.user_id)
        # print(business_index,user_index)
        matrix[business_index][user_index] = int(var.stars)
    print('Finish creating.')
    # pickle
    print(matrix)
    print('len of matrix is :', len(matrix))
    # store this obj
    output = open('matrix.pkl', 'wb')
    pickle.dump(matrix, output)
    output.close()

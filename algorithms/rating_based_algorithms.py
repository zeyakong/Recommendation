import collections
import pickle
import pprint
from collections import defaultdict, OrderedDict
from operator import itemgetter

import numpy as np

from algorithms.algorithm_utils import load_pickle, cosine_sim, euclidean_sim, pearson_sim, find_2vector_nonzero_sub, \
    find_sub_matrix, recommend_restaurant
from users.models import UserReview, User


def user_cf(username, similarity_method):
    """
    This method will return a list of dict restaurant ordered by rank.
    1. Find users which have the same rating for the new user : account >= 30
    2. Find similar users from 1. list : account : 15
    3. Find the high average scored restaurants : account: 5
    :param username:
    :param similarity_method:
    :return:
    """
    # the root path is the project folder
    rating_matrix = load_pickle('algorithms/rating_matrix.pkl')
    # get the user vector, the user is the system new user, so, it is from the userReviews model
    user_review_list = UserReview.objects.filter(user=User.objects.get(username=username))
    user_dict = dict()
    for one_review in user_review_list:
        user_dict[one_review.business_id] = one_review.stars

    """
    first find the unrecorded restaurant
    find similar users from the dataset
    1. find the users list which the new user and customers have [threshold] common rating.
    this function is a recursive function: first the min of user_vector is 5, 
    so, the threshold is 80% : 4.
    """
    threshold = len(user_dict.keys()) - 1  # means # of the common rating
    sub_matrix = find_sub_matrix(user_dict, rating_matrix, threshold)
    while len(sub_matrix.keys()) < 30:
        threshold = threshold - 1
        sub_matrix = find_sub_matrix(user_dict, rating_matrix, threshold)
    # print('len of user reviews:', len(user_dict.keys()))

    # print('find ', len(sub_matrix), 'people, threshold: ', threshold)
    # reduce the sub_matrix by ordering the similarity for that user.
    restaurant_keys = list()
    user_vector = list()
    for one_restaurant in user_dict.keys():
        restaurant_keys.append(one_restaurant)
        user_vector.append(int(user_dict[one_restaurant]))
    similarity = dict()
    for one_similar_user in sub_matrix.keys():
        # transfer the dict into vector to calculate.
        customer_vector = list()
        for one_restaurant in restaurant_keys:
            if one_restaurant in sub_matrix[one_similar_user]:
                customer_vector.append(int(sub_matrix[one_similar_user][one_restaurant]))
            else:
                customer_vector.append(0)
        # now we have two vectors: user_vector and customer_vector. we can calculate the similarity
        v1 = np.array(user_vector)
        v2 = np.array(customer_vector)
        # at that time we calculate the zero value:
        # v1, v2 = find_2vector_nonzero_sub(user_vector, customer_vector)
        if len(v1)>0 and len(v2)>0:
            # find similarity
            if similarity_method == 'euclidean':
                sim_score = euclidean_sim(vector1=v1, vector2=v2)
            elif similarity_method == 'cosine':
                sim_score = cosine_sim(vector1=v1, vector2=v2)
            else:
                print(v1, v2)
                sim_score = pearson_sim(vector1=v1, vector2=v2)
        else:
            sim_score =0
        similarity[one_similar_user] = sim_score
    # get top 15 similar users
    top_similar_users = collections.Counter(similarity).most_common(15)
    return top_similar_users, recommend_restaurant(similarity,user_dict)


def item_cf(rating_matrix, username, similarity_method, rec_type='popular'):
    # get the user vector, the user is the system new user, so, it is from the userReviews model
    user_review_list = UserReview.objects.filter(user=User.objects.get(username=username))
    user_dict = dict()
    for one_review in user_review_list:
        user_dict[one_review.business_id] = one_review.stars

    # first find the unrecorded restaurant
    # find similar users from the dataset
    """
    1. find the restaurant  which the new user liked most.
    this function is a recursive function: first the min of user_vector is 5, 
    so, the threshold is 80% : 4.
    """
    threshold = len(user_dict.keys()) - 1  # means # of the common rating
    sub_matrix = find_sub_matrix(user_dict, rating_matrix, threshold)
    while len(sub_matrix.keys()) < 30:
        threshold = threshold - 1
        sub_matrix = find_sub_matrix(user_dict, rating_matrix, threshold)
    # print('len of user reviews:', len(user_dict.keys()))

    # print('find ', len(sub_matrix), 'people, threshold: ', threshold)
    # reduce the sub_matrix by ordering the similarity for that user.
    restaurant_keys = list()
    user_vector = list()
    for one_restaurant in user_dict.keys():
        restaurant_keys.append(one_restaurant)
        user_vector.append(int(user_dict[one_restaurant]))
    similarity = dict()
    for one_similar_user in sub_matrix.keys():
        # transfer the dict into vector to calculate.
        customer_vector = list()
        for one_restaurant in restaurant_keys:
            if one_restaurant in sub_matrix[one_similar_user]:
                customer_vector.append(int(sub_matrix[one_similar_user][one_restaurant]))
            else:
                customer_vector.append(0)
        # now we have two vectors: user_vector and customer_vector. we can calculate the similarity
        v1 = np.array(user_vector)
        v2 = np.array(customer_vector)
        # v1, v2 = find_2vector_nonzero_sub(user_vector, customer_vector)
        # find similarity
        if similarity_method == 'euclidean':
            sim_score = euclidean_sim(vector1=v1, vector2=v2)
        elif similarity_method == 'cosine':
            sim_score = cosine_sim(vector1=v1, vector2=v2)
        else:
            sim_score = pearson_sim(vector1=v1, vector2=v2)
        similarity[one_similar_user] = sim_score
    # get top 15 similar users
    top_similar_users = collections.Counter(similarity).most_common(15)


def rating_recommend(username, similarity_method='euclidean'):
    """
    This function will use user_cf algorithm to generate recommendation
    :param username: the name of the input user. if the id is not existed, it will return null
    :param similarity_method: 'cosine', 'euclidean', 'pearson'
    :return:
    """

    return user_cf(username, similarity_method)

#
# if __name__ == '__main__':
#     pprint.pprint(rating_recommend('123'))
#     exit()

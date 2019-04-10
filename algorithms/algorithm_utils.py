import collections
import pickle
import pprint
from collections import defaultdict

import numpy as np


def euclidean_sim(vector1, vector2):
    # o distance
    o_distance = np.linalg.norm(vector1 - vector2)
    return 1 / (1 + o_distance)


def cosine_sim(vector1, vector2):
    # calculate cos_distance
    cos_distance = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * (np.linalg.norm(vector2)))
    # normalize
    return 0.5 + 0.5 * cos_distance


def pearson_sim(vector1, vector2):
    vector1 = vector1.tolist()
    vector2 = vector2.tolist()
    return 0.5 + 0.5 * np.corrcoef(vector1, vector2)[0][1]


# find two vectors' nonzero elements and return the two sub vectors.
def find_2vector_nonzero_sub(v1, v2):
    temp_1 = list()
    temp_2 = list()
    for i in range(min(len(v1), len(v2))):
        if v1[i] > 0 and v2[i] > 0:
            temp_1.append(v1[i])
            temp_2.append(v2[i])
    return np.array(temp_1), np.array(temp_2)


def load_pickle(pickle_name):
    pkl_file = open(pickle_name, 'rb')
    data = pickle.load(pkl_file)
    # pprint.pprint(data)
    pkl_file.close()
    return data


def find_sub_matrix(user_vector, matrix, threshold):
    sub_matrix = defaultdict(dict)
    for one_user in matrix.keys():
        matches = 0
        for one_restaurant in user_vector.keys():
            if one_restaurant in matrix[one_user]:
                matches = matches + 1
        # matches means number of they rated the same restaurant
        if matches >= threshold:
            sub_matrix[one_user] = matrix[one_user]
    return sub_matrix


def recommend_restaurant(similarity, user_dict):
    # get top 15 similar users
    top_similar_users = collections.Counter(similarity).most_common(15)

    # load rating matrix
    rating_matrix = load_pickle('algorithms/rating_matrix.pkl')

    # start recommend. From the sub matrix to find the restaurants the target user never go.
    # find current sub matrix:
    sub_matrix = defaultdict(dict)
    top_similar_users_id = list()
    for one_user in top_similar_users:
        sub_matrix[one_user[0]] = rating_matrix[one_user[0]]
        top_similar_users_id.append(one_user[0])
    # user_dict.keys() means those restaurants the user came
    recommend_weight = dict()
    recommend_total = dict()

    for one_user in top_similar_users_id:
        # print(sub_matrix[one_user])
        for one_rating in sub_matrix[one_user].keys():
            # calculate the weighted average star rating
            recommend_weight[one_rating] = recommend_weight.get(one_rating, 0) + similarity[one_user]
            recommend_total[one_rating] = float(recommend_total.get(one_rating, 0)) + float(
                sub_matrix[one_user][one_rating]) * similarity[one_user]
    recommend_final = dict()
    for one_restaurant in recommend_total.keys():
        recommend_final[one_restaurant] = recommend_total[one_restaurant]
    for one_restaurant in recommend_final.keys():
        if one_restaurant in user_dict.keys():
            recommend_final[one_restaurant] = 0

    return collections.Counter(recommend_final).most_common(5)

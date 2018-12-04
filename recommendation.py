import pprint, pickle
import numpy as np
import math
import random
import matplotlib.pyplot as plt


def load_pickle(pickle_name):
    print("Load the ", pickle_name, " matrix...")
    pkl_file = open(pickle_name, 'rb')
    data = pickle.load(pkl_file)
    # pprint.pprint(data)
    pkl_file.close()
    return data


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
    return 0.5 + 0.5 * np.corrcoef(vector1, vector2)[0][1]


def psd():
    pass


def start():
    """
    this function is the entry of this program
    :return: none
    """

    # load three matrix
    # rm rating matrix , rm[rid][uid] = rating
    # wm words vector matrix, wm[index] = word-frequency vector. len(wm) = total text reviews
    # len(wm[0]) = 2000. only chose the top 2000 words
    # maps.shape == rm.shape. maps[rid][uid] = index of wm. many-to-one relationship
    # rid: restaurant id. range(0,1,2,...,1600+)
    # uid: user(customer) id. range(0,1,2,...,20000+)
    rm = load_pickle('rm.pkl')
    wm = load_pickle('wm.pkl')
    maps = load_pickle('maps.pkl')

    # a = rm_find_sim_row_list(rm=rm, row=141, column=80)
    # print(type(rm))
    print('real', rm[174][16])
    print('predict', rm_predict(rid=174, uid=16, rm=rm))


def rm_predict(rid, uid, rm):
    # find similar user list
    sim_user = rm_find_sim_row_list(rm=rm.T, row=uid, column=rid)
    # find similar restaurant list
    sim_rest = rm_find_sim_row_list(rm=rm,row=rid, column=uid)
    # chose top 30 similar users and restaurants' score and get the average.
    score = get_score(rest_id=rid,user_id=uid,sim_rest_index_list=sim_rest,sim_user_index_list=sim_user,rm=rm)
    return score


def get_score(rest_id, user_id, sim_user_index_list, sim_rest_index_list,rm):
    # find the average score for 30 similar users chose this restaurant.
    count = 0
    number = 0
    for uid in sim_user_index_list:
        if rm[rest_id][uid] > 0:
            count = count + 1
            number = number + rm[rest_id][uid]
        if count >= 30:
            break
    if count == 0:
        score1 = 0
    else:
        score1 = number / count
    # find the average score for the 30 similar restaurants.
    number = 0
    count = 0
    for rid in sim_rest_index_list:
        if rm[rid][user_id] > 0:
            count = count + 1
            number = number + rm[rid][user_id]
        if count >= 30:
            break
    if count == 0:
        score2 = 0
    else:
        score2 = number / count
    return score1 * 0.5 + score2 * 0.5


# the following method will find the similar row for the given matrix. it will return the sorted
# result. From Euclidean distance. the first one is the most similar one.(smallest value)
def rm_find_sim_row_list(rm, row, column):
    result = dict()
    for i in range(len(rm)):
        if rm[i][column] > 0 and i != row:
            v1, v2 = find_2vector_nonzero_sub(v1=rm[i], v2=rm[row], ignore_index=column)
            sim_score = euclidean_sim(vector1=v1, vector2=v2)
            result[i] = sim_score
    temp = sorted(result.items(), key=lambda kv: kv[1])
    return [i[0] for i in temp]


# find two vectors' nonzero elements and return the two sub vectors.
def find_2vector_nonzero_sub(v1, v2, ignore_index):
    temp_1 = list()
    temp_2 = list()
    for i in range(min(len(v1), len(v2))):
        if i != ignore_index and v1[i] > 0 and v2[i] > 0:
            temp_1.append(v1[i])
            temp_2.append(v2[i])
    return np.array(temp_1), np.array(temp_2)


# def wm_find_sim_row_list(wm, maps, row, column):
#     result = dict()
#     for i in range(len(maps)):
#         if maps[i][column] > -1 and i != row:
#             v1, v2 = find_2vector_nonzero_sub(v1=rm[i], v2=rm[row], ignore_index=column)
#
#             sim_score = euclidean_sim(vector1=v1, vector2=v2)
#             result[i] = sim_score
#     temp = sorted(result.items(), key=lambda kv: kv[1])
#     return [i[0] for i in temp]
#     pass


def wm_predict(rid, uid, maps, wm):

    pass


if __name__ == '__main__':
    start()
    exit()

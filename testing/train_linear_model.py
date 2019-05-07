import pickle
import pprint
import random

import numpy as np
from joblib import dump, load
from sklearn.linear_model import LinearRegression

"""
How to combine the rating based and text based recommendation?
This easiest way is to use linear regression to train the model.
X = [[rating-predict, text-predict], ..... ]
Y = [ [real ], [real ] , ...]
model = LinearRegression()
model.fit(X, y)

So, how to get the rating-based prediction value as well as the text-based prediction?

In testing part, we already have a function called recommendation to get those information. 
For efficiency consideration, we only combine the bag-of-words and rating-based to train the model.
"""


# this training use sklearn package to train.
def model_training():
    # create the training model X.
    X = list()
    Y = list()

    # load training files
    print("Start Training...")
    rm = load_pickle('rm.pkl')
    bag_200 = load_pickle('TFIDF_200.pkl')
    maps = load_pickle('maps.pkl')
    test_set = load_pickle('test_set_1000.pkl')

    model = LinearRegression()
    # for each epoch
    for one in test_set:
        rid = one[0]
        uid = one[1]
        real_score = rm[rid][uid]
        Y.append([real_score])

        bag_200_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=bag_200, maps=maps)
        r_score = rm_predict(rid=rid, uid=uid, rm=rm, alg='cosine')
        X.append([r_score, bag_200_score])
        # train the model
        model.fit(X, Y)
    # store the model into local disk
    dump(model, 'trained_model.joblib')
    pprint.pprint(model.predict([[4.3, 3.5], [2.5, 3.4]]))


"""
sample copy the function from the testing class
"""


def create_test_sample(rm, size=20):
    print('start randomly choose test samples.')
    temp = list()
    result = list()
    for i in range(size):
        uid = random.randint(0, len(rm[0]))

        # get a random real rating index and hide this to predict.
        rid = random.sample([j for j, e in enumerate(np.array(rm).T[uid]) if e != 0], 1)[0]

        temp = [rid, uid]
        result.append(temp)
    # print(result)
    print('Success store the test pickle!')
    output = open('test_set_1000.pkl', 'wb')
    pickle.dump(result, output)
    output.close()


def rm_predict(rid, uid, rm, alg='cosine'):
    # find similar user list
    sim_user = rm_find_sim_row_list(rm=rm.T, row=uid, column=rid, alg=alg)
    # find similar restaurant list
    sim_rest = rm_find_sim_row_list(rm=rm, row=rid, column=uid, alg=alg)
    # chose top 30 similar users and restaurants' score and get the average.
    score = get_score(rest_id=rid, user_id=uid, sim_rest_index_list=sim_rest, sim_user_index_list=sim_user, rm=rm)
    return score


def get_score(rest_id, user_id, sim_user_index_list, sim_rest_index_list, rm):
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
def rm_find_sim_row_list(rm, row, column, alg='cosine'):
    result = dict()
    for i in range(len(rm)):
        if rm[i][column] > 0 and i != row:
            v1, v2 = find_2vector_nonzero_sub(v1=rm[i], v2=rm[row], ignore_index=column)
            if alg == 'euclidean':
                sim_score = euclidean_sim(vector1=v1, vector2=v2)
            elif alg == 'cosine':
                sim_score = cosine_sim(vector1=v1, vector2=v2)
            else:
                sim_score = pearson_sim(vector1=v1, vector2=v2)
            result[i] = sim_score
    temp = sorted(result.items(), key=lambda kv: kv[1])
    # print(temp)
    # return the list of similar rows of the matrix(from high to low).
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


def wm_find_sim_row_list(wm, maps, row, column):
    result = dict()
    for i in range(len(maps)):
        if maps[i][column] > 0 and i != row:
            # v1, v2 = find_2vector_nonzero_sub(v1=rm[i], v2=rm[row], ignore_index=column)
            score = 0
            count = 0
            for j in range(len(maps[i])):
                if maps[i][j] > 0 and maps[row][j] > 0:
                    # find the commen index review
                    # print('find row',i,'and row',row,'have same column', j)
                    textvec1 = wm[int(maps[i][j])]
                    textvec2 = wm[int(maps[row][j])]
                    sim_score = cosine_sim(vector1=np.array(textvec1), vector2=np.array(textvec2))
                    score = score + sim_score
                    count += 1
            result[i] = score / count
    temp = sorted(result.items(), key=lambda kv: -kv[1])
    # print(temp)
    return [i[0] for i in temp]


def wm_predict(rid, uid, maps, wm, rm):
    # find similar user list
    sim_user = wm_find_sim_row_list(wm=wm, maps=maps.T, row=uid, column=rid)
    # find similar restaurant list
    sim_rest = wm_find_sim_row_list(wm=wm, maps=maps, row=rid, column=uid)
    # chose top 30 similar users and restaurants' score and get the average.
    score = get_score(rest_id=rid, user_id=uid, sim_rest_index_list=sim_rest, sim_user_index_list=sim_user, rm=rm)
    return score


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


if __name__ == '__main__':
    model_training()
    # model = load('trained_model.joblib')
    # pprint.pprint(model.predict([[4.3, 3.5], [2.5, 3.4]]))
    exit()

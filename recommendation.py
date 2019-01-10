import pprint, pickle
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import scipy.stats as stats


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

    # test one data rid=141 , uid = 80
    # wm_find_sim_row_list(wm=wm,row=141,column=80,maps=maps)
    # rm_find_sim_row_list(rm=rm,row=141,column=80)

    # test_acc(size=200)
    # test_bag_of_words(size=200)
    # test_TFIDF(size=200)
    test_bag_TFIDF(size=200)


def rm_predict(rid, uid, rm):
    # find similar user list
    sim_user = rm_find_sim_row_list(rm=rm.T, row=uid, column=rid)
    # find similar restaurant list
    sim_rest = rm_find_sim_row_list(rm=rm, row=rid, column=uid)
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
def rm_find_sim_row_list(rm, row, column):
    result = dict()
    for i in range(len(rm)):
        if rm[i][column] > 0 and i != row:
            v1, v2 = find_2vector_nonzero_sub(v1=rm[i], v2=rm[row], ignore_index=column)
            sim_score = euclidean_sim(vector1=v1, vector2=v2)
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


def test_acc(size=10):
    rm = load_pickle('rm.pkl')
    wm = load_pickle('wm.pkl')
    maps = load_pickle('maps.pkl')
    print("Start Testing. Whole testing round:", size)

    # r: rating-based , t: text-based
    r_records = []
    t_records = []
    r_error = []
    t_error = []

    # for each epoch
    for i in range(0, size):
        # get a random user index
        uid = random.randint(0, len(rm[0]))

        # get a random real rating index and hide this to predict.
        rid = random.sample([j for j, e in enumerate(np.array(rm).T[uid]) if e != 0], 1)[0]
        real_score = rm[rid][uid]
        # print(real_score)
        r_score = rm_predict(rid=rid, uid=uid, rm=rm)
        t_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=wm, maps=maps)

        # records parameters:[user_index , restaurant_index , real_rank, predict_rank]
        one = [uid, rid, real_score, r_score]
        two = [uid, rid, real_score, t_score]

        print("Round:", i)

        r_records.append(one)
        t_records.append(two)
        r_error.append(abs(real_score - r_score))
        t_error.append(abs(real_score - t_score))

    print("After test the", size, "samples, mean absolute error (MAE) achieved:")
    print("rating-based:", MAE(r_records))
    print("text-based:", MAE(t_records))
    print('Error distribution for each approach:')
    # print(r_error)
    # print(t_error)

    # plot line histogram diagram
    # y, binEdges = np.histogram(r_error, bins=1)
    # bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
    # plt.plot(bincenters, y, '-')
    # plt.show()

    plt.figure(figsize=[12, 7])
    plt.hist([r_error, t_error], label=['rating-based', 'text-based'], alpha = 0.7)
    plt.title("Histogram: 200 sample")
    plt.xlabel("error")
    plt.ylabel("sample count")
    plt.legend(loc='upper right')
    plt.show()


def test_bag_of_words(size=10):
    print("Start Testing. Whole testing round:", size)

    rm = load_pickle('rm.pkl')
    bag_2000 = load_pickle('bag_of_words_2000.pkl')
    bag_1000 = load_pickle('bag_of_words_1000.pkl')
    bag_500 = load_pickle('bag_of_words_500.pkl')
    bag_200 = load_pickle('bag_of_words_200.pkl')
    maps = load_pickle('maps.pkl')

    # bag_of_words
    bag_2000_records = []
    bag_1000_records = []
    bag_500_records = []
    bag_200_records = []
    bag_2000_error = []
    bag_1000_error = []
    bag_500_error = []
    bag_200_error = []

    # for each epoch
    for i in range(0, size):
        # get a random user index
        uid = random.randint(0, len(rm[0]))

        # get a random real rating index and hide this to predict.
        rid = random.sample([j for j, e in enumerate(np.array(rm).T[uid]) if e != 0], 1)[0]
        real_score = rm[rid][uid]
        # print(real_score)
        # r_score = rm_predict(rid=rid, uid=uid, rm=rm)

        bag_2000_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=bag_2000, maps=maps)
        bag_1000_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=bag_1000, maps=maps)
        bag_500_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=bag_500, maps=maps)
        bag_200_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=bag_200, maps=maps)

        # records parameters:[user_index , restaurant_index , real_rank, predict_rank]
        one = [uid, rid, real_score, bag_2000_score]
        two = [uid, rid, real_score, bag_1000_score]
        three = [uid, rid, real_score, bag_500_score]
        four = [uid, rid, real_score, bag_200_score]

        print("Round:", i)

        bag_2000_records.append(one)
        bag_1000_records.append(two)
        bag_500_records.append(three)
        bag_200_records.append(four)
        bag_2000_error.append(abs(real_score - bag_2000_score))
        bag_1000_error.append(abs(real_score - bag_1000_score))
        bag_500_error.append(abs(real_score - bag_500_score))
        bag_200_error.append(abs(real_score - bag_200_score))

    print("After test the", size, "samples, mean absolute error (MAE) achieved:")
    print("bag_2000:", MAE(bag_2000_records))
    print("bag_1000:", MAE(bag_1000_records))
    print("bag_500:", MAE(bag_500_records))
    print("bag_200:", MAE(bag_200_records))
    print('Error distribution for each approach:')
    # print(r_error)
    # print(t_error)

    # plot line histogram diagram
    # y, binEdges = np.histogram(r_error, bins=1)
    # bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
    # plt.plot(bincenters, y, '-')
    # plt.show()

    plt.figure(figsize=[12, 7])
    plt.hist([bag_2000_error, bag_1000_error,bag_500_error,bag_200_error], label=['size=2000','size=1000','size=500','size=200'], alpha=0.7)
    plt.title("Histogram: 200 sample")
    plt.xlabel("error")
    plt.ylabel("sample count")
    plt.legend(loc='upper right')
    plt.show()


def test_bag_TFIDF(size= 10):
    rm = load_pickle('rm.pkl')
    bag_200 = load_pickle('bag_of_words_200.pkl')
    TFIDF_200 = load_pickle('TFIDF_200.pkl')
    maps = load_pickle('maps.pkl')
    print("Start Testing. Whole testing round:", size)

    # bag , TFIDF
    bag_records = []
    TFIDF_records = []
    bag_error = []
    TFIDF_error = []

    # for each epoch
    for i in range(0, size):
        # get a random user index
        uid = random.randint(0, len(rm[0]))

        # get a random real rating index and hide this to predict.
        rid = random.sample([j for j, e in enumerate(np.array(rm).T[uid]) if e != 0], 1)[0]
        real_score = rm[rid][uid]
        # print(real_score)
        bag_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=bag_200, maps=maps)
        TFIDF_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=TFIDF_200, maps=maps)

        # records parameters:[user_index , restaurant_index , real_rank, predict_rank]
        one = [uid, rid, real_score, bag_score]
        two = [uid, rid, real_score, TFIDF_score]

        print("Round:", i)

        bag_records.append(one)
        TFIDF_records.append(two)
        bag_error.append(abs(real_score - bag_score))
        TFIDF_error.append(abs(real_score - TFIDF_score))

    print("After test the", size, "samples, mean absolute error (MAE) achieved:")
    print("bag-of-words(size=200):", MAE(bag_records))
    print("TFIDF(size=200):", MAE(TFIDF_records))
    print('Error distribution for each approach:')
    # print(r_error)
    # print(t_error)

    # plot line histogram diagram
    # y, binEdges = np.histogram(r_error, bins=1)
    # bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
    # plt.plot(bincenters, y, '-')
    # plt.show()

    plt.figure(figsize=[12, 7])
    plt.hist([bag_error, TFIDF_error], label=['bag-of-words(size=200)', 'TFIDF(size=200)'], alpha=0.7)
    plt.title("Histogram: 200 sample")
    plt.xlabel("error")
    plt.ylabel("sample count")
    plt.legend(loc='upper right')
    plt.show()


def test_TFIDF(size=10):
    print("Start Testing. Whole testing round:", size)

    rm = load_pickle('rm.pkl')
    bag_2000 = load_pickle('TFIDF_2000.pkl')
    bag_1000 = load_pickle('TFIDF_1000.pkl')
    bag_500 = load_pickle('TFIDF_500.pkl')
    bag_200 = load_pickle('TFIDF_200.pkl')
    maps = load_pickle('maps.pkl')

    # bag_of_words
    bag_2000_records = []
    bag_1000_records = []
    bag_500_records = []
    bag_200_records = []
    bag_2000_error = []
    bag_1000_error = []
    bag_500_error = []
    bag_200_error = []

    # for each epoch
    for i in range(0, size):
        # get a random user index
        uid = random.randint(0, len(rm[0]))

        # get a random real rating index and hide this to predict.
        rid = random.sample([j for j, e in enumerate(np.array(rm).T[uid]) if e != 0], 1)[0]
        real_score = rm[rid][uid]
        # print(real_score)
        # r_score = rm_predict(rid=rid, uid=uid, rm=rm)

        bag_2000_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=bag_2000, maps=maps)
        bag_1000_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=bag_1000, maps=maps)
        bag_500_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=bag_500, maps=maps)
        bag_200_score = wm_predict(rid=rid, uid=uid, rm=rm, wm=bag_200, maps=maps)

        # records parameters:[user_index , restaurant_index , real_rank, predict_rank]
        one = [uid, rid, real_score, bag_2000_score]
        two = [uid, rid, real_score, bag_1000_score]
        three = [uid, rid, real_score, bag_500_score]
        four = [uid, rid, real_score, bag_200_score]

        print("Round:", i)

        bag_2000_records.append(one)
        bag_1000_records.append(two)
        bag_500_records.append(three)
        bag_200_records.append(four)
        bag_2000_error.append(abs(real_score - bag_2000_score))
        bag_1000_error.append(abs(real_score - bag_1000_score))
        bag_500_error.append(abs(real_score - bag_500_score))
        bag_200_error.append(abs(real_score - bag_200_score))

    print("After test the", size, "samples, mean absolute error (MAE) achieved:")
    print("TFIDF_2000:", MAE(bag_2000_records))
    print("TFIDF_1000:", MAE(bag_1000_records))
    print("TFIDF_500:", MAE(bag_500_records))
    print("TFIDF_200:", MAE(bag_200_records))
    print('Error distribution for each approach:')
    # print(r_error)
    # print(t_error)

    # plot line histogram diagram
    # y, binEdges = np.histogram(r_error, bins=1)
    # bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
    # plt.plot(bincenters, y, '-')
    # plt.show()

    plt.figure(figsize=[12, 7])
    plt.hist([bag_2000_error, bag_1000_error,bag_500_error,bag_200_error], label=['size=2000','size=1000','size=500','size=200'], alpha=0.7)
    plt.title("Histogram for size of TFIDF: 200 sample")
    plt.xlabel("error")
    plt.ylabel("sample count")
    plt.legend(loc='upper right')
    plt.show()


# records parameters:[user_index , restaurant_index , real_rank, predict_rank]
def RMSE(records):
    return math.sqrt(sum([(rui - pui) * (rui - pui) for u, i, rui, pui in records]) / float(len(records)))


def MAE(records):
    return (sum([abs(rui - pui) for u, i, rui, pui in records])) / float(len(records))


if __name__ == '__main__':
    start()
    exit()

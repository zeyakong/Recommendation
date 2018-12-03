import pprint, pickle
import numpy as np
import math
import random
import matplotlib.pyplot as plt

sim_distance = 0
training_data = []
matrix = []


# test_data = []

def start():
    global matrix, training_data, similarity_rest, similarity_user
    matrix = load_data()
    np.seterr(divide='ignore', invalid='ignore')

    # test
    print("Finish Loading. the matrix shape:", len(matrix), len(matrix[0]))
    print("restaurants: ", len(matrix))
    print("users: ", len(matrix[0]))
    # lens = []
    # count2 = 0
    # for one in matrix:
    #     count = 0
    #     for e in one:
    #         if e > 0:
    #             count = count + 1
    #     if count > 1400:
    #         count2 = count2 + 1
    #     lens.append(count)
    # print("count2,", count2)
    # print('sum:',sum(lens))
    # plt.hist(lens, edgecolor='black', bins=int(50), density=True)
    # plt.title("Density Histogram")
    # plt.xlabel("Review Count")
    # plt.ylabel("Density")
    # plt.show()

    print("\nSplit the matrix into train data-set and test data-set...")
    training_data = matrix
    # test_data = matrix[1300:]
    training_data = np.array(training_data)
    print("Split finished. \n\nsize of training data: ", len(training_data))
    # get_similarity_list(matrix, 24)
    # print("Size of test data:", 200)

    # find average score for 200 similar user

    # print(average, "count:", count)

    print("\nNow test the accuracy:")
    test(100)
    print("Want to predict manually?(y/n)")
    strs = input()
    if strs == 'y':
        predict_one()
    print("Goodbye")
    exit()
    # print("What restaurant score you want to predict for user:")
    # person = "1"
    # print("top match for:", person)
    #
    # print(top_matches(matrix, person))
    # print(get_recommendations(matrix, person))


def load_data():
    print("Load the rating matrix...")
    pkl_file = open('matrix.pkl', 'rb')

    data = pickle.load(pkl_file)
    # pprint.pprint(data)
    pkl_file.close()
    return data


def o_similarity(vector1, vector2):
    # o distance
    o_distance = np.linalg.norm(vector1 - vector2)
    return 1 / (1 + o_distance)


def cos_similarity(vector1, vector2):
    # calculate cos_distance
    cos_distance = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * (np.linalg.norm(vector2)))
    # normalize
    return 0.5 + 0.5 * cos_distance


def pearson_similarity(vector1, vector2):
    return 0.5 + 0.5 * np.corrcoef(vector1, vector2)[0][1]


def get_similarity_list(matrix, index, tar):
    list1 = []
    list2 = []
    list3 = []

    # for i in [j for j, e in enumerate(np.array(matrix)[index]) if e != 0]:
    for i in range(0, len(matrix)):
        temp_1 = []
        temp_2 = []
        if i != index and matrix[i][tar] > 0:
            # get common vector value
            for j in range(0, len(matrix[i])):
                if matrix[index][j] > 0 and matrix[i][j] > 0:
                    temp_1.append(matrix[index][j])
                    temp_2.append(matrix[i][j])
            if len(temp_1) > 0 and len(temp_2) > 0:
                vector1 = np.array(temp_1)
                vector2 = np.array(temp_2)
                # print(vector1,'\n',vector2)

                s1 = o_similarity(vector1, vector2)
                s2 = cos_similarity(vector1, vector2)
                s3 = pearson_similarity(vector1, vector2)
                list1.append(s1)
                list2.append(s2)
                list3.append(s3)
            else:
                list1.append(0)
                list2.append(0)
                list3.append(0)
        else:
            list1.append(0)
            list2.append(0)
            list3.append(0)
    return list1, list2, list3


def liner_classification():
    pass


def predict_one():
    print("\nInput the restaurant index you want to calculate:")
    restaurant_index = int(input())
    print("\nInput the user index you want to calculate:")
    user_index = int(input())
    # for i in range(0, 200):
    #     for j in range(0, 200):
    #         if matrix[i][j] > 0:
    #             print(i, j)

    # predict parameters: restaurant_id, user_id, algorithm{'o''c''p'} which means euclidean, cos, pearson
    o_score, cos_score, pearson_score = predict(restaurant_index, user_index, 'all')
    print("The predict score for user", user_index, "to choose restaurant", restaurant_index,
          ":\n(Pearson correlation)",
          pearson_score, "\n(Cosine)",
          cos_score,

          "\n(Euclidean Distance)", o_score)
    if matrix[restaurant_index][user_index] > 0:
        print("Dose it exist a real rating? Yes,the rating is:", matrix[restaurant_index][user_index])
    else:
        print("Dose it exist a real rating? No")


def test(size=200):
    print("Start Testing. Whole testing round:", size)
    o_records = []
    cos_records = []
    pearson_records = []
    o_error = []
    cos_error = []
    pearson_error = []
    for i in range(0, size):
        # get a random user index
        uid = random.randint(0, len(matrix[0]))
        # print("Testing round:", i, ",the random user", uid, "...")
        # get a random real rating index and hide this to predict.
        rid = random.sample([j for j, e in enumerate(np.array(matrix).T[uid]) if e != 0], 1)[0]
        real_score = matrix[rid][uid]
        # print(real_score)
        o_score, cos_score, pearson_score = predict(rid, uid, 'all')
        # records parameters:[user_index , restaurant_index , real_rank, predict_rank]
        one = [uid, rid, real_score, o_score]
        two = [uid, rid, real_score, cos_score]
        three = [uid, rid, real_score, pearson_score]
        o_records.append(one)
        cos_records.append(two)
        pearson_records.append(three)
        o_error.append(abs(real_score-o_score))
        cos_error.append(abs(real_score - cos_score))
        pearson_error.append(abs(real_score - pearson_score))

    print("After test the", size, "samples, Root mean squared error (RMSE) achieved:")
    print("Using Euclidean distance:", RMSE(o_records))
    print("Using cosine:", RMSE(cos_records))
    print("Using pearson:", RMSE(pearson_records))
    print('Error distribution for each approach:')
    # bins = np.linspace(0, 10, 10)
    plt.hist([o_error,cos_error,pearson_error],  alpha=0.5, label=['E', 'c','P'])
    # plt.hist(, bins, alpha=0.5, label='cosine')
    # plt.hist(, bins, alpha=0.5, label='Pearson')
    plt.title("Density Histogram")
    plt.xlabel("error")
    plt.ylabel("sample count")
    plt.legend(loc='upper right')
    plt.show()


def get_accuracy(records):
    pass


# records parameters:[user_index , restaurant_index , real_rank, predict_rank]
def RMSE(records):
    return math.sqrt(sum([(rui - pui) * (rui - pui) for u, i, rui, pui in records]) / float(len(records)))


def MAE(records):
    return sum([abs(rui - pui) for u, i, rui, pui in records])


def predict(restaurant_index, user_index, algorithm):
    # print("Calculating...")
    # print("Calculating the similarity for restaurant:", int(restaurant_index), ", user: ", int(user_index), "...")
    o_sim_rest_list, cos_sim_rest_list, pearson_sim_rest_list = get_similarity_list(training_data,
                                                                                    int(restaurant_index),
                                                                                    int(user_index))
    training_data_transpose = training_data.transpose()
    o_sim_user_list, cos_sim_user_list, pearson_sim_user_list = get_similarity_list(training_data_transpose,
                                                                                    int(user_index),
                                                                                    int(restaurant_index))

    o_sim_rest_index_list = np.array(o_sim_rest_list).argsort()[::-1]
    o_sim_user_index_list = np.array(o_sim_user_list).argsort()[::-1]
    o_score = get_score(restaurant_index, user_index, o_sim_user_index_list, o_sim_rest_index_list)

    cos_sim_rest_index_list = np.array(cos_sim_rest_list).argsort()[::-1]
    cos_sim_user_index_list = np.array(cos_sim_user_list).argsort()[::-1]
    cos_score = get_score(restaurant_index, user_index, cos_sim_user_index_list, cos_sim_rest_index_list)

    pearson_sim_rest_index_list = np.array(pearson_sim_rest_list).argsort()[::-1]
    pearson_sim_user_index_list = np.array(pearson_sim_user_list).argsort()[::-1]
    pearson_score = get_score(restaurant_index, user_index, pearson_sim_user_index_list, pearson_sim_rest_index_list)
    if algorithm == 'p':
        return pearson_score
    elif algorithm == 'o':
        return o_score
    elif algorithm == 'c':
        return cos_score
    else:
        return o_score, cos_score, pearson_score


def get_score(restaurant_index, user_index, sim_user_index_list, sim_rest_index_list):
    # find the average score for 30 similar users chose this restaurant.
    count = 0
    number = 0
    for uid in sim_user_index_list:
        if matrix[restaurant_index][uid] > 0:
            count = count + 1
            number = number + matrix[restaurant_index][uid]
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
        if matrix[rid][user_index] > 0:
            count = count + 1
            number = number + matrix[rid][user_index]
        if count >= 30:
            break
    if count == 0:
        score2 = 0
    else:
        score2 = number / count
    return score1 * 0.5 + score2 * 0.5


if __name__ == '__main__':
    start()

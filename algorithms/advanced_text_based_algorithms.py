import collections
import pprint
import time

from gensim.models import KeyedVectors
from joblib import load
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords

from algorithms.algorithm_utils import load_pickle, find_sub_matrix, recommend_restaurant
from algorithms.rating_based_algorithms import rating_recommend
from algorithms.text_based_algorithms import text_recommend
from users.models import UserReview, User

"""
This Python file provides some text-based algorithms: word2vec, Doc2vec and ....
Only support cosine similarity
"""


def test():
    filename = '../GoogleNews-vectors-negative300.bin'
    model = KeyedVectors.load_word2vec_format(filename, binary=True)
    # result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
    print(model.n_similarity('I love you'.lower().split(), 'fuck you'.lower().split()))
    print('finished...')
    start = time.time()
    print(model.n_similarity('icecream I like apple apple apple'.lower().split(), 'hello you'.lower().split()))
    end = time.time()
    print(end - start)


def load_word2vec_model(filename):
    binary = False
    pre_path = 'algorithms/'
    if filename == 'GoogleNews-vectors-negative300.bin':
        binary = True
    return KeyedVectors.load_word2vec_format(pre_path + filename, binary=binary)


def word2vec_recommend(username, model):
    # find submatrix first
    user_restaurant_list = list()  # the restaurants the user went before.
    user_dict = dict()  # dict: user[business_id] = text_review
    user_text_list = list()  # the users text reviews list orders by user_dict
    user_review_list = UserReview.objects.filter(user=User.objects.get(username=username))

    for one_review in user_review_list:
        user_dict[one_review.business_id] = one_review.text
        user_restaurant_list.append(one_review.business_id)
        user_text_list.append(one_review.text)

    # now we have the user's text vector and we can calculate the similarity
    """
       first find the unrecorded restaurant
       find similar users from the dataset
       1. find the users list which the new user and customers have [threshold] common rating.
       this function is a recursive function: first the min of user_vector is 5,
       so, the threshold is 80% : 4.
    """

    # load text_matrix
    text_matrix = load_pickle('algorithms/text_matrix.pkl')
    threshold = len(user_restaurant_list) - 1  # means # of the common rating
    sub_matrix = find_sub_matrix(user_dict, text_matrix, threshold)
    while len(sub_matrix.keys()) < 30:
        threshold = threshold - 1
        sub_matrix = find_sub_matrix(user_dict, text_matrix, threshold)
    pprint.pprint(len(sub_matrix))

    # now we got the sub matrix and we can process
    similarity = dict()
    for one_similar_user in sub_matrix.keys():
        customer_total_text = ""
        user_total_text = ""
        for one_restaurant in user_restaurant_list:
            if one_restaurant in sub_matrix[one_similar_user]:
                customer_total_text = customer_total_text + ' ' + sub_matrix[one_similar_user][one_restaurant]
                user_total_text = user_total_text + ' ' + user_dict[one_restaurant]
        # now we have two list: user_total_text and customer_total. we can calculate the similarity
        # in word2vec n_similarity.
        sim_score = 0
        # tokenize the text
        customer_tokens = tokenizer(customer_total_text, model)
        user_tokens = tokenizer(user_total_text, model)

        similarity[one_similar_user] = model.n_similarity(customer_tokens, user_tokens)
    # get top 15 similar users
    top_similar_users = collections.Counter(similarity).most_common(15)
    return top_similar_users, recommend_restaurant(similarity, user_dict)


def tokenizer(input_text, wv_model):
    # get tokens
    tokens = word_tokenize(input_text)
    clean_tokens = list()
    for token in tokens:
        if token.lower() in wv_model.wv.vocab:
            clean_tokens.append(token.lower())
    return clean_tokens


def linear_regression_model(username, similarity_method='cosine', method='bag_of_words'):
    similar_user_text_based, similar_restaurant_text_based = text_recommend(username=username, method=method,
                                                                            similarity_method=similarity_method)
    similar_user_rating_based, similar_restaurant_rating_based = rating_recommend(username,
                                                                                  similarity_method=similarity_method)
    # load linear regression model
    liner_regression_model = load('algorithms/trained_model.joblib')
    # prepare the X values, first find all the restaurant list.
    restaurant_list = list()
    for one in range(len(similar_restaurant_rating_based)):
        if similar_restaurant_rating_based[one][0] not in restaurant_list:
            restaurant_list.append(similar_restaurant_rating_based[one][0])
        if similar_restaurant_text_based[one][0] not in restaurant_list:
            restaurant_list.append(similar_restaurant_text_based[one][0])
    result = dict()
    X = list()
    for one_rest in restaurant_list:
        # get rating score
        r_score = get_score(similar_restaurant_rating_based, one_rest)
        t_score = get_score(similar_restaurant_text_based, one_rest)
        X.append([r_score, t_score])
    # use model to predict
    Y = liner_regression_model.predict(X)
    count = 0
    for one in restaurant_list:
        result[one] = Y[count][0]
        count = count + 1
    return similar_user_rating_based, similar_user_text_based, collections.Counter(result).most_common(5)


def get_score(similar_restaurants, restaurant_id):
    for one in similar_restaurants:
        if restaurant_id == one[0]:
            return one[1]
    return 0

# if __name__ == '__main__':
#     print('loading...')
#     model = load_word2vec_model('glove.6B.50d.txt.word2vec')
#     print('Finish loading')
#     start = time.time()
#     simi_user, simi_rec = word2vec_recommend('123', model)
#     end = time.time()
#     print(end - start)
#     pprint.pprint(simi_rec)
#     pprint.pprint(simi_user)
#     exit()

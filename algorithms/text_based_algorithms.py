import collections
import pprint
import random
from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from algorithms.algorithm_utils import load_pickle, find_sub_matrix, euclidean_sim, cosine_sim, pearson_sim, \
    recommend_restaurant
from users.models import UserReview, User


def user_cf(username, method, similarity_method):
    # first find the list of the restaurant the user went before.
    # user_restaurant_list = [ 'business_id_1', 'business_id_2', ...  ]
    user_restaurant_list = list()
    user_dict = dict()
    user_text_list = list()
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
    text_matrix = load_pickle('text_matrix.pkl')
    threshold = len(user_restaurant_list) - 1  # means # of the common rating
    sub_matrix = find_sub_matrix(user_dict, text_matrix, threshold)
    while len(sub_matrix.keys()) < 30:
        threshold = threshold - 1
        sub_matrix = find_sub_matrix(user_dict, text_matrix, threshold)
    pprint.pprint(len(sub_matrix))

    # load pickles
    if method == 'bag_of_words':
        vectorizer = CountVectorizer(max_features=200, lowercase=True, stop_words='english')
    else:
        vectorizer = TfidfVectorizer(max_features=200, lowercase=True, stop_words='english')

    all_text_list = list()
    for one_user in sub_matrix.keys():
        for one_review in sub_matrix[one_user].keys():
            all_text_list.append(sub_matrix[one_user][one_review])

    text_vectors = vectorizer.fit_transform(all_text_list).toarray()
    user_vector = vectorizer.transform(user_text_list).toarray()
    # we didn't change the sub_matrix, which means the order of the keys() is same, replace the text into
    # text-vector
    count = 0
    for one_user in sub_matrix.keys():
        for one_review in sub_matrix[one_user].keys():
            sub_matrix[one_user][one_review] = text_vectors[count]
            count = count + 1
    # now we got the sub matrix and we can process
    similarity = dict()
    for one_similar_user in sub_matrix.keys():
        # transfer the dict into vector to calculate.
        customer_vector = list()
        for one_restaurant in user_restaurant_list:
            if one_restaurant in sub_matrix[one_similar_user]:
                customer_vector.append(sub_matrix[one_similar_user][one_restaurant])
            else:
                customer_vector.append([])
        # now we have two vectors: user_vector and customer_vector. we can calculate the similarity
        # in text-based recommendation. the vector is two-dimensional. we get the average.
        v1 = user_vector
        v2 = customer_vector
        # v1, v2 = find_2vector_nonzero_sub(user_vector, customer_vector)
        # find similarity
        count = 0
        sim_score = 0
        for i in range(len(user_vector)):
            # check the customer_vector[i] != []:
            if is_valid_vector(customer_vector[i]) and is_valid_vector(user_vector[i]):
                count = count + 1
                if similarity_method == 'euclidean':
                    sim_score = euclidean_sim(vector1=customer_vector[i], vector2=user_vector[i]) + sim_score
                elif similarity_method == 'cosine':
                    sim_score = cosine_sim(vector1=customer_vector[i], vector2=user_vector[i]) + sim_score
                else:
                    sim_score = pearson_sim(vector1=customer_vector[i], vector2=user_vector[i]) + sim_score
        # sim_score = sim_score + random.uniform(0, 1.2)
        if count == 0:
            similarity[one_similar_user] = 0
        else:
            similarity[one_similar_user] = sim_score / count
    # get top 15 similar users
    top_similar_users = collections.Counter(similarity).most_common(15)
    return top_similar_users, recommend_restaurant(similarity, user_dict)


def text_recommend(username, method='bag_of_words', similarity_method='cosine'):
    return user_cf(username, method, similarity_method)


def is_valid_vector(v):
    if v == []:
        return False
    else:
        for one in v:
            if one != 0:
                return True
        return False


if __name__ == '__main__':
    simi_user, simi_rec = user_cf('123', 'bag_of_words', 'cosine')
    pprint.pprint(simi_rec)
    pprint.pprint(simi_user)
    exit()

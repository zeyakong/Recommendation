import collections
import pprint
import random
from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from algorithms.algorithm_utils import load_pickle, find_sub_matrix, euclidean_sim, cosine_sim, pearson_sim, \
    recommend_restaurant
from restaurant.models import Review
from users.models import UserReview, User


def user_cf(username, method, similarity_method):
    # load pickles
    if method == 'bag_of_words':
        vectorizer = CountVectorizer(max_features=200, lowercase=True, stop_words='english')
    elif method == 'tfidf':
        vectorizer = TfidfVectorizer(max_features=200, lowercase=True, stop_words='english')
    else:
        vectorizer = CountVectorizer(max_features=200, lowercase=True, stop_words='english')
    # get the user vector, the user is the system new user, so, it is from the userReviews model
    user_review_list = UserReview.objects.filter(user=User.objects.get(username=username))

    user_text_list = list()
    for one_review in user_review_list:
        user_text_list.append(one_review.text)

    # get all texts.
    text_list = []
    review_list = Review.objects.all()
    for var in review_list:
        text_list.append(var.text)
    result = vectorizer.fit_transform(text_list).toarray()
    index = 0
    text_matrix = defaultdict(dict)
    for var in review_list:
        text_matrix[var.user_id][var.business_id] = result[index]
        index = index + 1

    user_vector = vectorizer.transform(user_text_list).toarray()

    # add the vector into the dict
    user_dict = dict()
    # indicate the restaurant that user went
    restaurant_keys = list()
    count = 0
    for one_review in user_review_list:
        user_dict[one_review.business_id] = user_vector[count]
        restaurant_keys.append(one_review.business_id)
        count = count + 1

    # now we have the user's text vector and we can calculate the similarity
    """
       first find the unrecorded restaurant
       find similar users from the dataset
       1. find the users list which the new user and customers have [threshold] common rating.
       this function is a recursive function: first the min of user_vector is 5, 
       so, the threshold is 80% : 4.
       """
    threshold = len(user_dict.keys()) - 1  # means # of the common rating
    sub_matrix = find_sub_matrix(user_dict, text_matrix, threshold)
    while len(sub_matrix.keys()) < 30:
        threshold = threshold - 1
        sub_matrix = find_sub_matrix(user_dict, text_matrix, threshold)

    # now we got the sub matrix and we can process
    similarity = dict()
    for one_similar_user in sub_matrix.keys():
        # transfer the dict into vector to calculate.
        customer_vector = list()
        for one_restaurant in restaurant_keys:
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
        similarity[one_similar_user] = sim_score / count
    # get top 15 similar users
    top_similar_users = collections.Counter(similarity).most_common(15)

    # now we found similar 15 users and we can generate the recommendation like rating based.
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


# if __name__ == '__main__':
#     simi_user, simi_rec = user_cf('123', 'tfidf', 'cosine')
#     pprint.pprint(simi_rec)
#     pprint.pprint(simi_user)
#     exit()

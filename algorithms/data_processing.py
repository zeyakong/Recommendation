import pickle
import pprint
from collections import defaultdict

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from restaurant.models import Business, Review


def create_rating_matrix():
    rating_matrix = defaultdict(dict)
    # get all reviews
    review_list = Review.objects.all()
    print('Start creating star ratings matrix...')
    for one_review in review_list:
        rating_matrix[one_review.user_id][one_review.business_id] = one_review.stars

    filename = 'rating_matrix.pkl'
    output = open(filename, 'wb')
    pickle.dump(rating_matrix, output)
    output.close()
    print('Finish creating, output file name:', filename, 'len of the matrix: ', len(rating_matrix))


def create_bag_of_words_matrix():
    # get all texts.
    text_list = []
    review_list = Review.objects.all()
    for var in review_list:
        text_list.append(var.text)
        # user_list.append(var.user_id)
        # busi_list.append(var.business_id)
    vectorizer = CountVectorizer(max_features=200, lowercase=True, stop_words='english')
    result = vectorizer.fit_transform(text_list).toarray()
    index = 0
    bag_of_words_matrix = defaultdict(dict)
    for var in review_list:
        bag_of_words_matrix[var.user_id][var.business_id] = result[index]
        index = index + 1
    print('index = ', index)
    filename = 'bag_of_words_200_matrix.pkl'
    output = open(filename, 'wb')
    pickle.dump(bag_of_words_matrix, output)
    output.close()
    print('Finish creating, output file name:', filename, 'len of the matrix: ', len(bag_of_words_matrix))


def create_tfidf_matrix():
    # get all texts.
    text_list = []
    review_list = Review.objects.all()
    for var in review_list:
        text_list.append(var.text)
        # user_list.append(var.user_id)
        # busi_list.append(var.business_id)
    vectorizer = TfidfVectorizer(max_features=200, lowercase=True, stop_words='english')
    result = vectorizer.fit_transform(text_list).toarray()
    index = 0
    tfidf_matrix = defaultdict(dict)
    for var in review_list:
        tfidf_matrix[var.user_id][var.business_id] = result[index]
        index = index + 1
    print('index = ', index)
    filename = 'tfidf_200_matrix.pkl'
    output = open(filename, 'wb')
    pickle.dump(tfidf_matrix, output)
    output.close()
    print('Finish creating, output file name:', filename, 'len of the matrix: ', len(tfidf_matrix))


def create_features_list():
    text_list = []
    review_list = Review.objects.all()
    for var in review_list:
        text_list.append(var.text)
        # user_list.append(var.user_id)
        # busi_list.append(var.business_id)
    vectorizer = CountVectorizer(max_features=200, lowercase=True, stop_words='english')
    vectorizer.fit_transform(text_list)
    # print(vectorizer.get_feature_names() == vectorizer2.get_feature_names())
    # both bag-of-words and tfidf have same top 200 features. So, only export one list is ok.
    filename = 'features_200.pkl'
    output = open(filename, 'wb')
    pickle.dump(vectorizer.get_feature_names(), output)
    output.close()
    print('Finish creating, output file name:', filename, 'len of the matrix: ', len(vectorizer.get_feature_names()))


def create_text_matrix():
    text_matrix = defaultdict(dict)
    # get all reviews
    review_list = Review.objects.all()
    print('Start creating text reviews matrix...')
    for one_review in review_list:
        text_matrix[one_review.user_id][one_review.business_id] = one_review.text

    filename = 'text_matrix.pkl'
    output = open(filename, 'wb')
    pickle.dump(text_matrix, output)
    output.close()
    print('Finish creating, output file name:', filename, 'len of the matrix: ', len(text_matrix))


if __name__ == '__main__':
    # create_text_matrix()
    exit()

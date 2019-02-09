from restaurant.models import Customer, Review, Business
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import matplotlib.pyplot as plt
import pandas as pd
import pickle


def get_data():
    text_list = []
    user_list = []
    busi_list = []
    review_list = Review.objects.all()
    for var in review_list:
        text_list.append(var.text)
        user_list.append(var.user_id)
        busi_list.append(var.business_id)
    return text_list, user_list, busi_list

                
def get_text():
    text_list = []
    # user_list = []
    # busi_list = []
    review_list = Review.objects.all()
    for var in review_list:
        text_list.append(var.text)
        # user_list.append(var.user_id)
        # busi_list.append(var.business_id)
    return text_list


def load_pickle(file):
    print("Load the",file,"matrix...")
    pkl_file = open(file, 'rb')
    data = pickle.load(pkl_file)
    # pprint.pprint(data)
    pkl_file.close()
    return data


def get_keywords(input_text):
    # get tokens
    tokens = word_tokenize(input_text)

    # create noise list and stopwords list
    noise_list = [',', '.', ';', '...', '?', ':', '!', '-', '\n', '\\\\', '(', ')', '--', '\'', '\"', '\'\'']
    sr = stopwords.words('english')
    noise_list = noise_list + sr

    # create the PorterStemmer: playing -> play
    stemmer = PorterStemmer()
    clean_tokens = list()
    for token in tokens:
        if token.lower() not in noise_list:
            clean_tokens.append(stemmer.stem(token.lower()))
    return clean_tokens


def start():
    # nltk.download()
    rating_matrix = load_pickle()
    maps = np.zeros(rating_matrix.shape)

    # get all this categories business
    business_list = Business.objects.all()
    # user_list = Customer.objects.all()
    review_list = Review.objects.all()

    blist = []
    for var in business_list:
        blist.append(var.business_id)

    ulist = []
    for var in review_list:
        if var.user_id not in ulist:
            ulist.append(var.user_id)

    text_list, uid_list, rid_list = get_data()
    print('Get', len(text_list), 'text reviews.\nStart finding keywords for each review...')
    #
    for i in range(len(uid_list)):
        res_index = blist.index(rid_list[i])
        user_index = ulist.index(uid_list[i])
        maps[res_index][user_index] = i

    print(maps)
    output = open('maps.pkl', 'wb')
    pickle.dump(maps, output)
    output.close()

    # words_list = list()
    # for one in text_list[0:1000]:
    #     words_list = words_list + get_keywords(one)
    # print('Finished! len of the words list', len(words_list))
    # print()

    # vectorizer = CountVectorizer()
    # X = vectorizer.fit_transform(text_list)
    # print(vectorizer.get_feature_names())
    # print(X.toarray().shape)

    # fre = Counter(words_list)
    # print(len(fre))

    # fre = fre.most_common(15)
    # x, y = zip(*fre)
    # plt.figure(figsize=(15, 8))
    # plt.bar(x,y,edgecolor='black')
    # plt.ylabel('Times')
    # plt.xlabel('Word')
    # print(fre)
    # for one in fre:
    #     print(one)
    #
    # df = pd.DataFrame(fre)
    # print(df)
    # df.drop(df.columns[1:], inplace=True)

    # df.plot(kind='bar')

    # plt.show()


def get_words_vec():
    text_list = get_text()
    # text_list = ['I like you free good',
    #              'I hate you bade good',
    #              'how are you, good ,street bade ']
    vectorizer = CountVectorizer(max_features=200, lowercase=True, stop_words='english')
    X = vectorizer.fit_transform(text_list)

    # print(vectorizer.get_feature_names())
    # print(X.toarray().shape)

    # print(vectorizer.vocabulary_)
    output = open('bag_of_words_200.pkl', 'wb')
    pickle.dump(X.toarray(), output)
    output.close()


def get_doc_vec_by_word2vec():
    text_list = get_text()
    result = list()
    words_embedding = load_pickle('words_embedding_300d.pkl')
    for one in text_list:
        tokens = get_keywords(one)
        for ones in tokens:
            if ones in words_embedding:
                temp = words_embedding[ones]





def get_words_TFIDF():
    text_list = get_text()
    # text_list = ['I like you free good',
    #              'I hate you bade good',
    #              'how are you, good ,street bade ']

    vectorizer= TfidfVectorizer(stop_words='english', lowercase=True, max_features=200)

    X = vectorizer.fit_transform(text_list)
    output = open('TFIDF_200.pkl', 'wb')
    pickle.dump(X.toarray(), output)
    output.close()

    # print(vectorizer.get_feature_names())
    # print(X.toarray().shape)

    # print(vectorizer.vocabulary_)
    # output = open('word2vec.pkl', 'wb')
    # pickle.dump(X.toarray(), output)
    # output.close()


def print_top_n_words():
    text_list = get_text()
    vectorizer = CountVectorizer(max_features=2000, lowercase=True, stop_words='english')
    X = vectorizer.fit_transform(text_list)
    sum_words = X.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    # print(type(words_freq))
    x = []
    y = []
    for one in words_freq[0:15]:
        x.append(one[0])
        y.append(one[1])
    plt.figure(figsize=[12, 7])
    plt.bar(x, y)
    plt.show()


def store_top_n_words(filename, size=2000):
    text_list = get_text()
    vectorizer = CountVectorizer(max_features=2000, lowercase=True, stop_words='english')
    X = vectorizer.fit_transform(text_list)
    sum_words = X.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    # print(words_freq)
    x = []
    for one in words_freq[0:2000]:
        x.append(one[0])
    output = open(filename, 'wb')
    pickle.dump(x, output)
    output.close()


def test():
    # maps[r_index][u_index] = text_index
    maps = load_pickle('maps.pkl')
    # rm: rating matrix . rm[r_index][u_index] = rating(1~5)
    rm = load_pickle('matrix.pkl')
    # for i in range(len(rm[45])):
    #     if rm[45][i]>0:
    #         print(i)
    # print(maps[45][26145])


if __name__ == '__main__':
    # a = load_pickle('maps.pkl')
    # print(a)
    # print('shape',a.shape)
    # get_words_TFIDF()
    # store_top_n_words('top_2000_words.pkl')
    # print(get_keywords('i DSADA NI MA hi Everty'))

    # start()
    # get_words_vec()
    # sr = stopwords.words('english')
    # print(sr)
    # test()
    # test_str = "I won't like this working work street. I played football played by others"
    # print(get_keywords(test_str))
    exit()

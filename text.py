from restaurant.models import Customer, Review, Business
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd


def get_text_list():
    result = []
    review_list = Review.objects.all()
    for var in review_list:
        result.append(var.text)
    return result


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

    text_list = get_text_list()
    print('Get', len(text_list), 'text reviews.\nStart finding keywords for each review...')

    words_list = list()
    for one in text_list[0:2000]:
        words_list = words_list + get_keywords(one)
    print('Finished! len of the words list', len(words_list))
    # print()
    fre = Counter(words_list)
    print(len(fre))
    fre = fre.most_common(15)
    x, y = zip(*fre)
    plt.figure(figsize=(15, 8))
    plt.bar(x,y,edgecolor='black')
    plt.ylabel('Times')
    plt.xlabel('Word')
    # print(fre)
    # for one in fre:
    #     print(one)
    #
    # df = pd.DataFrame(fre)
    # print(df)
    # df.drop(df.columns[1:], inplace=True)

    # df.plot(kind='bar')

    plt.show()


if __name__ == '__main__':
    start()
    # sr = stopwords.words('english')
    # print(sr)
    # test_str = "I won't like this working work street. I played football played by others"
    # print(get_keywords(test_str))
    exit()
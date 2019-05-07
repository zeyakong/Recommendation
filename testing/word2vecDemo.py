from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import time
import pickle
import numpy as np


def load_pickle(pickle_name):
    print("Load the ", pickle_name, " matrix...")
    pkl_file = open(pickle_name, 'rb')
    data = pickle.load(pkl_file)
    # pprint.pprint(data)
    pkl_file.close()
    return data


def start():
    # run_glove_word2vec()
    get_word2vec_vector()


def get_word2vec_vector():
    # load top words list
    top_words = load_pickle('top_2000_words.pkl')

    print('Start saving...')
    start = time.time()
    filename = 'GoogleNews-vectors-negative300.bin'
    model = KeyedVectors.load_word2vec_format(filename, binary=True)
    result = {}
    count = 1
    not_count = 0
    for one in top_words:
        print('Saving', count, '...')
        if one in model.vocab:
            result[one] = model[one]
        else:
            result[one] = np.zeros((300,), dtype=int)
            not_count = not_count+1
        count = count + 1
    print('Finish, not count:',not_count)
    end = time.time()
    print('time:', end - start)

    # save result into desk
    output = open('words_embedding_300d.pkl', 'wb')
    pickle.dump(result, output)
    output.close()


def run_google_word2vec():
    start = time.time()
    filename = 'GoogleNews-vectors-negative300.bin'
    model = KeyedVectors.load_word2vec_format(filename, binary=True)
    # result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
    print(model.n_similarity('I love you'.lower().split(),'you like me'.lower().split()))
    end = time.time()
    print('time:', end - start)


def run_glove_word2vec():
    # glove_input_file = 'glove.6B.300d.txt'
    # word2vec_output_file = 'glove.6B.300d.txt.word2vec'
    # glove2word2vec(glove_input_file, word2vec_output_file)
    start = time.time()

    # load the Stanford GloVe model
    filename = 'glove.6B.50d.txt.word2vec'
    model = KeyedVectors.load_word2vec_format(filename, binary=False)
    # model.wv.save_word2vec_format('model.bin')
    # calculate: (king - man) + woman = ?
    # result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
    vec1 = model['food']
    vec2 = model['happy']
    print(vec1)
    print(vec2)
    print(vec1 + vec2)
    end = time.time()
    print('time:', end - start)


if __name__ == '__main__':
    run_glove_word2vec()
    exit()

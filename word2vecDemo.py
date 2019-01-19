from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import time


def start():
    # run_google_word2vec()
    run_glove_word2vec()

def run_google_word2vec():
    start = time.time()
    filename = 'GoogleNews-vectors-negative300.bin'
    model = KeyedVectors.load_word2vec_format(filename, binary=True)
    # result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
    print(model['man'])
    end = time.time()
    print('time:', end-start)


def run_glove_word2vec():
    start = time.time()
    # glove_input_file = 'glove.6B.50d.txt'
    # word2vec_output_file = 'glove.6B.50d.txt.word2vec'
    # glove2word2vec(glove_input_file, word2vec_output_file)

    # load the Stanford GloVe model
    filename = 'glove.6B.50d.txt.word2vec'
    model = KeyedVectors.load_word2vec_format(filename, binary=False)
    # model.wv.save_word2vec_format('model.bin')

    # calculate: (king - man) + woman = ?
    # result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
    print(model['king'])
    end = time.time()
    print('time:', end - start)


if __name__ == '__main__':
    start()

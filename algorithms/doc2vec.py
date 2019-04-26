import pprint
from gensim.test.utils import common_texts

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

# tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]
# model = Doc2Vec(tagged_data, vector_size=5, window=2, min_count=1, workers=4)
#
# test_data = word_tokenize("I love chatbots".lower())
# test_data2 = word_tokenize("hello afternoon".lower())
# pprint.pprint(model.n_similarity(['good', 'morning', 'hello'], ['hello', 'name']))
from restaurant.models import Review
from gensim.test.utils import get_tmpfile


def train_doc2vec_model():
    # get all text review
    print('loading data...')
    review_list = Review.objects.all()
    corpus = list()
    for one in review_list:
        # tokenizer
        one_text_token = word_tokenize(one.text)
        corpus.append(one_text_token)
    print("Finish loading corpus")

    print('Start training the model...')
    # start training the model
    tagged_data = [TaggedDocument(doc, [i]) for i, doc in enumerate(corpus)]

    model = Doc2Vec(tagged_data, vector_size=50, window=8, min_count=1, workers=4)
    # reduce size
    model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
    # save the model into desk
    model.save('doc2vec_model.50d')
    print('Finish storing')


def load_doc2vec_model():
    model = Doc2Vec.load('doc2vec_model.50d')
    # pprint.pprint(model.wv.n_similarity(['like','restaurant'], ['restaurant','good']))

if __name__ == '__main__':
    load_doc2vec_model()
    exit()

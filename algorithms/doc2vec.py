import pprint

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

data = ['hello, my name is phuck',
        'good morning',
        'good afternoon',
        'hello, my name is phuck',
        'good morning',
        'good afternoon',
        ]

tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]
model = Doc2Vec(tagged_data, vector_size=5, window=2, min_count=1, workers=4)

# test_data = word_tokenize("I love chatbots".lower())
# test_data2 = word_tokenize("hello afternoon".lower())
# pprint.pprint(model.n_similarity(['good','morning','hello'],['hello','name']))


exit()
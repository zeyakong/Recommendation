import pprint

from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
from gensim.similarities import Similarity

index_tmpfile = get_tmpfile("index")
query = [(1, 2)]

index = Similarity(index_tmpfile, common_corpus, num_features=len(common_dictionary))  # build the index

similarities = index[query]  # get similarities between the query and all index documents



exit()

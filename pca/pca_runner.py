import operator
import itertools
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# key_list1 = itertools.islice(sorted(dict_of_bigrams.items(), key=operator.itemgetter(1), reverse=True), 0, 40)
# key_list2 = itertools.islice(sorted(dict_of_bigrams.items(), key=operator.itemgetter(1), reverse=True), 0, 40)
# key_list3 = itertools.islice(sorted(dict_of_bigrams.items(), key=operator.itemgetter(1), reverse=True), 0, 40)
# ch1_bigram_list = [dict_of_bigrams.get(x[0]) for x in key_list1]
#
# corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "cha2.txt")
# p = corpus.paras()
# read_paragraphs_and_split(p)
# ch2_bigram_list = [dict_of_bigrams.get(y[0]) for y in key_list2]
#
# corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "cha3.txt")
# p = corpus.paras()
# read_paragraphs_and_split(p)
# ch3_bigram_list = [dict_of_bigrams.get(z[0]) for z in key_list3]
#
# lists = list()
# lists.append(ch1_bigram_list)
# lists.append(ch2_bigram_list)
# lists.append(ch3_bigram_list)
#
# X = np.array(lists)
# pca = PCA(n_components=40)
# transformed_data = pca.fit(X)
# pca_score = pca.explained_variance_ratio_
# first_pc = pca.components_[0]
# second_pc = pca.components_[1]
#
# for i in transformed_data:
#     plt.scatter( first_pc[0] * i[0], first_pc[0] * i[0], color="r")
#     plt.scatter( second_pc[0] * i[0], second_pc[0] * i[0], color="c")
#
# plt.xlabel("First Principal Component")
# plt.ylabel("Second Principal Component")
# plt.show()
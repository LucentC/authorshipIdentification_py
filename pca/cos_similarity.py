import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from database import connect_to_database
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from scipy import spatial


def get_hausdorff_distance(lA, lB):
    min_distance = []
    for list_from_lA in lA:
        min_val = None
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            if min_val is None:
                min_val = dis
                break
            if dis < min_val:
                min_val = dis
        min_distance.append(min_val)
    return np.average(min_distance)


def get_features_from_database(SELECT_QUERY):
    # for x in novel:
    #     del x[-1]
    rows = [item['feature_value'] for item in connect_to_database.execute_select_query(SELECT_QUERY)]
    return [rows[x:x + 57] for x in xrange(0, len(rows), 57)]


def get_normalized_data(features):
    # mean = sum(x)/len(x)
    # std_dev = (1/len(x) * sum([ (x_i - mean)**2 for x_i in x]))**0.5
    # z_scores = [(x_i - mean)/std_dev for x_i in x]
    X = np.array(features)
    return preprocessing.scale(X)


def PCA_reduce_dimensionality(features):
    # only 2 components are retained
    # X_norm = preprocessing.StandardScaler().fit_transform(X)
    X = get_normalized_data(features)
    pca = PCA(n_components=3)
    return pca.fit_transform(X)

def LDA_reduce_dimenstionality(features):
    X = get_normalized_data(feature_list)
    lda = LDA(n_components=3)
    return lda.fit_transform(X)

author_list = []
feature_list = []

SQL_1 = "SELECT feature_value FROM fact WHERE doc_id = 1 ORDER BY para_id, feature_id;" #blue
t1 = get_features_from_database(SQL_1)
feature_list.extend(t1)
author_list.extend([0 for x in range(len(t1))])

SQL_2 = "SELECT feature_value FROM fact WHERE doc_id = 408 ORDER BY para_id, feature_id;" #green
t2 = get_features_from_database(SQL_2)
feature_list.extend(t2)
author_list.extend([1 for x in range(len(t2))])

SQL_3 = "SELECT feature_value FROM fact WHERE doc_id = 318 ORDER BY para_id, feature_id;" #red
t3 = get_features_from_database(SQL_3)
feature_list.extend(t3)
author_list.extend([2 for x in range(len(t3))])

fig = plt.figure(1, figsize=(4, 3))

X = PCA_reduce_dimensionality(feature_list)
y = np.choose(author_list, [0, 1, 2]).astype(np.float)

plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
plt.cla()
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y)
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_zlabel('PCA3')

# plt.scatter(X[:, 0], X[:, 1], c=y)
# plt.xlabel('PC1')
# plt.ylabel('PC2')
# plt.autoscale(enable=True, axis=u'both', tight=False)
plt.show()

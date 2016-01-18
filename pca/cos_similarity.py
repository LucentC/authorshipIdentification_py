import csv
import itertools
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
    return max(min_distance)


def get_features_from_database(doc_id):
    # for x in novel:
    #     del x[-1]
    SELECT_QUERY = "SELECT feature_value FROM fact WHERE doc_id = " + str(doc_id) + " ORDER BY para_id, feature_id;"
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


def draw_2D_graph(authors, features):
    fig = plt.figure(1, figsize=(4, 3))

    X = PCA_reduce_dimensionality(features)
    y = np.choose(authors, [0, 1, 2]).astype(np.float)

    plt.scatter(X[:, 0], X[:, 1], c=y)
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.autoscale(enable=True, axis=u'both', tight=False)
    plt.show()


def draw_3D_graph(authors, features):
    fig = plt.figure(1, figsize=(4, 3))

    X = PCA_reduce_dimensionality(features)
    y = np.choose(authors, [0, 1, 2]).astype(np.float)

    plt.clf()
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    plt.cla()
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y)
    ax.set_xlabel('PCA1')
    ax.set_ylabel('PCA2')
    ax.set_zlabel('PCA3')

    plt.show()


def output_csv_file(authors, features):
    X = PCA_reduce_dimensionality(features).tolist()
    print type(authors)
    if len(X) is not len(authors):
        raise Exception()
    #X = [list(item) for item in zip(X, authors)]
    X = map(lambda (a, b): a.insert(0, b), zip(X, authors))
    print X
    # with open('test.csv', 'wb') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(X)

author_list = []
feature_list = []

t1 = get_features_from_database(1)
feature_list.extend(t1)
author_list.extend([0 for x in range(len(t1))])

t2 = get_features_from_database(408)
feature_list.extend(t2)
author_list.extend([1 for x in range(len(t2))])

t3 = get_features_from_database(318)
feature_list.extend(t3)
author_list.extend([2 for x in range(len(t3))])

#draw_3D_graph(author_list, feature_list)
output_csv_file(author_list, feature_list)

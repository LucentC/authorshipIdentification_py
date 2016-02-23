import csv
import itertools
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from database import connect_to_database
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.neighbors import KNeighborsClassifier
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


def get_min_of_max_hausdorff_distance(lA, lB):
    max_distance = []
    for list_from_lA in lA:
        max_val = None
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            if max_val is None:
                max_val = dis
                break
            if dis > max_val:
                max_val = dis
        max_distance.append(max_val)
    return min(max_distance)


def get_avg_of_max_hausdorff_distance(lA, lB):
    max_distance = []
    for list_from_lA in lA:
        max_val = None
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            if max_val is None:
                max_val = dis
                break
            if dis > max_val:
                max_val = dis
        max_distance.append(max_val)
    return np.average(max_distance)


def get_max_of_max_hausdorff_distance(lA, lB):
    max_distance = []
    for list_from_lA in lA:
        max_val = None
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            if max_val is None:
                max_val = dis
                break
            if dis > max_val:
                max_val = dis
        max_distance.append(max_val)
    return max(max_distance)


def get_min_of_avg_hausdorff_distance(lA, lB):
    avg_distance = []
    for list_from_lA in lA:
        total_val = None
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            total_val += dis
        avg_distance.append(total_val / len(lB))
    return min(avg_distance)


def get_self_def_distance_v2(qp, lB):
    min_distance = []
    dis_list = []

    for list_from_lA in qp:
        min_val = None
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            dis_list.append(dis)
            if min_val is None:
                min_val = dis
                continue
            if dis < min_val:
                min_val = dis

        min_distance.append(min_val / float(np.std(dis_list)))
    return sum(min_distance) / len(lB)


def get_self_def_distance_v1(lA, lB):
    """
        This is a self defined distance function
        created by Raheem.
    """
    min_distance = []

    for list_from_lA in lA:
        min_val = None
        count = 0
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            count += dis
            if min_val is None:
                min_val = dis
                break
            if dis < min_val:
                min_val = dis

        if count == 0:
            continue
        min_distance.append(min_val / (count / len(lB)))
    return sum(min_distance) / len(lA)


def get_knn_classifier(X, y):
    #pca = PCA_reduce_dimensionality(X)
    #neigh = KNeighborsClassifier(algorithm='brute', n_neighbors=len(set(y)), metric='euclidean')
    neigh = KNeighborsClassifier(algorithm='ball_tree', n_neighbors=len(set(y)), metric='pyfunc', func=get_min_of_avg_hausdorff_distance)
    return neigh.fit(X, y)


def get_features_from_database_by_author_id(author_id):
    SELECT_QUERY = "SELECT feature_value FROM fact WHERE doc_id IN (SELECT doc_id FROM document WHERE author_id = {});"\
                    .format(author_id)
    rows = [item['feature_value'] for item in connect_to_database.execute_select_query(SELECT_QUERY)]
    return [rows[x:x + 57] for x in xrange(0, len(rows), 57)]


def get_features_from_database_by_doc_id(doc_id):
    # for x in novel:
    #     del x[-1]
    SELECT_QUERY = "SELECT feature_value FROM fact WHERE doc_id = " + str(doc_id) + " ORDER BY para_id, feature_id;"
    rows = [item['feature_value'] for item in connect_to_database.execute_select_query(SELECT_QUERY)]
    return [rows[x:x + 57] for x in xrange(0, len(rows), 57)]


def get_all_doc_id_in_paragraph():
    SELECT_QUERY = "SELECT DISTINCT doc_id FROM paragraph ORDER BY doc_id;"
    rows = connect_to_database.execute_select_query(SELECT_QUERY)
    return rows


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


def LDA_reduce_dimensionality(authors, features):
    X = get_normalized_data(features)
    # if len(X) is not len(authors):
    #     raise Exception()

    lda = LDA(n_components=2)
    return lda.fit(X, authors).transform(X)


def draw_2D_graph(authors, features):
    fig = plt.figure(1, figsize=(4, 3))

    #X = PCA_reduce_dimensionality(features)
    X = LDA_reduce_dimensionality(authors, features)
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


def output_csv_lists(authors, features):
    X = PCA_reduce_dimensionality(features).tolist()

    if len(X) is not len(authors):
        raise Exception()

    for i in range(len(X)):
        X[i].append(authors[i])

    return X


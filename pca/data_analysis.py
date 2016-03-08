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
    SELECT_QUERY = "SELECT feature_value FROM fact WHERE doc_id IN (SELECT doc_id FROM document WHERE author_id = {});" \
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

    # X = PCA_reduce_dimensionality(features)
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


def output_author_features_lists(doc_id):
    SQL_SELECT_QUERY = "SELECT d.author_id, {} as doc_id, ct.para_id, ct.f1, ct.f2, ct.f3, ct.f4, ct.f5, ct.f6, ct.f7" \
                       ", ct.f8, ct.f9, ct.f10, ct.f11, ct.f12, ct.f13, ct.f14, ct.f15, ct.f16, ct.f17, ct.f18, ct.f19" \
                       ", ct.f20, ct.f21, ct.f22, ct.f23, ct.f24, ct.f25, ct.f26, ct.f27, ct.f28, ct.f29, ct.f30," \
                       " ct.f31, ct.f32, ct.f33, ct.f34, ct.f35, ct.f36, ct.f37, ct.f38, ct.f39, ct.f40, ct.f41," \
                       " ct.f42, ct.f43, ct.f44, ct.f45, ct.f46, ct.f47, ct.f48, ct.f49, ct.f50, ct.f51, ct.f52," \
                       " ct.f53, ct.f54, ct.f55, ct.f56, ct.f57  FROM crosstab('SELECT para_id, " \
                       "feature_id ,feature_value FROM fact WHERE doc_id = {} ORDER BY para_id, feature_id', 'SELECT " \
                       "DISTINCT feature_id FROM fact WHERE doc_id = {} ORDER BY feature_id') as ct(para_id int, f1 " \
                       "real, f2 real, f3 real, f4 real, f5 real, f6 real, f7 real, f8 real, f9 real, f10 real, f11 " \
                       "real, f12 real, f13 real, f14 real, f15 real, f16 real, f17 real, f18 real, f19 real, f20 " \
                       "real, f21 real, f22 real, f23 real, f24 real, f25 real, f26 real, f27 real, f28 real, f29 " \
                       "real, f30 real, f31 real, f32 real, f33 real, f34 real, f35 real, f36 real, f37 real, f38 " \
                       "real, f39 real, f40 real, f41 real, f42 real, f43 real, f44 real, f45 real, f46 real, f47 " \
                       "real, f48 real, f49 real, f50 real, f51 real, f52 real, f53 real, f54 real, f55 real, f56 " \
                       "real, f57 real) INNER JOIN document d ON d.doc_id = {};".format(doc_id, doc_id, doc_id, doc_id)

    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)


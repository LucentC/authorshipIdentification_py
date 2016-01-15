import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from database import connect_to_database
from sklearn import preprocessing
from sklearn.decomposition import PCA
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


def get_normalized_data(SELECT_QUERY):
    rows = [item['feature_value'] for item in connect_to_database.execute_select_query(SELECT_QUERY)]
    novel = [rows[x:x + 57] for x in xrange(0, len(rows), 57)]

    mean = sum(x)/len(x)
    std_dev = (1/len(x) * sum([ (x_i - mean)**2 for x_i in x]))**0.5

    z_scores = [(x_i - mean)/std_dev for x_i in x]

    X = np.array(novel)
    # only 2 components are retained
    return preprocessing.normalize(X)



def reduce_dimensionality(SELECT_QUERY):
    rows = [item['feature_value'] for item in connect_to_database.execute_select_query(SELECT_QUERY)]
    novel = [rows[x:x + 57] for x in xrange(0, len(rows), 57)]
    for x in novel:
        del x[-1]

    X = np.array(novel)
    # only 2 components are retained
    X_norm = preprocessing.normalize(X)
    pca_1 = PCA(n_components=2)
    return pca_1.fit_transform(X_norm)

#     # #cur.execute("SELECT feature_value FROM fact WHERE doc_id = 9 AND para_id = 1617 AND (feature_id = 1 OR feature_id = 2 OR feature_id = 3 OR feature_id = 4 OR feature_id = 5 OR feature_id = 16 OR feature_id = 29 OR feature_id = 30);") #add ordered by feature_id
#     # cur.execute("SELECT feature_value FROM fact WHERE doc_id = 1 AND para_id = 10;") #add ordered by feature_id

#     # #cur.execute("SELECT feature_value FROM fact WHERE doc_id = 9 AND para_id = 1620 AND (feature_id = 1 OR feature_id = 2 OR feature_id = 3 OR feature_id = 4 OR feature_id = 5 OR feature_id = 16 OR feature_id = 29 OR feature_id = 30);")
#     # cur.execute("SELECT feature_value FROM fact WHERE doc_id = 2 AND para_id = 500;")

#     # cur.execute("SELECT feature_value FROM fact WHERE doc_id = 11 AND para_id = 1771 AND (feature_id = 1 OR feature_id = 2 OR feature_id = 3 OR feature_id = 4 OR feature_id = 5 OR feature_id = 16 OR feature_id = 29 OR feature_id = 30);")

#     # #cur.execute("SELECT feature_value FROM fact WHERE doc_id = 1 AND (feature_id = 1 OR feature_id = 2 OR feature_id = 3 OR feature_id = 4 OR feature_id = 5 OR feature_id = 16 OR feature_id = 29 OR feature_id = 30);")
#     # cur.execute("SELECT feature_value FROM fact WHERE doc_id = 1 ORDER BY para_id;")

#     #cur.execute("SELECT feature_value FROM fact WHERE doc_id = 2 AND (feature_id = 1 OR feature_id = 2 OR feature_id = 3 OR feature_id = 4 OR feature_id = 5 OR feature_id = 16 OR feature_id = 29 OR feature_id = 30);")
#     cur.execute("SELECT feature_value FROM fact WHERE doc_id = 1 ORDER BY para_id;")

#     # print get_hausdorff_distance(l4, l5)
#     # print spatial.distance.euclidean(l1, l2)
#     # print spatial.distance.cosine(l1, l2)

SQL_1 = "SELECT feature_value FROM fact WHERE doc_id in (SELECT doc_id FROM document WHERE author_id = 4) ORDER BY para_id, feature_id;"
t1 = np.array(reduce_dimensionality(SQL_1))

SQL_2 = "SELECT feature_value FROM fact WHERE doc_id in (SELECT doc_id FROM document WHERE author_id = 5) ORDER BY para_id, feature_id;"
t2 = np.array(reduce_dimensionality(SQL_2))

SQL_3 = "SELECT feature_value FROM fact WHERE doc_id in (SELECT doc_id FROM document WHERE author_id = 6) ORDER BY para_id, feature_id;"
t3 = np.array(reduce_dimensionality(SQL_3))

SQL_4 = "SELECT feature_value FROM fact WHERE doc_id = 636"
t4 = np.array(get_normalized_data(SQL_4))

SQL_5 = "SELECT feature_value FROM fact WHERE doc_id = 2288"
t5 = np.array(get_normalized_data(SQL_5))

SQL_6 = "SELECT feature_value FROM fact WHERE doc_id = 1581"
t6 = np.array(get_normalized_data(SQL_6))

SQL_7 = "SELECT feature_value FROM fact WHERE doc_id = 176"


# print get_hausdorff_distance(t4, t5)
# print get_hausdorff_distance(t4, t6)

fig = plt.figure()

plt.scatter(t4[:, 0], t4[:, 1],  marker='x', color='r')
plt.scatter(t5[:, 0], t5[:, 1],  marker='^', color='g')
plt.scatter(t6[:, 0], t6[:, 1],  marker='o', color='b')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.autoscale(enable=True, axis=u'both', tight=False)

# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(t4[:, 0], t4[:, 1], t4[:, 2], marker='^', color='r')
# ax.scatter(t5[:, 0], t5[:, 1], t5[:, 2], marker='o', color='g')
# ax.scatter(t6[:, 0], t6[:, 1], t6[:, 2], marker='x', color='b')
# ax.set_xlabel('PCA1')
# ax.set_ylabel('PCA2')
# ax.set_zlabel('PCA3')
plt.show()

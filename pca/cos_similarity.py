import math
import numpy as np
import matplotlib.pyplot as plt
from database import connect_to_database
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


def reduce_dimensionality(SELECT_QUERY):
    rows = [item['feature_value'] for item in connect_to_database.execute_select_query(SELECT_QUERY)]
    novel = [rows[x:x + 57] for x in xrange(0, len(rows), 57)]

    X = np.array(novel)
    # only 2 components are retained
    pca_1 = PCA(n_components=2)
    return pca_1.fit_transform(X)

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

SQL_1 = "SELECT feature_value FROM fact WHERE doc_id = 3 ORDER BY para_id, feature_id;"
t1 = np.array(reduce_dimensionality(SQL_1))

SQL_2 = "SELECT feature_value FROM fact WHERE doc_id = 6 ORDER BY para_id, feature_id;"
t2 = np.array(reduce_dimensionality(SQL_2))

plt.figure()
plt.scatter(t1[:, 0], t1[:, 1],  marker='x')
plt.scatter(t2[:, 0], t2[:, 1],  marker='.')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.autoscale(enable=True, axis=u'both', tight=False)
plt.xlim(-1000, 1000)
plt.ylim(-1000, 1000)
plt.show()

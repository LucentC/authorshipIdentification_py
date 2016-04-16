import time
import numpy as np
from data_analysis import data_warehouse
from data_analysis import calculate_K_nearest_neighbors_classifier as CKNN


start_time = time.time()

author_list = []
feature_list = []

d1 = data_warehouse.get_stylometric_features_by_doc_id(2013) # 1
feature_list.append(d1)
d2 = data_warehouse.get_stylometric_features_by_doc_id(408)
feature_list.append(d2)
d3 = data_warehouse.get_stylometric_features_by_doc_id(1400)
feature_list.append(d3)
author_list.extend([0 for x in range(3)])

d4 = data_warehouse.get_stylometric_features_by_doc_id(434)
feature_list.append(d4)
d5 = data_warehouse.get_stylometric_features_by_doc_id(622)
feature_list.append(d5)
d6 = data_warehouse.get_stylometric_features_by_doc_id(660)
feature_list.append(d6)
author_list.extend([1 for x in range(3)])

d7 = data_warehouse.get_stylometric_features_by_doc_id(191) # 3
feature_list.append(d7)
d8 = data_warehouse.get_stylometric_features_by_doc_id(459)
feature_list.append(d8)
d9 = data_warehouse.get_stylometric_features_by_doc_id(468)
feature_list.append(d9)
author_list.extend([2 for x in range(3)])

X = np.array(feature_list, dtype=float)
y = np.array(author_list)


print "Finished getting data from the database"
print CKNN.get_knn_classifier_cross_validation(X, y)

print "--- {} seconds ---".format(time.time() - start_time)

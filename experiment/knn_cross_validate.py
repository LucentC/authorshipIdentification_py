import time
import numpy as np
from data_analysis import data_warehouse
from data_analysis import calculate_K_nearest_neighbors_classifier as CKNN


start_time = time.time()

author_list = []
feature_list = []

t1 = data_warehouse.get_features_from_database_by_author_id(1) # 1
feature_list.extend(t1)
author_list.extend([0 for x in range(len(t1))])

t2 = data_warehouse.get_features_from_database_by_author_id(2) # 2
feature_list.extend(t2)
author_list.extend([1 for x in range(len(t2))])

t3 = data_warehouse.get_features_from_database_by_author_id(3) # 3
feature_list.extend(t3)
author_list.extend([2 for x in range(len(t3))])

X = np.array(feature_list)
y = np.array(author_list)

print "Finished getting data from the database"
print CKNN.get_knn_classifier_cross_validation(X, y)

print "--- %s seconds ---".format(time.time() - start_time)

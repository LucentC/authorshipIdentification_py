from data_analysis import data_warehouse
from data_analysis import calculate_K_nearest_neighbors_classifier as cknn
from data_analysis import calculate_nearest_neighbors_with_pruning as cnnp

author_list = []
feature_list = []

t1 = data_warehouse.get_stylometric_features_by_author_id(11) # 1
feature_list.extend(t1)
author_list.extend([1 for x in range(len(t1))])

t2 = data_warehouse.get_stylometric_features_by_author_id(12) # 2
feature_list.extend(t2)
author_list.extend([2 for x in range(len(t2))])

t3 = data_warehouse.get_stylometric_features_by_author_id(13) # 3
feature_list.extend(t3)
author_list.extend([3 for x in range(len(t3))])

qp = data_warehouse.get_stylometric_features_by_doc_id(663)

#print cknn.get_query_set_probabilistic(feature_list, author_list, qp)
for dist in cnnp.get_author_list_with_pruning_method(feature_list, author_list, qp, 1.0):
    print dist


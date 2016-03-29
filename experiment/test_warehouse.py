import time
from data_analysis import data_warehouse
from data_analysis import calculate_K_nearest_neighbors_classifier as cknn

feature_list = []
author_list = []

start_time = time.time()
feature_list, author_list = data_warehouse.get_all_features_from_database_fact()
qp = data_warehouse.get_features_from_database_by_doc_id(663)
result = cknn.get_query_set_probabilistic(feature_list, author_list, qp)
print result
print set(author_list)
print len(result)
print "--- {} seconds ---".format(time.time() - start_time)
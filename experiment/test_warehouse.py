import time
from data_analysis import data_warehouse
from data_analysis import calculate_K_nearest_neighbors_classifier as cknn

feature_list = []
author_list = []

start_time = time.time()
docs_in_fact = [dict(item) for item in data_warehouse.get_author_details_and_doc_list_in_fact()]
for item in docs_in_fact:
    print "Processing data"
    doc = data_warehouse.get_features_from_database_by_doc_id(item['doc_id'])
    feature_list.extend(doc)
    author_list.extend([item['author_id'] for x in range(len(doc))])

qp = data_warehouse.get_features_from_database_by_doc_id(663)
print "Finished getting data"
print cknn.get_query_set_probabilistic(feature_list, author_list, qp)
print "--- {} seconds ---".format(time.time() - start_time)
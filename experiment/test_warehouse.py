import time
from data_analysis import data_warehouse
from data_analysis import calculate_K_nearest_neighbors_classifier as cknn

feature_list = []
author_list = []

start_time = time.time()
# feature_list, author_list = data_warehouse.get_all_features_from_database_fact()
qp = data_warehouse.get_stylometric_features_by_doc_id(663)
# result = cknn.get_query_set_probabilistic(feature_list, author_list, qp)
# result = cknn.get_query_set_probabilistic(feature_list, author_list, qp)
author_hash = dict([(row['author_id'], row['author_name']) for row in data_warehouse.get_all_author_id_and_name()])
feature_list, author_list = data_warehouse.get_all_features_from_database_fact()

if len(feature_list) != len(author_list):
        print "Error"

results = []
knn_proba = cknn.get_query_set_probabilistic(feature_list, author_list, qp)

authors = list(set(author_list))

if len(knn_proba) != len(authors):
    print "Error"

for idx in range(len(set(authors))):
    results.append((author_hash.get(authors[idx]), knn_proba[idx]))

for item in results:
    print item

print "--- {} seconds ---".format(time.time() - start_time)
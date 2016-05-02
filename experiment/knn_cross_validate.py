import time
import numpy as np
from data_analysis import data_warehouse
from sklearn import cross_validation
from data_analysis import calculate_K_nearest_neighbors_classifier as CKNN
from data_analysis import calculate_K_nearest_neighbors_classifier_for_sets as KNN_for_set


start_time = time.time()

doc_ids_list = [2013, 408, 1400, 434, 622, 660, 191, 459, 468, 1]
author_list = [1, 1, 1, 11, 11, 11, 21, 21, 21, 1]
feature_list = []

for idx in doc_ids_list:
    data = data_warehouse.get_stylometric_features_by_doc_id(idx)
    print data
    feature_list.append(data)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(feature_list, author_list, test_size=0.1, random_state=1)

train = np.array(zip(X_train, y_train))
test = np.array(zip(X_test, y_test))

predictions = []


print "Finished getting data from the database"
#print CKNN.get_knn_classifier_cross_validation(X, y)
for idx in range(len(X_test)):
    print 'Classifying test instance number ', str(idx) + ':'
    neighbors = KNN_for_set.get_set_neighbor(training_set=train, test_instance=test[idx][0], k=5)
    majority_vote = KNN_for_set.select_neighbors_class(neighbors)
    print 'Predicted label = ', str(majority_vote), ' , Actual label = ', str(test[idx][1])

print "--- {} seconds ---".format(time.time() - start_time)

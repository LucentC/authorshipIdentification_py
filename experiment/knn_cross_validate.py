import time
import numpy as np
from data_analysis import data_warehouse
from sklearn import cross_validation
from sklearn.metrics import classification_report, accuracy_score
from data_analysis import calculate_K_nearest_neighbors_classifier_for_sets as KNN


start_time = time.time()

author_list = []
feature_list = []

for i in range(1, 20):
    temp_arr = data_warehouse.get_stylometric_features_by_author_id(i) # 3
    feature_list.extend(temp_arr)
    author_list.extend([i for x in range(len(temp_arr))])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(feature_list, author_list, test_size=0.1, random_state=1)

train = np.array(zip(X_train, y_train))
test = np.array(zip(X_test, y_test))

predictions = []


print 'Finished getting data from the database'
#print CKNN.get_knn_classifier_cross_validation(X, y)
for idx in range(len(X_test)):
    print 'Classifying test instance number ', str(idx) + ':'
    neighbors = KNN.get_set_neighbor(training_set=train, test_instance=test[idx][0], k=5)
    majority_vote = KNN.select_neighbors_class(neighbors)
    predictions.append(majority_vote)
    print 'Predicted label = ', str(majority_vote), ' , Actual label = ', str(test[idx][1])

print '\nThe overall accuracy of the model is: ', str(accuracy_score(y_test, predictions)), '\n'
print 'A detailed classification report: \n\n', classification_report(y_test, predictions)

print '--- {} seconds ---'.format(time.time() - start_time)

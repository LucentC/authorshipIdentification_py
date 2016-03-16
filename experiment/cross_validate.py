import numpy as np
from data_analysis import data_warehouse
from sklearn.cross_validation import KFold

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

kf = KFold(len(feature_list), n_folds=3)
print len(feature_list)
print len(author_list)
print len(kf)

for train_index, test_index in kf:
    print ("TRAIN: ", train_index, "TEST: ", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

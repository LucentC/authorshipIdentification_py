from pca import data_analysis

author_list = []
feature_list = []

t1 = data_analysis.get_features_from_database_by_author_id(11) # 1
feature_list.extend(t1)
author_list.extend([1 for x in range(len(t1))])

t2 = data_analysis.get_features_from_database_by_author_id(12) # 2
feature_list.extend(t2)
author_list.extend([2 for x in range(len(t2))])

t3 = data_analysis.get_features_from_database_by_author_id(13) # 3
feature_list.extend(t3)
author_list.extend([3 for x in range(len(t3))])

min_list = []
qp = data_analysis.get_features_from_database_by_doc_id(663)
#qp = data_analysis.PCA_reduce_dimensionality(data_temp)

neigh = data_analysis.get_knn_classifier(feature_list, author_list)
a = b = c = 0
for li in neigh.predict_proba(qp):
    a += li[0]
    b += li[1]
    c += li[2]
print "Writen by Mr. 4 ", (a / len(qp)) * 100, "%"
print "Writen by Mr. 5 ", (b / len(qp)) * 100, "%"
print "Writen by Mr. 6 ", (c / len(qp)) * 100, "%"

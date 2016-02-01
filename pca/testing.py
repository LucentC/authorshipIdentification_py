from pca import data_analysis

author_list = []
feature_list = []

t1 = data_analysis.get_features_from_database_by_author_id(1) # 1
feature_list.extend(t1)
author_list.extend([0 for x in range(len(t1))])

t2 = data_analysis.get_features_from_database_by_author_id(2) # 2
feature_list.extend(t2)
author_list.extend([1 for x in range(len(t2))])

t3 = data_analysis.get_features_from_database_by_author_id(3) # 3
feature_list.extend(t3)
author_list.extend([2 for x in range(len(t3))])

#data_analysis.draw_3D_graph(author_list, feature_list)
#print data_analysis.LDA_reduce_dimensionality(author_list, feature_list)
#print data_analysis.PCA_reduce_dimensionality(feature_list)
#data_analysis.draw_2D_graph(author_list, feature_list)

qp = data_analysis.get_features_from_database_by_doc_id(1031)

print t1
a = data_analysis.get_self_def_distance(t1, qp)
b = data_analysis.get_self_def_distance(t2, qp)
c = data_analysis.get_self_def_distance(t3, qp)
print (a / (a + b + c)) * 100, "%"
print (b / (a + b + c)) * 100, "%"
print (c / (a + b + c)) * 100, "%"

neigh = data_analysis.get_knn_classifier(feature_list, author_list)
print len(qp)
print neigh.predict(qp)
#print len(neigh.predict(qp))
print neigh.predict_proba(qp)
#print len(neigh.predict_proba(qp))

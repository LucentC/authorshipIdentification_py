from pca import data_analysis

author_list = []
feature_list = []

t1 = data_analysis.get_features_from_database_by_doc_id(233) # 1
feature_list.extend(t1)
author_list.extend([0 for x in range(len(t1))])

t2 = data_analysis.get_features_from_database_by_doc_id(377) # 2
feature_list.extend(t2)
author_list.extend([1 for x in range(len(t2))])

t3 = data_analysis.get_features_from_database_by_doc_id(862) # 3
feature_list.extend(t3)
author_list.extend([2 for x in range(len(t3))])

#print data_analysis.LDA_reduce_dimensionality(author_list, feature_list)
#print data_analysis.PCA_reduce_dimensionality(feature_list, 3)
#data_analysis.draw_2D_graph(author_list, feature_list)

li = data_analysis.PCA_reduce_dimensionality(feature_list, 2)
l1 = [list(li[i]) for i in author_list if i == 0]
l2 = [list(li[i]) for i in author_list if i == 1]
l3 = [list(li[i]) for i in author_list if i == 2]

print data_analysis.get_hausdorff_distance(l1, l2)
print data_analysis.get_hausdorff_distance(l1, l3)
print data_analysis.get_self_def_distance(l1, l2)
print data_analysis.get_self_def_distance(l1, l3)

data_analysis.draw_3D_graph(author_list, feature_list)
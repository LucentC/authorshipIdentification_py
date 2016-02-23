from pca import data_analysis

t1 = data_analysis.get_features_from_database_by_doc_id(1)     # Mr. 1
t2 = data_analysis.get_features_from_database_by_doc_id(408)    # Mr. 1
t3 = data_analysis.get_features_from_database_by_doc_id(3) # Mr. 3
t4 = data_analysis.get_features_from_database_by_doc_id(235) # Mr. 12
t5 = data_analysis.get_features_from_database_by_doc_id(357) # Mr. 12
t6 = data_analysis.get_features_from_database_by_doc_id(264)
t7 = data_analysis.get_features_from_database_by_doc_id(862)

print data_analysis.get_self_def_distance_v2(t1, t2)
print data_analysis.get_self_def_distance_v2(t1, t3)
print
print data_analysis.get_self_def_distance_v2(t4, t5)
print data_analysis.get_self_def_distance_v2(t4, t1)
print data_analysis.get_self_def_distance_v2(t4, t2)
print data_analysis.get_self_def_distance_v2(t4, t3)
print
print data_analysis.get_self_def_distance_v2(t6, t7)
print data_analysis.get_self_def_distance_v2(t6, t1)
print data_analysis.get_self_def_distance_v2(t6, t2)
print data_analysis.get_self_def_distance_v2(t6, t3)
print data_analysis.get_self_def_distance_v2(t6, t4)
print data_analysis.get_self_def_distance_v2(t6, t5)

from pca import data_analysis

t1 = data_analysis.get_features_from_database_by_doc_id(1)     # Mr. 1
t2 = data_analysis.get_features_from_database_by_doc_id(408)    # Mr. 1
t3 = data_analysis.get_features_from_database_by_doc_id(3) # Mr. 3
t4 = data_analysis.get_features_from_database_by_doc_id(235) # Mr. 12
t5 = data_analysis.get_features_from_database_by_doc_id(357) # Mr. 12

print data_analysis.get_m_hausdorff_distance(t1, t2)
print data_analysis.get_m_hausdorff_distance(t1, t3)

print data_analysis.get_m_hausdorff_distance(t4, t5)
print data_analysis.get_m_hausdorff_distance(t4, t2)

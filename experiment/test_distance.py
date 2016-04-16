import itertools
from data_analysis import data_warehouse
from data_analysis import modified_hausdorff_distance as MHD

#print MHD.get_min_of_avg_hausdorff_distance(data_warehouse.get_stylometric_features_by_doc_id(1129), data_warehouse.get_stylometric_features_by_doc_id(2254))
#print MHD.get_min_of_avg_hausdorff_distance(data_warehouse.get_stylometric_features_by_doc_id(1129), data_warehouse.get_stylometric_features_by_doc_id(51))

listA = [1, 2, 3]


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

for x, y in pairwise(listA + [listA[0]]):
    print x, y
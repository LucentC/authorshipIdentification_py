from operator import itemgetter
from collections import Counter
from data_analysis import modified_hausdorff_distance as MHD


def _get_set_tuple_distance(training_instance, test_instance):
    """
        Here, both training_instance and test_instance represents a document,
        which is a list of lists, where the inner lists refer to paragraphs
        of a document.
    """
    return (training_instance, MHD.get_standard_hausdorff_distance(training_instance[0], test_instance))


def get_set_neighbor(training_set, test_instance, k, radius):
    distance = [_get_set_tuple_distance(training_instance, test_instance) for training_instance in training_set]
    sorted_distance = sorted(distance, key=itemgetter(1))
    sorted_training_instances = [tup[0] for tup in sorted_distance if tup[0] >= radius]
    return sorted_training_instances[:k]


def select_neighbors_class(neighbors):
    classes = [neigh[1] for neigh in neighbors]
    return Counter(classes).most_common()[0][0]


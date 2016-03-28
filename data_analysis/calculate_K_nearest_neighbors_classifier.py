from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
import modified_hausdorff_distance as MHD


def get_knn_classifier_with_eucli(data, label):
    neigh = KNeighborsClassifier(algorithm='brute', n_neighbors=len(set(label)), metric='euclidean')
    return neigh.fit(data, label)


def get_knn_classifier_cross_validation(data, label):
    neigh = KNeighborsClassifier(algorithm='ball_tree', n_neighbors=len(set(label)), metric='pyfunc', func=MHD.get_min_of_max_hausdorff_distance)
    #neigh = KNeighborsClassifier(algorithm='auto', n_neighbors=len(set(label)), metric=MHD.get_standard_hausdorff_distance)
    return cross_val_score(neigh, data, label, cv=2, scoring='accuracy').mean()


def get_query_points_probabilistic(feature_list, author_list, qp):
    """
        feature_list - the feature list to indicate the stylometric features
        author_list - the author list to indicate a paragraph is written by whom
        qp - the query point, mostly represents a document

        This function will return a list that represents the probabilistic
        value of each query point. In our case, it refers to paragraphs.
        To be more accurate, it is a list to indicate which author writes
        'that' paragraph.
    """
    neigh = get_knn_classifier_with_eucli(feature_list, author_list)
    return neigh.predict_proba(qp)


def get_query_set_probabilistic(feature_list, author_list, qp):
    """
        feature_list - the feature list to indicate the stylometric features
        author_list - the author list to indicate a paragraph is written by whom
        qp - the query point, mostly represents a document

        This function will return a summarized list that represents
        probabilistic value of how likely/much an author contributes to
        a query set, which is, a document in our case.
    """
    set_proba = [0] * len(set(author_list))

    for point in get_query_points_probabilistic(feature_list, author_list, qp):
        for idx, val in enumerate(point):
            set_proba[idx] += val

    for idx in range(0, len(set_proba)):
        set_proba[idx] /= len(qp)

    return set_proba

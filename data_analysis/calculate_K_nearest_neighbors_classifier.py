from sklearn.neighbors import KNeighborsClassifier


def get_knn_classifier(X, y):
    #pca = PCA_reduce_dimensionality(X)
    neigh = KNeighborsClassifier(algorithm='brute', n_neighbors=len(set(y)), metric='euclidean')
    #neigh = KNeighborsClassifier(algorithm='ball_tree', n_neighbors=len(set(y)), metric='pyfunc', func=get_min_of_max_hausdorff_distance)
    return neigh.fit(X, y)


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
    neigh = get_knn_classifier(feature_list, author_list)
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

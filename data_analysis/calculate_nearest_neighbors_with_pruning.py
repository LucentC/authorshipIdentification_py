from sklearn.neighbors import RadiusNeighborsRegressor


def get_author_list_with_pruning_method(feature_list, author_list, qp, radius):
    """
        feature_list - the feature list to indicate the stylometric features
        author_list - the author list to indicate a paragraph is written by whom
        qp - the query point, mostly represents a document

        This function will return a shortened author list, which can greatly
        reduce the size of training set by removing those data points too far
        from the query point. Since it takes time to calculate the Hausdorff
        distance, reducing the size of testing set can speed up the process

        Please refer to the following link for more information
        http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.RadiusNeighborsRegressor.html#sklearn.neighbors.RadiusNeighborsRegressor
    """
    neigh = RadiusNeighborsRegressor(radius=radius, algorithm='brute', p=2)
    neigh.fit(feature_list, author_list)
    return neigh.radius_neighbors(qp, return_distance=True)

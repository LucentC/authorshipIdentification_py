import data_normalization
from sklearn.decomposition import PCA


def __PCA_reduce_dimensionality(features, components):
    # only 2 components are retained
    # X_norm = preprocessing.StandardScaler().fit_transform(X)
    X = data_normalization.get_normalized_data(features)
    pca = PCA(n_components=components)
    return pca.fit_transform(X)


def PCA_reduce_to_3_dimensionality(features):
    return __PCA_reduce_dimensionality(features, 3)


def PCA_reduce_to_2_dimensionality(features):
    return __PCA_reduce_dimensionality(features, 2)
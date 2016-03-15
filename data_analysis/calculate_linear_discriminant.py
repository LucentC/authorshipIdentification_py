from data_analysis import data_normalization
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA


def LDA_reduce_dimensionality(authors, features):
    X = data_normalization.get_normalized_data(features)
    lda = LDA(n_components=2)
    return lda.fit(X, authors).transform(X)

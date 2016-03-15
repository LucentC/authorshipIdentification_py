import csv
import itertools
import numpy as np
from database import connect_to_database


def output_csv_lists(authors, features):
    X = PCA_reduce_dimensionality(features).tolist()

    if len(X) is not len(authors):
        raise Exception()

    for i in range(len(X)):
        X[i].append(authors[i])

    return X


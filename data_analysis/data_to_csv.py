import csv
import calculate_principle_component
from itertools import groupby
from operator import itemgetter


def get_output_lists_for_csv_after_3d_pca(authors, features):
    X = calculate_principle_component.PCA_reduce_to_3_dimensionality(features).tolist()

    if len(X) != len(authors):
        raise Exception()

    for i in range(len(X)):
        X[i].append(authors[i])

    return X


def write_csvfile_output(filename, header_row, data_lists):

    pre_path = '/tmp/csv_files/'

    with open(filename, 'wb') as csvfile:
        csv_wr = csv.writer(csvfile)
        csv_wr.writerow(header_row)

        for row in data_lists:
            csv_wr.writerow(row)

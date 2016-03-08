import csv
from pca import data_analysis


with open('output.csv', 'wb') as csvfile:
    header_row = ['author id', 'document id', 'paragraph id'] + ['feature ' + str(i) for i in range(1, 57)]
    csv_wr = csv.writer(csvfile)
    csv_wr.writerow(header_row)

    # 2 refers to document ID, now this function only support getting data with doc_id
    # please change the doc_id in the following function
    for row in data_analysis.output_author_features_lists(2):
        csv_wr.writerow(row)

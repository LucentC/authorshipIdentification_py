from csv_exportation import data_to_csv
from data_analysis import data_warehouse

header_row = ['author id', 'document id', 'paragraph id'] + ['feature ' + str(i) for i in range(1, 57)]

documents = [item['doc_id'] for item in data_warehouse.get_doc_ids_from_database_fact()]
data_list = []

for doc_id in documents:
    data_list.extend(data_warehouse.get_cross_tab_features_from_database_by_doc_id(doc_id))

data_to_csv.write_csvfile_output('stylo_features.csv', header_row, data_list)

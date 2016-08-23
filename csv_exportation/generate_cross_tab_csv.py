from csv_exportation import data_to_csv
from data_analysis import data_warehouse

header_row = ['author id', 'document id', 'paragraph id'] + ['feature ' + str(i) for i in range(1, 57)]
data_list = data_warehouse.get_cross_tab_features_from_database_by_doc_id(2)
data_to_csv.write_csvfile_output('output.csv', header_row, data_list)

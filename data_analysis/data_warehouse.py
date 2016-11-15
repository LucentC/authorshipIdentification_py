from database import connect_to_database
from psycopg2.extensions import QuotedString


def get_stylometric_features_by_author_id(author_id):
    SELECT_QUERY = "SELECT feature_value FROM fact WHERE doc_id IN (SELECT doc_id FROM document WHERE author_id = {});" \
        .format(author_id)
    rows = [item['feature_value'] for item in connect_to_database.execute_select_query(SELECT_QUERY)]
    return [rows[x:x + 57] for x in xrange(0, len(rows), 57)]


def get_stylometric_features_by_doc_id(doc_id):
    SELECT_QUERY = "SELECT feature_value FROM fact WHERE doc_id = {} ORDER BY para_id, feature_id;".format(doc_id)
    rows = [item['feature_value'] for item in connect_to_database.execute_select_query(SELECT_QUERY)]
    return [rows[x:x + 57] for x in xrange(0, len(rows), 57)]


def __get_features_and_authors(SQL_SELECT_QUERY):
    previous_paraId = -1
    feature_list = []
    author_list = []
    temp = []

    for row in connect_to_database.execute_select_query(SQL_SELECT_QUERY):

        if previous_paraId != row['para_id']:

            # if it is not the first loop
            if previous_paraId != -1:
                feature_list.append(temp)
                author_list.append(row['author_id'])
                temp = []

            previous_paraId = row['para_id']

        temp.append(row['feature_value'])

    return feature_list, author_list


def get_all_features_from_database_fact():
    SQL_SELECT_QUERY = "SELECT d.author_id, f.doc_id, f.para_id, f.feature_value FROM fact f INNER JOIN document d ON " \
                       "f.doc_id = d.doc_id ORDER BY d.author_id, f.doc_id, f.para_id, f.feature_id;"
    return __get_features_and_authors(SQL_SELECT_QUERY)


def get_features_from_database_fact_by_list_of_author_id(authors):
    SQL_SELECT_QUERY = "SELECT d.author_id, f.doc_id, f.para_id, f.feature_value FROM fact f INNER JOIN document d ON " \
                       "f.doc_id = d.doc_id WHERE d.author_id IN ({}) ORDER BY d.author_id, f.doc_id, f.para_id, " \
                       "f.feature_id;".format(",".join(authors))
    return __get_features_and_authors(SQL_SELECT_QUERY)


def get_doc_ids_from_database_fact():
    SQL_SELECT_QUERY = "SELECT DISTINCT doc_id FROM fact ORDER BY doc_id;"
    rows = connect_to_database.execute_select_query(SQL_SELECT_QUERY)
    return rows


def get_docs_from_database_document_by_author_id(author_id):
    SQL_SELECT_QUERY = "SELECT doc_id, author_id, doc_title, doc_content FROM document " \
                       "WHERE author_id = {};".format(author_id)
    rows = connect_to_database.execute_select_query(SQL_SELECT_QUERY)
    return rows


def get_docs_from_database_document_by_doc_id(doc_id):
    SQL_SELECT_QUERY = "SELECT doc_id, author_id, doc_title, lang, doc_content FROM document " \
                       "WHERE doc_id = {}".format(doc_id)
    rows = connect_to_database.execute_select_query(SQL_SELECT_QUERY)
    return rows


def get_docs_name_by_doc_ids(doc_list):
    SQL_SELECT_QUERY = "SELECT doc_id, doc_title FROM document WHERE doc_id IN ({})".format(','.join(doc_list))
    rows = connect_to_database.execute_select_query(SQL_SELECT_QUERY)
    return rows

def get_all_doc_id_from_database_paragraph():
    SELECT_QUERY = "SELECT DISTINCT doc_id FROM paragraph ORDER BY doc_id;"
    rows = connect_to_database.execute_select_query(SELECT_QUERY)
    return rows


def get_cross_tab_features_from_database_by_doc_id(doc_id):
    SQL_SELECT_QUERY = "SELECT d.author_id, p.doc_id, ct.para_id, ct.f1, ct.f2, ct.f3, ct.f4, ct.f5, ct.f6, ct.f7, " \
                       "ct.f8, ct.f9, ct.f10, ct.f11, ct.f12, ct.f13, ct.f14, ct.f15, ct.f16, ct.f17, ct.f18, " \
                       "ct.f19, ct.f20, ct.f21, ct.f22, ct.f23, ct.f24, ct.f25, ct.f26, ct.f27, ct.f28, ct.f29, " \
                       "ct.f30, ct.f31, ct.f32, ct.f33, ct.f34, ct.f35, ct.f36, ct.f37, ct.f38, ct.f39, ct.f40, " \
                       "ct.f41, ct.f42, ct.f43, ct.f44, ct.f45, ct.f46, ct.f47, ct.f48, ct.f49, ct.f50, ct.f51, " \
                       "ct.f52, ct.f53, ct.f54, ct.f55, ct.f56, ct.f57  FROM crosstab('SELECT para_id, feature_id, " \
                       "feature_value FROM fact ORDER BY para_id, feature_id', 'SELECT DISTINCT feature_id FROM fact " \
                       "ORDER BY feature_id') as ct(para_id int, f1 real, f2 real, f3 real, f4 real, f5 real, f6 " \
                       "real, f7 real, f8 real, f9 real, f10 real, f11real, f12 real, f13 real, f14 real, f15 real, " \
                       "f16 real, f17 real, f18 real, f19 real, f20 real, f21 real, f22 real, f23 real, f24 real, " \
                       "f25 real, f26 real, f27 real, f28 real, f29 real, f30 real, f31 real, f32 real, f33 real, " \
                       "f34 real, f35 real, f36 real, f37 real, f38 real, f39 real, f40 real, f41 real, f42 real, " \
                       "f43 real, f44 real, f45 real, f46 real, f47 real, f48 real, f49 real, f50 real, f51 real, " \
                       "f52 real, f53 real, f54 real, f55 real, f56 real, f57 real) " \
                       "INNER JOIN paragraph p ON " \
                       "p.para_id = ct.para_id " \
                       "INNER JOIN document d ON " \
                       "p.doc_id = d.doc_id " \
                       "WHERE p.doc_id = {} ORDER BY d.author_id, p.doc_id, ct.para_id;".format(doc_id)

    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)


def get_total_num_of_authors():
    SQL_SELECT_QUERY = "SELECT COUNT(author_id) as number FROM author;"
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)[0]['number']


def get_total_num_of_docs():
    SQL_SELECT_QUERY = "SELECT COUNT(doc_id) as number FROM document;"
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)[0]['number']


def get_total_num_of_docs_with_stylo_values():
    SQL_SELECT_QUERY = "SELECT COUNT(DISTINCT doc_id) as number FROM fact;"
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)[0]['number']


def get_author_and_written_docs_count():
    SQL_SELECT_QUERY = "SELECT d.author_id as aid, a.author_name as aname, COUNT(d.doc_id) as doc_num FROM document " \
                       "d INNER JOIN author a ON d.author_id = a.author_id GROUP BY d.author_id, a.author_name " \
                       "ORDER BY d.author_id;"
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)


def get_author_name_by_id(author_id):
    if type(author_id) is not int:
        return -1
    SQL_SELECT_QUERY = "SELECT author_name FROM author WHERE author_id = {};".format(author_id)
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)[0]['author_name']


def get_all_author_id_and_name():
    SQL_SELECT_QUERY = "SELECT author_id, author_name FROM author;"
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)


def get_num_of_doc_written_by_an_author(author_id):
    if type(author_id) is not int:
        return -1
    SQL_SELECT_QUERY = "SELECT COUNT(doc_id) as num FROM document WHERE author_id = {};".format(author_id)
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)[0]['num']


def get_all_docs_by_author_id(author_id):
    if type(author_id) is not int:
        return -1
    SQL_SELECT_QUERY = "SELECT doc_id, doc_title, year_of_pub FROM document WHERE author_id = {} ORDER " \
                       "BY doc_id;".format(author_id)
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)


def get_doc_title_by_id(doc_id):
    SQL_SELECT_QUERY = "SELECT doc_title FROM document WHERE doc_id = {};".format(doc_id)
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)[0]['doc_title']


def get_doc_content_by_id(doc_id):
    if type(doc_id) is not int:
        return -1
    SQL_SELECT_QUERY = "SELECT doc_title, doc_content FROM document WHERE doc_id = {};".format(doc_id)
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)[0]


def get_author_details_and_doc_list_in_fact():
    SQL_SELECT_QUERY = "SELECT author_id, doc_id FROM document WHERE doc_id IN " \
                       "(SELECT DISTINCT(doc_id) FROM fact ORDER BY doc_id) ORDER BY author_id, doc_id;"
    return connect_to_database.execute_select_query(SQL_SELECT_QUERY)

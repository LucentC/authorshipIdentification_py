from database import connect_to_database_v2
from psycopg2.extensions import QuotedString


def get_author_name_by_id(author_id):
    if type(author_id) is not int:
        return -1

    SQL_SELECT_QUERY = "SELECT author_name FROM author WHERE author_id = {};".format(author_id)

    try:
        return connect_to_database_v2.execute_select_query(SQL_SELECT_QUERY)[0]['author_name']
    except IndexError:
        return -1


def get_author_name_by_doc_id(doc_id):
    SQL_SELECT_QUERY = "SELECT author_name FROM author a INNER JOIN document d ON a.author_id = d.author_id WHERE d.doc_id = {};".format(
        doc_id)
    return connect_to_database_v2.execute_select_query(SQL_SELECT_QUERY)[0]['author_name']


def get_doc_title_by_id(doc_id):
    SQL_SELECT_QUERY = "SELECT doc_title FROM document WHERE doc_id = {};".format(doc_id)
    return connect_to_database_v2.execute_select_query(SQL_SELECT_QUERY)[0]['doc_title']


def get_docs_name_by_doc_ids(doc_list):
    SQL_SELECT_QUERY = "SELECT doc_id, doc_title FROM document WHERE doc_id IN ({})".format(','.join(doc_list))
    rows = connect_to_database_v2.execute_select_query(SQL_SELECT_QUERY)
    return rows


def get_total_no_of_paragraphes_by_doc_id(doc_id):
    SQL_SELECT_QUERY = "SELECT COUNT(DISTINCT para_id) FROM paragraph WHERE doc_id = {};".format(int(doc_id))
    rows = connect_to_database_v2.execute_select_query(SQL_SELECT_QUERY)[0][0]
    return rows

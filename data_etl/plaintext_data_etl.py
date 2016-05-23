import sys
from database import connect_to_database
from database import feature_queries_preprocessing
from db_schema_classes.chapter import Chapter
from db_schema_classes.document import Document
from db_schema_classes.paragraph import Paragraph


def read_paragraphs_and_split(doc,sw_id):
    SQL_INSERT_QUERY = ''

    # Historical problem
    ch = Chapter(doc.get_doc_id(), -1)
    SQL_INSERT_QUERY += ch.get_chapter_insert_query()

    paragraphs = doc.get_doc_paragraphs(sw_id = sw_id)
    for para in paragraphs:
        p = Paragraph(doc.get_doc_id(),sw_id, para)
        SQL_INSERT_QUERY += feature_queries_preprocessing.get_fact_insert_query(doc.get_doc_id(), p)

    connect_to_database.execute_insert_query(SQL_INSERT_QUERY)

    # for para in paragraphs:
    #     for bigram in para.get_bigrams():
    #         print bigram.get_bigram_insert_query()
    #         connect_to_database.execute_insert_query(bigram.get_bigram_insert_query())


def read_file_and_get_doc_list(path):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    with open(path, 'r') as doc_file:
        content = doc_file.read()

    doc_list = []
    doc = Document(-1, -1, 'qp', 'qp', 'qp', content, 'qp')
    for para in doc.get_doc_paragraphs():
         doc_list.append(Paragraph(-1, para).get_stylo_list())

    return doc_list

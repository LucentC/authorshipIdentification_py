import time
from database import connect_to_database
from database import feature_queries_preprocessing
from db_schema_classes.chapter import Chapter
from db_schema_classes.document import Document
from db_schema_classes.paragraph import Paragraph


def read_paragraphs_and_split(doc):
    SQL_INSERT_QUERY = ''
    ch = Chapter(doc.get_doc_id(), -1)
    SQL_INSERT_QUERY += ch.get_chapter_insert_query()
    for para in doc.get_doc_paragraphs():
        p = Paragraph(doc.get_doc_id(), para)
        SQL_INSERT_QUERY += feature_queries_preprocessing.get_fact_insert_query(doc.get_doc_id(), p)
    connect_to_database.execute_insert_query(SQL_INSERT_QUERY)
    print 'finished dumping a novel'


"""
    A list of lists is returned and stored in the variable 'results'.
    Use the database column-name 'doc_content' to reference the content.

    Visit connect_to_database.py for more details.
"""
start_time = time.time()
SQL_INSERT_QUERY = "SELECT doc_id, author_id, doc_title, doc_content FROM document WHERE author_id BETWEEN 51 AND 60;"
results = connect_to_database.execute_select_query(SQL_INSERT_QUERY)
for result in results:
    read_paragraphs_and_split(Document(result['doc_id'], result['author_id'],
                                       result['doc_title'].decode('utf-8', 'ignore'),
                                       result['doc_content'].decode('utf-8', 'ignore')))
print "--- {} seconds ---".format(time.time() - start_time)

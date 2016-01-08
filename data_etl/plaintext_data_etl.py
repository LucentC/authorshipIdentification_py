import nltk
from database import connect_to_database
from database import feature_queries_preprocessing
from db_schema_classes.chapter import Chapter
from db_schema_classes.document import Document
from db_schema_classes.paragraph import Paragraph

SQL_INSERT_QUERY = ""


def process_book_item(document):
    global SQL_INSERT_QUERY
    tokens = nltk.word_tokenize(document.get_doc_content())
    paragraph_list = [tokens[x:x + 500] for x in xrange(0, len(tokens), 500)]
    read_paragraphs_and_split(document.get_doc_id(), paragraph_list)
    connect_to_database.execute_insert_query(SQL_INSERT_QUERY)


def read_paragraphs_and_split(doc_id, paragraphs):
    global SQL_INSERT_QUERY
    para_no = 0
    ch = Chapter(doc_id, -1)
    SQL_INSERT_QUERY += ch.get_chapter_insert_query()
    for para in paragraphs:
        para_no += 1
        p = Paragraph(doc_id, para_no, para)
        SQL_INSERT_QUERY += feature_queries_preprocessing.get_fact_insert_query(doc_id, p)
    print SQL_INSERT_QUERY


"""
    A list of lists is returned and stored in the variable 'results'.
    Use the database column-name 'doc_content' to reference the content.

    Visit connect_to_database.py for more details.
"""
SQL_INSERT_QUERY = "SELECT doc_id, author_id, doc_title, doc_content FROM document WHERE author_id = 43 AND doc_id = 939;"
results = connect_to_database.execute_select_query(SQL_INSERT_QUERY)
for result in results:
    process_book_item(Document(result['doc_id'], result['author_id'],
                               result['doc_title'].decode('utf-8', 'ignore'),
                               result['doc_content'].decode('utf-8', 'ignore')))

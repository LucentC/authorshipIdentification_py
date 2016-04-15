import time
from database import connect_to_database
from data_etl import plaintext_data_etl
from data_etl.db_schema_classes.document import Document


"""
    A list of lists is returned and stored in the variable 'results'.
    Use the database column-name 'doc_content' to reference the content.

    Visit connect_to_database.py for more details.
"""
start_time = time.time()
SQL_INSERT_QUERY = "SELECT doc_id, author_id, doc_title, doc_content FROM document WHERE author_id BETWEEN 63 AND 70;"
results = connect_to_database.execute_select_query(SQL_INSERT_QUERY)
for result in results:
    plaintext_data_etl.read_paragraphs_and_split(Document(result['doc_id'], result['author_id'],
                                                          result['doc_title'], "1882-02-25",
                                                          "loc", result['doc_content'],
                                                          "url"))
print "--- {} seconds ---".format(time.time() - start_time)

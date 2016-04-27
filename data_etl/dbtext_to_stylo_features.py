from data_analysis import data_warehouse
from data_etl import plaintext_data_etl
from data_etl.db_schema_classes.document import Document

"""
    A list of lists is returned and stored in the variable 'results'.
    Use the database column-name 'doc_content' to reference the content.

    Visit connect_to_database.py for more details.
"""
docs_in_fact = [row['doc_id'] for row in data_warehouse.get_doc_ids_from_database_fact()]
print docs_in_fact

for author_id in range(1, 1000):
    """
        Using this method is more memory-friendly as the documents is
        retrieved sequentially
    """
    docs = data_warehouse.get_docs_from_database_document_by_author_id(author_id)

    for doc in docs:
        if doc['doc_id'] in docs_in_fact:
            docs.remove(doc)
            continue

        plaintext_data_etl.read_paragraphs_and_split(Document(doc['doc_id'], doc['author_id'],
                                                              doc['doc_title'], 'lang', 'loc',
                                                              '1882-02-25', doc['doc_content'],
                                                              'url'))

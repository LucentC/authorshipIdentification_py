from data_analysis import data_warehouse
from data_etl import plaintext_data_etl
from data_etl.db_schema_classes.document import Document

"""
    A list of lists is returned and stored in the variable 'results'.
    Use the database column-name 'doc_content' to reference the content.

    Visit connect_to_database.py for more details.
"""
slide_window_id = 0
#docs_in_fact = [row['doc_id'] for row in data_warehouse.get_doc_ids_from_database_fact()]
docs_in_para =[row['doc_id'] for row in data_warehouse.get_doc_ids_with_sw_id_from_database_paragraph(sw_id=slide_window_id)]

for author_id in range(0, 10):
    """
        Using this method is more memory-friendly as the documents is
        retrieved sequentially
    """
    print "do author id", author_id
    docs = data_warehouse.get_docs_from_database_document_by_author_id(author_id)

    for doc in docs:
        if doc['doc_id'] in docs_in_para:
            docs.remove(doc)
            print doc['doc_id'],"with slide window id",slide_window_id, "has already been done"
            continue

        print "Dumping novel with doc_id ", str(doc['doc_id']),"slide window", slide_window_id
        plaintext_data_etl.read_paragraphs_and_split(Document(doc['doc_id'], doc['author_id'],
                                                              doc['doc_title'], 'lang', 'loc',
                                                              '1882-02-25', doc['doc_content'],
                                                              'url'),sw_id=slide_window_id)

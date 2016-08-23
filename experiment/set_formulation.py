from data_analysis import data_warehouse


def fomulate_set_paragraphes(author_id, set_size):
    document_list = data_warehouse.get_docs_from_database_document_by_author_id(author_id)
    paragraph_list = [data_warehouse.get_cross_tab_features_from_database_by_doc_id(idx) for idx in document_list]

    for idx in range(0, len(paragraph_list), set_size):
        yield paragraph_list[idx:idx + set_size]

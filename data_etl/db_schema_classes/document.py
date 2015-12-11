class Document:

    def __init__(self, doc_title):
        self.doc_title = doc_title
        #self.doc_year_of_pub = doc_year_of_pub

    def get_doc_title(self):
        return self.doc_title

    def get_doc_insert_query(self):
        return "INSERT INTO document(author_id, doc_title, year_of_pub) " \
               "VALUES (currval('author_author_id_seq'), '{}', '{}');\n"\
                .format(self.doc_title, "1886-02-25")

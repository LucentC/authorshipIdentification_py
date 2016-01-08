from psycopg2.extensions import QuotedString


class Document:

    def __init__(self, doc_title, year_of_pub, doc_content):
        self.doc_title = doc_title
        self.year_of_pub = year_of_pub
        self.doc_content = doc_content

    def get_doc_title(self):
        return self.doc_title

    def get_doc_insert_query(self):
        return "INSERT INTO document(author_id, doc_title, year_of_pub, doc_content) " \
               "VALUES (currval('author_author_id_seq'), '{}', '{}', {});\n"\
                .format(self.doc_title, "1886-02-25", QuotedString(self.doc_content).getquoted())

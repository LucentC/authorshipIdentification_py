from psycopg2.extensions import QuotedString


class Document:

    def __init__(self, author_id, book):
        self.author_id = author_id
        self.doc_title = book['title']
        self.doc_content = book['content']

    def get_doc_title(self):
        return self.doc_title

    def get_doc_insert_query(self):
        if self.author_id is -1:
            return "INSERT INTO document(author_id, doc_title, year_of_pub, doc_content) " \
                   "VALUES (currval('author_author_id_seq'), {}, '{}', {});\n"\
                    .format(QuotedString(self.doc_title).getquoted(), "1886-02-25",
                            QuotedString(self.doc_content).getquoted())
        else:
            return "INSERT INTO document(author_id, doc_title, year_of_pub, doc_content) " \
                   "VALUES ({}, {}, '{}', {});\n"\
                    .format(self.author_id, QuotedString(self.doc_title).getquoted(), "1886-02-25",
                            QuotedString(self.doc_content).getquoted())

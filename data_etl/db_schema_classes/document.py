import nltk
from psycopg2.extensions import QuotedString


class Document:

    def __init__(self, doc_id, author_id, doc_title, doc_content):
        self.doc_id = doc_id
        self.author_id = author_id
        self.doc_title = doc_title
        self.doc_content = doc_content

    def get_doc_id(self):
        return self.doc_id

    def get_author_id(self):
        return self.author_id

    def get_doc_title(self):
        return self.doc_title

    def get_doc_content(self):
        return self.doc_content

    def get_doc_paragraphs(self):
        """
            This function will return our self-defined paragraph, in the format of a list of lists.
            nltk is used here to tokenize the document's content.
            Thus, those tokens will be split and regrouped based on our definition.
            For example, we just defined 1500 tokens to be a paragraph.
        """
        tokens = nltk.word_tokenize(self.doc_content)
        paragraphs = [tokens[x:x + 1500] for x in xrange(0, len(tokens), 1500)]
        return paragraphs

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

from psycopg2.extensions import QuotedString

class Bigram:

    def __init__(self, bigrams=[]):
        self.bigram = "-".join(bigrams).lower()

    def get_bigram_insert_query(self):
        return "INSERT INTO bigram(feature_id, author_id ,doc_id, para_id, bigram) " \
               "VALUES ({}, currval('author_author_id_seq'), currval('document_doc_id_seq'), " \
               "currval('paragraph_para_id_seq'), {});\n".format(25, QuotedString(self.bigram).getquoted())

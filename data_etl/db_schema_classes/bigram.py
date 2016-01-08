from psycopg2.extensions import QuotedString


class Bigram:

    def __init__(self, doc_id, bigrams=[]):
        self.doc_id = doc_id
        self.bigram = "-".join(bigrams).lower().encode('utf-8')

    def get_bigram_insert_query(self):
        return "INSERT INTO bigram_feature(feature_id, doc_id, para_id, bigram) " \
               "VALUES ({}, {}, " \
               "currval('paragraph_para_id_seq'), {});\n".format(58, self.doc_id, QuotedString(self.bigram).getquoted())

class Bigram:

    def __init__(self, first_word, second_word):
        self.first_word = first_word
        self.second_word = second_word

    def get_bigram_insert_query(self):
        return "INSERT INTO bigram(author_id, doc_id, para_id, sen_id, bigram) " \
               "VALUES (currval('author_author_id_seq'), currval('document_doc_id_seq'), currval('paragraph_para_id_seq'), " \
               "currval('sentence_sen_id_seq'), '" + self.first_word + " " + self.second_word + "');";
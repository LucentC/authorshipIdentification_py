class Fact:

    def __init__(self, doc_id, para_id, para):
        self.doc_id = doc_id
        self.para_id = para_id
        self.paragraph = para

    def __format_insert_query(self, feature_id, feature_value):
        return "INSERT INTO fact(doc_id, para_id, feature_id, feature_value) " \
               "VALUES(currval('document_doc_id_seq'), currval('paragraph_para_id_seq')," \
               " {}, {});\n".format(feature_id, feature_value)

    def get_fact_insert_query(self):
        SQL_INSERT_QUERY = ""
        SQL_INSERT_QUERY += self.__format_insert_query(1, self.paragraph.get_total_no_of_words())
        SQL_INSERT_QUERY += self.__format_insert_query(2, self.paragraph.get_total_no_of_distinct_words())
        SQL_INSERT_QUERY += self.__format_insert_query(3, self.paragraph.get_average_word_length())
        SQL_INSERT_QUERY += self.__format_insert_query(4, self.paragraph.get_stddev_of_word_length())
        SQL_INSERT_QUERY += self.__format_insert_query(5, self.paragraph.get_vocabulary_richness())
        SQL_INSERT_QUERY += self.__format_insert_query(6, self.paragraph.get_total_no_of_character())
        SQL_INSERT_QUERY += self.__format_insert_query(12, self.paragraph.get_total_no_of_sentences())
        SQL_INSERT_QUERY += self.__format_insert_query(13, self.paragraph.get_average_no_of_words_per_sentence())
        return SQL_INSERT_QUERY

class Fact:

    def __init__(self, doc_id, para_id, para):
        self.doc_id = doc_id
        self.para_id = para_id
        self.paragraph = para

    @staticmethod
    def __format_insert_query(feature_id, feature_value):
        return "INSERT INTO fact(doc_id, para_id, feature_id, feature_value) " \
               "VALUES(currval('document_doc_id_seq'), currval('paragraph_para_id_seq')," \
               " {}, {});\n".format(feature_id, feature_value)

    def get_fact_insert_query(self):
        """
            The function will retrieve nearly all stylometric features' value
            from the paragraph supplied and transform it into SQL query with the aid
            of the above static function __format_insert_query.

            ----------------------- PLEASE NOTE -----------------------
            NOTE THAT the bigram insert query will be retrieved directly from the
            Bigram class.
        """
        SQL_INSERT_QUERY = ""
        SQL_INSERT_QUERY += self.__format_insert_query(1, self.paragraph.get_total_no_of_words())
        SQL_INSERT_QUERY += self.__format_insert_query(2, self.paragraph.get_total_no_of_distinct_words())
        SQL_INSERT_QUERY += self.__format_insert_query(3, self.paragraph.get_average_word_length())
        SQL_INSERT_QUERY += self.__format_insert_query(4, self.paragraph.get_stddev_of_word_length())
        SQL_INSERT_QUERY += self.__format_insert_query(5, self.paragraph.get_vocabulary_richness())
        SQL_INSERT_QUERY += self.__format_insert_query(6, self.paragraph.get_K_vocabulary_richness())
        SQL_INSERT_QUERY += self.__format_insert_query(7, self.paragraph.get_R_vocabulary_richness())
        SQL_INSERT_QUERY += self.__format_insert_query(8, self.paragraph.get_C_vocabulary_richness())
        SQL_INSERT_QUERY += self.__format_insert_query(9, self.paragraph.get_H_vocabulary_richness())
        SQL_INSERT_QUERY += self.__format_insert_query(10, self.paragraph.get_S_vocabulary_richness())
        SQL_INSERT_QUERY += self.__format_insert_query(11, self.paragraph.get_k_vocabulary_richness())
        SQL_INSERT_QUERY += self.__format_insert_query(12, self.paragraph.get_LN_vocabulary_richness())
        SQL_INSERT_QUERY += self.__format_insert_query(13, self.paragraph.get_entropy())
        SQL_INSERT_QUERY += self.__format_insert_query(14, self.paragraph.get_average_word_length())
        SQL_INSERT_QUERY += self.__format_insert_query(15, self.paragraph.get_stddev_of_word_length())
        SQL_INSERT_QUERY += self.__format_insert_query(16, self.paragraph.get_total_no_of_character())
        SQL_INSERT_QUERY += self.__format_insert_query(17, self.paragraph.get_total_no_of_alpha_character())
        SQL_INSERT_QUERY += self.__format_insert_query(18, self.paragraph.get_total_no_of_uppercase_character())
        SQL_INSERT_QUERY += self.__format_insert_query(19, self.paragraph.get_total_no_of_lowercase_character())
        SQL_INSERT_QUERY += self.__format_insert_query(20, self.paragraph.get_total_no_of_special_character())
        SQL_INSERT_QUERY += self.__format_insert_query(21, self.paragraph.get_total_no_of_digital_character())
        SQL_INSERT_QUERY += self.__format_insert_query(22, self.paragraph.get_total_no_of_whitespace_character())
        SQL_INSERT_QUERY += self.__format_insert_query(23, self.paragraph.get_alpha_chars_ratio())
        SQL_INSERT_QUERY += self.__format_insert_query(24, self.paragraph.get_uppercase_chars_ratio())
        SQL_INSERT_QUERY += self.__format_insert_query(25, self.paragraph.get_lowercase_chars_ratio())
        SQL_INSERT_QUERY += self.__format_insert_query(26, self.paragraph.get_special_chars_ratio())
        SQL_INSERT_QUERY += self.__format_insert_query(27, self.paragraph.get_digital_chars_ratio())
        SQL_INSERT_QUERY += self.__format_insert_query(28, self.paragraph.get_whitespace_chars_ratio())
        SQL_INSERT_QUERY += self.__format_insert_query(29, self.paragraph.get_total_no_of_sentences())
        SQL_INSERT_QUERY += self.__format_insert_query(30, self.paragraph.get_average_no_of_words_per_sentence())
        SQL_INSERT_QUERY += self.__format_insert_query(31, self.paragraph.get_freq_of_nouns())
        SQL_INSERT_QUERY += self.__format_insert_query(32, self.paragraph.get_freq_of_proper_nouns())
        SQL_INSERT_QUERY += self.__format_insert_query(33, self.paragraph.get_freq_of_pronoun())
        SQL_INSERT_QUERY += self.__format_insert_query(34, self.paragraph.get_freq_of_ordinal_adj())
        SQL_INSERT_QUERY += self.__format_insert_query(35, self.paragraph.get_freq_of_comparative_adj())
        SQL_INSERT_QUERY += self.__format_insert_query(36, self.paragraph.get_freq_of_superlative_adj())
        SQL_INSERT_QUERY += self.__format_insert_query(37, self.paragraph.get_freq_of_ordinal_adv())
        SQL_INSERT_QUERY += self.__format_insert_query(38, self.paragraph.get_freq_of_comparative_adv())
        SQL_INSERT_QUERY += self.__format_insert_query(39, self.paragraph.get_freq_of_superlative_adv())
        SQL_INSERT_QUERY += self.__format_insert_query(40, self.paragraph.get_freq_of_modal_auxiliary())
        SQL_INSERT_QUERY += self.__format_insert_query(41, self.paragraph.get_freq_of_base_form_verb())
        SQL_INSERT_QUERY += self.__format_insert_query(42, self.paragraph.get_freq_of_past_verb())
        SQL_INSERT_QUERY += self.__format_insert_query(43, self.paragraph.get_freq_of_presesnt_participle_verb())
        SQL_INSERT_QUERY += self.__format_insert_query(44, self.paragraph.get_freq_of_past_participle_verb())
        SQL_INSERT_QUERY += self.__format_insert_query(45, self.paragraph.get_freq_of_particle())
        SQL_INSERT_QUERY += self.__format_insert_query(46, self.paragraph.get_freq_of_wh_words())
        SQL_INSERT_QUERY += self.__format_insert_query(47, self.paragraph.get_freq_of_conjunction())
        SQL_INSERT_QUERY += self.__format_insert_query(48, self.paragraph.get_freq_of_numerical())
        SQL_INSERT_QUERY += self.__format_insert_query(49, self.paragraph.get_freq_of_determiner())
        SQL_INSERT_QUERY += self.__format_insert_query(50, self.paragraph.get_freq_of_existential_there())
        SQL_INSERT_QUERY += self.__format_insert_query(51, self.paragraph.get_freq_of_existential_to())
        SQL_INSERT_QUERY += self.__format_insert_query(52, self.paragraph.get_freq_of_preposition())
        SQL_INSERT_QUERY += self.__format_insert_query(53, self.paragraph.get_freq_of_genitive_marker())
        SQL_INSERT_QUERY += self.__format_insert_query(54, self.paragraph.get_freq_of_quotation())
        SQL_INSERT_QUERY += self.__format_insert_query(55, self.paragraph.get_freq_of_comma())
        SQL_INSERT_QUERY += self.__format_insert_query(56, self.paragraph.get_freq_of_sen_terminator())
        SQL_INSERT_QUERY += self.__format_insert_query(57, self.paragraph.get_freq_of_symbol())

        for bigram in self.paragraph.get_bigrams():
            SQL_INSERT_QUERY += bigram.get_bigram_insert_query()

        return SQL_INSERT_QUERY

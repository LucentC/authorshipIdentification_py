def __format_insert_query(feature_id, feature_value):
    return "INSERT INTO fact(doc_id, para_id, feature_id, feature_value) " \
            "VALUES(currval('document_doc_id_seq'), currval('paragraph_para_id_seq')," \
            " {}, {});\n".format(feature_id, feature_value)


def get_fact_insert_query(paragraph):
    """
        The function will retrieve all stylometric features' value
        from the paragraph supplied and transform it into SQL query with the aid
        of the above static function __format_insert_query.

        ----------------------- PLEASE NOTE -----------------------
        NOTE THAT the bigram insert query will be retrieved directly from the
        Bigram class.
    """
    SQL_INSERT_QUERY = ""
    SQL_INSERT_QUERY += paragraph.get_para_insert_query()
    SQL_INSERT_QUERY += __format_insert_query(1, paragraph.get_total_no_of_words())
    SQL_INSERT_QUERY += __format_insert_query(2, paragraph.get_total_no_of_distinct_words())
    SQL_INSERT_QUERY += __format_insert_query(3, paragraph.get_average_word_length())
    SQL_INSERT_QUERY += __format_insert_query(4, paragraph.get_stddev_of_word_length())
    SQL_INSERT_QUERY += __format_insert_query(5, paragraph.get_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(6, paragraph.get_K_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(7, paragraph.get_R_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(8, paragraph.get_C_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(9, paragraph.get_H_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(10, paragraph.get_S_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(11, paragraph.get_k_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(12, paragraph.get_LN_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(13, paragraph.get_entropy())
    SQL_INSERT_QUERY += __format_insert_query(14, paragraph.get_average_word_length())
    SQL_INSERT_QUERY += __format_insert_query(15, paragraph.get_stddev_of_word_length())
    SQL_INSERT_QUERY += __format_insert_query(16, paragraph.get_total_no_of_character())
    SQL_INSERT_QUERY += __format_insert_query(17, paragraph.get_total_no_of_alpha_character())
    SQL_INSERT_QUERY += __format_insert_query(18, paragraph.get_total_no_of_uppercase_character())
    SQL_INSERT_QUERY += __format_insert_query(19, paragraph.get_total_no_of_lowercase_character())
    SQL_INSERT_QUERY += __format_insert_query(20, paragraph.get_total_no_of_special_character())
    SQL_INSERT_QUERY += __format_insert_query(21, paragraph.get_total_no_of_digital_character())
    SQL_INSERT_QUERY += __format_insert_query(22, paragraph.get_total_no_of_whitespace_character())
    SQL_INSERT_QUERY += __format_insert_query(23, paragraph.get_alpha_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(24, paragraph.get_uppercase_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(25, paragraph.get_lowercase_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(26, paragraph.get_special_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(27, paragraph.get_digital_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(28, paragraph.get_whitespace_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(29, paragraph.get_total_no_of_sentences())
    SQL_INSERT_QUERY += __format_insert_query(30, paragraph.get_average_no_of_words_per_sentence())
    SQL_INSERT_QUERY += __format_insert_query(31, paragraph.get_freq_of_nouns())
    SQL_INSERT_QUERY += __format_insert_query(32, paragraph.get_freq_of_proper_nouns())
    SQL_INSERT_QUERY += __format_insert_query(33, paragraph.get_freq_of_pronoun())
    SQL_INSERT_QUERY += __format_insert_query(34, paragraph.get_freq_of_ordinal_adj())
    SQL_INSERT_QUERY += __format_insert_query(35, paragraph.get_freq_of_comparative_adj())
    SQL_INSERT_QUERY += __format_insert_query(36, paragraph.get_freq_of_superlative_adj())
    SQL_INSERT_QUERY += __format_insert_query(37, paragraph.get_freq_of_ordinal_adv())
    SQL_INSERT_QUERY += __format_insert_query(38, paragraph.get_freq_of_comparative_adv())
    SQL_INSERT_QUERY += __format_insert_query(39, paragraph.get_freq_of_superlative_adv())
    SQL_INSERT_QUERY += __format_insert_query(40, paragraph.get_freq_of_modal_auxiliary())
    SQL_INSERT_QUERY += __format_insert_query(41, paragraph.get_freq_of_base_form_verb())
    SQL_INSERT_QUERY += __format_insert_query(42, paragraph.get_freq_of_past_verb())
    SQL_INSERT_QUERY += __format_insert_query(43, paragraph.get_freq_of_presesnt_participle_verb())
    SQL_INSERT_QUERY += __format_insert_query(44, paragraph.get_freq_of_past_participle_verb())
    SQL_INSERT_QUERY += __format_insert_query(45, paragraph.get_freq_of_particle())
    SQL_INSERT_QUERY += __format_insert_query(46, paragraph.get_freq_of_wh_words())
    SQL_INSERT_QUERY += __format_insert_query(47, paragraph.get_freq_of_conjunction())
    SQL_INSERT_QUERY += __format_insert_query(48, paragraph.get_freq_of_numerical())
    SQL_INSERT_QUERY += __format_insert_query(49, paragraph.get_freq_of_determiner())
    SQL_INSERT_QUERY += __format_insert_query(50, paragraph.get_freq_of_existential_there())
    SQL_INSERT_QUERY += __format_insert_query(51, paragraph.get_freq_of_existential_to())
    SQL_INSERT_QUERY += __format_insert_query(52, paragraph.get_freq_of_preposition())
    SQL_INSERT_QUERY += __format_insert_query(53, paragraph.get_freq_of_genitive_marker())
    SQL_INSERT_QUERY += __format_insert_query(54, paragraph.get_freq_of_quotation())
    SQL_INSERT_QUERY += __format_insert_query(55, paragraph.get_freq_of_comma())
    SQL_INSERT_QUERY += __format_insert_query(56, paragraph.get_freq_of_sen_terminator())
    SQL_INSERT_QUERY += __format_insert_query(57, paragraph.get_freq_of_symbol())

    for bigram in paragraph.get_bigrams():
        SQL_INSERT_QUERY += bigram.get_bigram_insert_query()

    return SQL_INSERT_QUERY

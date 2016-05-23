def __format_insert_query(feature_id, doc_id, feature_value):
    return "INSERT INTO fact(doc_id, para_id, feature_id, feature_value) " \
            "VALUES({}, currval('paragraph_para_id_seq')," \
            " {}, {});\n".format(doc_id, feature_id, feature_value)


def get_fact_insert_query(doc_id, paragraph):
    """
        The function will retrieve all stylometric features' value
        from the doc_id, paragraph supplied and transform it into SQL query with the aid
        of the above static function __format_insert_query.

        ----------------------- PLEASE NOTE -----------------------
        NOTE THAT the bigram insert query will be retrieved directly from the
        Bigram class.
    """
    SQL_INSERT_QUERY = ""
    SQL_INSERT_QUERY += paragraph.get_para_insert_query()
    print "insert to db paragraph is ok"
    SQL_INSERT_QUERY += __format_insert_query(1, doc_id, paragraph.get_total_no_of_words())
    SQL_INSERT_QUERY += __format_insert_query(2, doc_id, paragraph.get_total_no_of_distinct_words())
    SQL_INSERT_QUERY += __format_insert_query(3, doc_id, paragraph.get_average_word_length())
    SQL_INSERT_QUERY += __format_insert_query(4, doc_id, paragraph.get_stddev_of_word_length())
    SQL_INSERT_QUERY += __format_insert_query(5, doc_id, paragraph.get_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(6, doc_id, paragraph.get_K_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(7, doc_id, paragraph.get_R_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(8, doc_id, paragraph.get_C_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(9, doc_id, paragraph.get_H_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(10, doc_id, paragraph.get_S_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(11, doc_id, paragraph.get_k_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(12, doc_id, paragraph.get_LN_vocabulary_richness())
    SQL_INSERT_QUERY += __format_insert_query(13, doc_id, paragraph.get_entropy())
    SQL_INSERT_QUERY += __format_insert_query(14, doc_id, paragraph.get_average_word_length())
    SQL_INSERT_QUERY += __format_insert_query(15, doc_id, paragraph.get_stddev_of_word_length())
    SQL_INSERT_QUERY += __format_insert_query(16, doc_id, paragraph.get_total_no_of_character())
    SQL_INSERT_QUERY += __format_insert_query(17, doc_id, paragraph.get_total_no_of_alpha_character())
    SQL_INSERT_QUERY += __format_insert_query(18, doc_id, paragraph.get_total_no_of_uppercase_character())
    SQL_INSERT_QUERY += __format_insert_query(19, doc_id, paragraph.get_total_no_of_lowercase_character())
    SQL_INSERT_QUERY += __format_insert_query(20, doc_id, paragraph.get_total_no_of_special_character())
    SQL_INSERT_QUERY += __format_insert_query(21, doc_id, paragraph.get_total_no_of_digital_character())
    SQL_INSERT_QUERY += __format_insert_query(22, doc_id, paragraph.get_total_no_of_whitespace_character())
    SQL_INSERT_QUERY += __format_insert_query(23, doc_id, paragraph.get_alpha_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(24, doc_id, paragraph.get_uppercase_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(25, doc_id, paragraph.get_lowercase_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(26, doc_id, paragraph.get_special_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(27, doc_id, paragraph.get_digital_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(28, doc_id, paragraph.get_whitespace_chars_ratio())
    SQL_INSERT_QUERY += __format_insert_query(29, doc_id, paragraph.get_total_no_of_sentences())
    SQL_INSERT_QUERY += __format_insert_query(30, doc_id, paragraph.get_average_no_of_words_per_sentence())
    SQL_INSERT_QUERY += __format_insert_query(31, doc_id, paragraph.get_freq_of_nouns())
    SQL_INSERT_QUERY += __format_insert_query(32, doc_id, paragraph.get_freq_of_proper_nouns())
    SQL_INSERT_QUERY += __format_insert_query(33, doc_id, paragraph.get_freq_of_pronoun())
    SQL_INSERT_QUERY += __format_insert_query(34, doc_id, paragraph.get_freq_of_ordinal_adj())
    SQL_INSERT_QUERY += __format_insert_query(35, doc_id, paragraph.get_freq_of_comparative_adj())
    SQL_INSERT_QUERY += __format_insert_query(36, doc_id, paragraph.get_freq_of_superlative_adj())
    SQL_INSERT_QUERY += __format_insert_query(37, doc_id, paragraph.get_freq_of_ordinal_adv())
    SQL_INSERT_QUERY += __format_insert_query(38, doc_id, paragraph.get_freq_of_comparative_adv())
    SQL_INSERT_QUERY += __format_insert_query(39, doc_id, paragraph.get_freq_of_superlative_adv())
    SQL_INSERT_QUERY += __format_insert_query(40, doc_id, paragraph.get_freq_of_modal_auxiliary())
    SQL_INSERT_QUERY += __format_insert_query(41, doc_id, paragraph.get_freq_of_base_form_verb())
    SQL_INSERT_QUERY += __format_insert_query(42, doc_id, paragraph.get_freq_of_past_verb())
    SQL_INSERT_QUERY += __format_insert_query(43, doc_id, paragraph.get_freq_of_presesnt_participle_verb())
    SQL_INSERT_QUERY += __format_insert_query(44, doc_id, paragraph.get_freq_of_past_participle_verb())
    SQL_INSERT_QUERY += __format_insert_query(45, doc_id, paragraph.get_freq_of_particle())
    SQL_INSERT_QUERY += __format_insert_query(46, doc_id, paragraph.get_freq_of_wh_words())
    SQL_INSERT_QUERY += __format_insert_query(47, doc_id, paragraph.get_freq_of_conjunction())
    SQL_INSERT_QUERY += __format_insert_query(48, doc_id, paragraph.get_freq_of_numerical())
    SQL_INSERT_QUERY += __format_insert_query(49, doc_id, paragraph.get_freq_of_determiner())
    SQL_INSERT_QUERY += __format_insert_query(50, doc_id, paragraph.get_freq_of_existential_there())
    SQL_INSERT_QUERY += __format_insert_query(51, doc_id, paragraph.get_freq_of_existential_to())
    SQL_INSERT_QUERY += __format_insert_query(52, doc_id, paragraph.get_freq_of_preposition())
    SQL_INSERT_QUERY += __format_insert_query(53, doc_id, paragraph.get_freq_of_genitive_marker())
    SQL_INSERT_QUERY += __format_insert_query(54, doc_id, paragraph.get_freq_of_quotation())
    SQL_INSERT_QUERY += __format_insert_query(55, doc_id, paragraph.get_freq_of_comma())
    SQL_INSERT_QUERY += __format_insert_query(56, doc_id, paragraph.get_freq_of_sen_terminator())
    SQL_INSERT_QUERY += __format_insert_query(57, doc_id, paragraph.get_freq_of_symbol())

    # for bigram in paragraph.get_bigrams():
    #     SQL_INSERT_QUERY += bigram.get_bigram_insert_query()

    return SQL_INSERT_QUERY

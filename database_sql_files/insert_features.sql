-- All of the below features are in a paragraph
-- Lexical Feature
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'total_number_of_words');
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'total_number_of_distinct_words');
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'average_word_length');
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'standard_deviation_of_word_length');
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'vocabulary_richness_measures');
-- vr = total_number_of_distinct_words / total_number_of_words
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'total_number_of_characters');
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'frequency_of_english_characters');
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'frequency_of_uppercase_characters');
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'frequency_of_lowercase_characters');
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'frequency_of_numerical_characters');
INSERT INTO feature(feature_type, feature_name) VALUES('lexical', 'frequency_of_special_characters');
-- Structural Feature
--INSERT INTO feature(feature_type, feature_name) VALUES('structural', 'total_number_of_lines');
--INSERT INTO feature(feature_type, feature_name) VALUES('structural', 'total_number_of_paragraphs');
INSERT INTO feature(feature_type, feature_name) VALUES('structural', 'total_number_of_sentences');
INSERT INTO feature(feature_type, feature_name) VALUES('structural', 'average_number_of_words_per_sentence');
INSERT INTO feature(feature_type, feature_name) VALUES('structural', 'average_number_of_words_per_paragraphs');
INSERT INTO feature(feature_type, feature_name) VALUES('structural', 'average_number_of_sentences_per_paragraphs');
-- Syntactic Feature
INSERT INTO feature(feature_type, feature_name) VALUES('syntactic', 'frequency_of_noun');
INSERT INTO feature(feature_type, feature_name) VALUES('syntactic', 'frequency_of_proper_noun');
INSERT INTO feature(feature_type, feature_name) VALUES('syntactic', 'frequency_of_verb');
INSERT INTO feature(feature_type, feature_name) VALUES('syntactic', 'frequency_of_adjectives');
INSERT INTO feature(feature_type, feature_name) VALUES('syntactic', 'frequency_of_adverbs');
INSERT INTO feature(feature_type, feature_name) VALUES('syntactic', 'frequency_of_comparatives');
INSERT INTO feature(feature_type, feature_name) VALUES('syntactic', 'frequency_of_superlatives');
INSERT INTO feature(feature_type, feature_name) VALUES('syntactic', 'frequency_of_wh_words');
INSERT INTO feature(feature_type, feature_name) VALUES('syntactic', 'frequency_of_function_words');
-- Bigram
INSERT INTO feature(feature_type, feature_name) VALUES('bigram', 'bigram');
import itertools
import nltk
import numpy
import re
import os
from collections import Counter
from bigram import Bigram


class Paragraph:

        def __init__(self, doc, para_no, para=[]):
            """
                Constructor of Paragraph class

            """
            """ The meta-data of the document """
            self.document = doc
            self.para_no = para_no
            self.file_path = ""

            """ Unhandled raw paragraph """
            self.paragraph = para

            """ Tagging the part of speech of each word in the paragraph and count the frequency """
            self.tagged_tokens = [] #nltk.pos_tag(self.paragraph)
            self.pos_counter = Counter(tag for word, tag in self.tagged_tokens)

            """ Extracting the word in paragraph and count the length """
            self.words_list = [word for word in self.paragraph if re.match(r'.*\w', word)]
            self.words_length = [len(word) for word in self.words_list]
            self.low_case_words_list = [word.lower() for word in self.words_list]
            self.char_list = list(itertools.chain(*self.words_list))

            self.write_paragraph_to_file()

        def write_paragraph_to_file(self):
            path = "/tmp/pladetect/{}/".format(self.document.get_doc_title())
            if not os.path.exists(path):
                os.makedirs(path)

            self.file_path = path + "paragraph_{}.txt".format(self.para_no)
            with open(self.file_path, 'w') as paragraph_file:
                paragraph_file.write(u' '.join(self.paragraph).encode('utf-8'))

        def get_para_insert_query(self):
            return "INSERT INTO paragraph(doc_id, chapter_id, path) " \
                   "VALUES (currval('document_doc_id_seq'), currval('chapter_chapter_id_seq'), '{}');\n"\
                    .format(self.file_path)

        def get_total_no_of_words(self):
            return len(self.paragraph)

        def get_total_no_of_distinct_words(self):
            return len(set(self.paragraph))

        def get_vocabulary_richness(self):
            return float(self.get_total_no_of_distinct_words()) / float(self.get_total_no_of_words())

        def get_average_word_length(self):
            return numpy.mean(self.words_length)

        def get_stddev_of_word_length(self):
            return numpy.std(self.words_length)

        def get_total_no_of_character(self):
            return sum(self.words_length)

        def get_total_no_of_english_character(self):
            eng_list = [char for char in self.char_list if re.match('[a-zA-Z]', char)]
            return len(eng_list)

        def get_total_no_of_special_character(self):
            special_list = [char for char in self.char_list if re.match('\W', char)]
            return len(special_list)

        def get_total_no_of_uppercase_character(self):
            uppercase_list = [char for char in self.char_list if char.isupper()]
            return len(uppercase_list)

        def get_total_no_of_lowercase_character(self):
            lowercase_list = [char for char in self.char_list if char.islower()]
            return len(lowercase_list)

        def get_total_no_of_digital_character(self):
            digit_list = [char for char in self.char_list if char.isdigit()]
            return len(digit_list)

        def get_total_no_of_sentences(self):
            """
                Still have some problems
            """
            return len(self.paragraph)

        def get_average_no_of_words_per_sentence(self):
            """
                Still have some problems
            """
            return numpy.mean([len(sen) for sen in self.paragraph])

        def get_freq_of_nouns(self):
            return self.pos_counter['NN']

        def get_freq_of_proper_nouns(self):
            return self.pos_counter['NP']

        def get_freq_of_adj(self):
            return self.pos_counter['JJ']

        def get_freq_of_adv(self):
            return self.pos_counter['RB']

        def get_freq_of_wh_words(self):
            return self.pos_counter['WH']

        def get_freq_of_verbs(self):
            return self.pos_counter['V'] + self.pos_counter['VD'] + self.pos_counter['VG'] + self.pos_counter['VN']

        def get_bigrams(self):
            bigram_list = []
            for bigram in nltk.bigrams(self.low_case_words_list):
                bigram_list.append(Bigram(bigram))
            return bigram_list

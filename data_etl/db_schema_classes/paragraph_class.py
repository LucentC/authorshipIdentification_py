import itertools
import nltk
import numpy
import re
import os
from bigram import Bigram


class Paragraph:

        def __init__(self, doc, para_no, para=[]):
            self.document = doc
            self.para_no = para_no
            self.file_path = ""
            self.paragraph = para
            self.flattened_paragraph = list(itertools.chain(*para))
            #self.words_length = [len(word) for word in self.flattened_paragraph]
            self.words_length = [len(word) for word in self.paragraph]
            self.write_paragraph_to_file()

        def write_paragraph_to_file(self):
            path = "/tmp/pladetect/{}/".format(self.document.get_doc_title())

            if not os.path.exists(path):
                os.makedirs(path)

            self.file_path = path + "paragraph_{}.txt".format(self.para_no)
            with open(self.file_path, 'w') as paragraph_file:
                paragraph_file.write(u' '.join(self.paragraph).encode('utf-8'))
                #paragraph_file.write(u' '.join(self.flattened_paragraph).encode('utf8'))

        def get_para_insert_query(self):
            return "INSERT INTO paragraph(doc_id, chapter_id, path) " \
                   "VALUES (currval('document_doc_id_seq'), currval('chapter_chapter_id_seq'), '{}');\n"\
                    .format(self.file_path)

        def get_total_no_of_words(self):
            return len(self.flattened_paragraph)

        def get_total_no_of_distinct_words(self):
            return len(set(self.flattened_paragraph))

        def get_vocabulary_richness(self):
            return float(self.get_total_no_of_distinct_words()) / float(self.get_total_no_of_words())

        def get_average_word_length(self):
            return numpy.mean(self.words_length)

        def get_stddev_of_word_length(self):
            return numpy.std(self.words_length)

        def get_total_no_of_character(self):
            return sum(self.words_length)

        def get_total_no_of_sentences(self):
            return len(self.paragraph)

        def get_average_no_of_words_per_sentence(self):
            return numpy.mean([len(sen) for sen in self.paragraph])

        def get_bigrams(self):
            bigram_list = []
            # for sentence in self.paragraph:
            #     sentence = [word for word in sentence if re.match(r'.*\w', word)]
            #     for bigram in nltk.bigrams(sentence):
            #         bigram_list.append(Bigram(bigram))
            para = [word for word in self.paragraph if re.match(r'.*\w', word)]
            for bigram in nltk.bigrams(para):
                bigram_list.append(Bigram(bigram))
            return bigram_list

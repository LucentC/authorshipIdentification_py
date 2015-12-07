import itertools
import nltk
import numpy
from bigram_class import Bigram


class Paragraph:

        def __init__(self, para_no, para=[]):
            self.para_no = para_no
            self.para_path = "test"
            self.paragraph = para
            self.flattened_paragraph = list(itertools.chain(*para))
            self.words_length = [len(word) for word in self.flattened_paragraph]

        def get_para_insert_query(self):
            return "INSERT INTO paragraph(doc_id, chapter_id, path) " \
                   "VALUES (currval('document_doc_id_seq'), currval('chapter_chapter_id_seq'), '" \
                   + self.para_path + "');"

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
            for sentence in self.paragraph:
                print sentence
                for bigram in nltk.bigrams(sentence):
                    print Bigram(bigram).get_bigram_insert_query()


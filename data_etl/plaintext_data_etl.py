import re
import nltk
from db_schema_classes.paragraph_class import Paragraph

dict_of_bigrams = dict()


def count_bigrams_in_para(bigram_key):
    """This is the description"""
    if bigram_key in dict_of_bigrams:
        dict_of_bigrams[bigram_key] += 1
    else:
        dict_of_bigrams[bigram_key] = 1


def match_tokens_to_bigrams(tokens):
    """This is the description"""
    previous = ""
    tokens = [token.lower() for token in tokens]
    tagged_token = nltk.pos_tag(tokens)

    for key, val in tagged_token:
        if re.match(r'.*\w', key):
            #print "Match word: ", key
            #print "Part-of-Speech: ", val
            if not previous:
                previous = key
                continue

            count_bigrams_in_para(previous + "-" + key)
            previous = key
        #else:
        # To be added to deal with punctuation


def read_paragraphs_and_split(paragraphs):
    for para in paragraphs:
        p = Paragraph(1, para)
        #print p.get_no_of_sentences()
        print p.get_average_no_of_words_per_sentence()
        # num_of_sen = 0
        # for sentence in para:
        #     num_of_sen += 1
        #     #match_tokens_to_bigrams(sentence)
        # print num_of_sen

#paragraphs = nltk.corpus.gutenberg.paras("shakespeare-caesar.txt")
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "cha1.txt")
p = corpus.paras()
read_paragraphs_and_split(p)
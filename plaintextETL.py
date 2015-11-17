import nltk
import re
import operator
import itertools

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
            print "Match word: ", key
            print "Part-of-Speech: ", val
            if not previous:
                previous = key
                continue

            count_bigrams_in_para(previous + "-" + key)
            previous = key
        #else:
        # To be added to deal with punctuation

#paragraphs = nltk.corpus.gutenberg.paras("shakespeare-caesar.txt")
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "test.txt")
paragraphs = corpus.paras()

for para in paragraphs:
    for sentence in para:
        match_tokens_to_bigrams(sentence)
        sorted_bigram_list = itertools.islice(sorted(dict_of_bigrams.items(), key=operator.itemgetter(1), reverse=True), 0, 20)
        #sorted_bigram_list = sorted(dict_of_bigrams.items(), key=operator.itemgetter(1), reverse=True)

for x in sorted_bigram_list:
    print x
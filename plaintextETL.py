import nltk
import re


def match_tokens_to_bigrams(tokens):
    """This is the description"""
    previous = ""
    tagged_token = nltk.pos_tag(tokens)

    for key, val in tagged_token:
        if re.match(r'.*\w', key):
            print "Match word: ", key
            print "Part-of-Speech: ", val
            if not previous:
                previous = key
                continue

            previous = key
        else:
            print "Match non-word: ", key
            print "Part-of-Speech: ", val

#paragraphs = nltk.corpus.gutenberg.paras("shakespeare-caesar.txt")
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "test.txt")
paragraphs = corpus.paras()

for para in paragraphs:
    print para, "\n\n"
    for sentence in para:
        match_tokens_to_bigrams(sentence)

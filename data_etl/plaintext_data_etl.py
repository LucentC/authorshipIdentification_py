import re
import nltk
from db_schema_classes.paragraph_class import Paragraph
from db_schema_classes.fact_class import Fact
from db_schema_classes.author_class import Author
from db_schema_classes.document_class import Document

dict_of_bigrams = dict()
SQL_INSERT_QUERY = ""

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
    global SQL_INSERT_QUERY
    for para in paragraphs:
        if para[0][0] == "Author" and para[0][1] == ":":
            SQL_INSERT_QUERY += Author(" ".join(para[0][2:])).get_author_insert_query()
            continue

        if para[0][0] == "Title" and para[0][1] == ":":
            SQL_INSERT_QUERY += Document(" ".join(para[0][2:])).get_doc_insert_query()
            continue

        p = Paragraph(1, para)
        p.get_bigrams()
        #fact = Fact(1, 1, Paragraph(1, para))
        #SQL_INSERT_QUERY += fact.get_fact_insert_query()
        # num_of_sen = 0
        # for sentence in para:
        #     num_of_sen += 1
        #     #match_tokens_to_bigrams(sentence)
        # print num_of_sen

#paragraphs = nltk.corpus.gutenberg.paras("shakespeare-caesar.txt")
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "pg46.txt")
p = corpus.paras()
read_paragraphs_and_split(p)
#print SQL_INSERT_QUERY

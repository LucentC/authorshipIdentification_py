import re
import nltk
from db_schema_classes.paragraph_class import Paragraph
from db_schema_classes.fact_class import Fact
from db_schema_classes.author_class import Author
from db_schema_classes.document_class import Document

SQL_INSERT_QUERY = ""


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

        fact = Fact(1, 1, p)
        SQL_INSERT_QUERY += fact.get_fact_insert_query()

        bigram_list = p.get_bigrams()

        for bigram in bigram_list:
            SQL_INSERT_QUERY += bigram.get_bigram_insert_query()

#paragraphs = nltk.corpus.gutenberg.paras("shakespeare-caesar.txt")
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "pg46.txt")
p = corpus.paras()
read_paragraphs_and_split(p)
print SQL_INSERT_QUERY

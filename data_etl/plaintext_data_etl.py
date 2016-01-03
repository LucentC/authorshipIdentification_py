import nltk
import codecs
import time
import connect_to_database
from db_schema_classes.paragraph import Paragraph
from db_schema_classes.fact import Fact
from db_schema_classes.author import Author
from db_schema_classes.document import Document
from db_schema_classes.chapter import Chapter
from gutenberg_crawler.BookItem import BookItem


SQL_INSERT_QUERY = ""


def process_book_item(book):
    global SQL_INSERT_QUERY
    SQL_INSERT_QUERY += Author(book['author_name']).get_author_insert_query()
    SQL_INSERT_QUERY += Document(book['title']).get_doc_insert_query()
    tokens = nltk.word_tokenize(book['content'])
    paragraph_list = [tokens[x:x + 500] for x in xrange(0, len(tokens), 500)]
    read_paragraphs_and_split(book['title'], paragraph_list)
    print SQL_INSERT_QUERY
    connect_to_database.execute_insert_query(SQL_INSERT_QUERY)


def read_paragraphs_and_split(doc_name, paragraphs):
    global SQL_INSERT_QUERY
    para_no = 0
    ch = Chapter(-1)
    SQL_INSERT_QUERY += ch.get_chapter_insert_query()
    for para in paragraphs:
        para_no += 1
        p = Paragraph(doc_name, para_no, para)
        SQL_INSERT_QUERY += p.get_para_insert_query()

        fact = Fact(1, 1, p)
        SQL_INSERT_QUERY += fact.get_fact_insert_query()

        #for bigram in p.get_bigrams():
        #    SQL_INSERT_QUERY += bigram.get_bigram_insert_query()

#paragraphs = nltk.corpus.gutenberg.paras("shakespeare-caesar.txt")
#corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "test.txt")
#corpus_paragraphs = corpus.paras()
# start_time = time.time()
# corpus = codecs.open("data/pg46.txt", "r", "utf-8").read()
#
#
# print SQL_INSERT_QUERY
# print "--- {} seconds ---".format(time.time() - start_time)
#connect_to_database.execute_insert_query(SQL_INSERT_QUERY)

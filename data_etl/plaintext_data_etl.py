import nltk
import codecs
import connect_to_database
from db_schema_classes.paragraph_class import Paragraph
from db_schema_classes.fact import Fact
from db_schema_classes.author import Author
from db_schema_classes.document import Document
from db_schema_classes.chapter import Chapter

SQL_INSERT_QUERY = ""


def read_paragraphs_and_split(paragraphs):
    global SQL_INSERT_QUERY
    chapter_count = 0
    para_count = 0
    doc = None
    ch = Chapter(-1)
    SQL_INSERT_QUERY += Author("Charles Dicken").get_author_insert_query()
    doc = Document("THE CHRISTMAS CAROL")
    SQL_INSERT_QUERY += doc.get_doc_insert_query()
    SQL_INSERT_QUERY += ch.get_chapter_insert_query()
    for para in paragraphs:
        if para[0][0] == "Author" and para[0][1] == ":":
            SQL_INSERT_QUERY += Author(" ".join(para[0][2:])).get_author_insert_query()
            continue

        if para[0][0] == "Title" and para[0][1] == ":":
            doc = Document(" ".join(para[0][2:]))
            SQL_INSERT_QUERY += doc.get_doc_insert_query()
            SQL_INSERT_QUERY += ch.get_chapter_insert_query()
            continue

        if para[0][0] == "STAVE":
            chapter_count += 1
            ch = Chapter(chapter_count)
            SQL_INSERT_QUERY += ch.get_chapter_insert_query()
            continue

        para_count += 1
        p = Paragraph(doc, para_count, para)
        SQL_INSERT_QUERY += p.get_para_insert_query()

        fact = Fact(1, 1, p)
        SQL_INSERT_QUERY += fact.get_fact_insert_query()

        for bigram in p.get_bigrams():
            SQL_INSERT_QUERY += bigram.get_bigram_insert_query()

#paragraphs = nltk.corpus.gutenberg.paras("shakespeare-caesar.txt")
#corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "test.txt")
#corpus_paragraphs = corpus.paras()
corpus = codecs.open("data/pg46.txt", "r", "utf-8").read()
tokens = nltk.word_tokenize(corpus)
paragraph_list = [tokens[x:x + 500] for x in xrange(0, len(tokens), 500)]
read_paragraphs_and_split(paragraph_list)

#print SQL_INSERT_QUERY
#connect_to_database.execute_insert_query(SQL_INSERT_QUERY)

import nltk
import connect_to_database
from db_schema_classes.paragraph import Paragraph
from db_schema_classes.fact import Fact
from db_schema_classes.author import Author
from db_schema_classes.document import Document
from db_schema_classes.chapter import Chapter


SQL_INSERT_QUERY = ""


def process_book_item(book):
    global SQL_INSERT_QUERY
    SQL_INSERT_QUERY += Author(book['author_name']).get_author_insert_query()
    SQL_INSERT_QUERY += Document(book['title']).get_doc_insert_query()
    tokens = nltk.word_tokenize(book['content'])
    paragraph_list = [tokens[x:x + 500] for x in xrange(0, len(tokens), 500)]
    read_paragraphs_and_split(book['title'], paragraph_list)
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

# corpus = codecs.open("/home/raheem/Downloads/Gutenberg/txt/Aldous Huxley___Mortal Coils.txt", "r", "utf-8").read()
# tokens = nltk.word_tokenize(corpus)
# SQL_INSERT_QUERY += Author("Charles Dicken").get_author_insert_query()
# SQL_INSERT_QUERY += Document("A Tale of Two Cities").get_doc_insert_query()
# paragraph_list = [tokens[x:x + 1500] for x in xrange(0, len(tokens), 1500)]
# read_paragraphs_and_split("A Tale of Two Cities", paragraph_list)
# connect_to_database.execute_insert_query(SQL_INSERT_QUERY)
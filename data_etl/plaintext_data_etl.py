import nltk
from db_schema_classes.paragraph_class import Paragraph
from db_schema_classes.fact_class import Fact
from db_schema_classes.author_class import Author
from db_schema_classes.document_class import Document
from db_schema_classes.chapter_class import Chapter

SQL_INSERT_QUERY = ""


def read_paragraphs_and_split(paragraphs):
    global SQL_INSERT_QUERY
    chapter_count = 0
    para_count = 0
    doc = None
    ch = Chapter(-1)
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
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "pg46.txt")
corpus_paragraphs = corpus.paras()
read_paragraphs_and_split(corpus_paragraphs)
print SQL_INSERT_QUERY

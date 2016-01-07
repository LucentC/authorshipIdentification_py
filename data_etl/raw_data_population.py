import os
import time
import codecs
import psycopg2
import connect_to_database
import plaintext_data_etl
from gutenberg_crawler.BookItem import BookItem
from db_schema_classes.author import Author
from db_schema_classes.document import Document

base_dir = '/home/dickson/Documents/programming/Gutenberg/txt/'
min_size = 100 * 1000 #100 Kb
books = []

start_time = time.time()

# for root, sub_dir, files in os.walk(base_dir):
#     for fi in files:
#         if os.path.getsize(root + fi) >= min_size:
#             book = BookItem()
#             book['author_name'] = fi.split('___')[0]
#             book['title'] = fi.split('___')[1][:-4]
#             with open(root + fi, 'r') as doc_file:
#                 book['content'] = doc_file.read()
#             books.append(book)
#
# for book in books:
#     SQL_INSERT_QUERY = ""
#     SQL_INSERT_QUERY += Author(book['author_name']).get_author_insert_query()
#     SQL_INSERT_QUERY += Document(book['title'], "123", book['content']).get_doc_insert_query()
#     connect_to_database.execute_insert_query(SQL_INSERT_QUERY)

GET_CONTENT = "select doc_content from document where doc_id = 1;"
try:
    conn = psycopg2.connect("dbname = 'stylometry_v2' user = 'dickson' host = 'localhost' password = 'dickson'")
    cur = conn.cursor()
    cur.execute(GET_CONTENT) #add ordered by feature_id

    rows = cur.fetchall()
    print rows[0][0]
    plaintext_data_etl.process_book_item(rows[0][0])
except psycopg2.DatabaseError, e:
    print 'Error %s' % e

print "--- {} seconds ---".format(time.time() - start_time)
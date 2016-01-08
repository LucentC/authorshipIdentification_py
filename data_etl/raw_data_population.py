import os
import sys

from database import connect_to_database
from db_schema_classes.author import Author
from db_schema_classes.document import Document
from gutenberg_crawler.BookItem import BookItem

base_dir = '/home/dickson/Documents/programming/Gutenberg/txt/'
min_size = 100 * 1000

"""
    To make python read all the files with
    utf-8 encoding by default
"""
reload(sys)
sys.setdefaultencoding('utf-8')

for root, sub_dir, files in os.walk(base_dir):

    for fi in files:

        if os.path.getsize(root + fi) >= min_size:

            book = BookItem()
            SQL_INSERT_QUERY = ""

            book['author_name'] = fi.split('___')[0]
            book['title'] = fi.split('___')[1][:-4]

            with open(root + fi, 'r') as doc_file:
                book['content'] = doc_file.read()

            author = Author(book['author_name'])
            author_queried_id = connect_to_database.test_if_author_exists(author)

            """
                The test_if_author_exists function returns -1
                if the name of the author is not found on the database.

                Visit connect_to_database.py for more details.
            """
            if author_queried_id is -1:
                SQL_INSERT_QUERY += author.get_author_insert_query()

            SQL_INSERT_QUERY += Document(-1, author_queried_id, book['title'], book['content']).get_doc_insert_query()
            print fi
            connect_to_database.execute_insert_query(SQL_INSERT_QUERY)

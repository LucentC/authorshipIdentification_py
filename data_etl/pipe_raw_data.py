import sys
import zipfile
from database import connect_to_database
from data_etl.db_schema_classes.author import Author
from data_etl.db_schema_classes.document import Document

dir_path = '/tmp/gutenberg/'
path_to_store_txt = '/tmp/gutenberg/txt/'


def process_book_item(book):
    """
        This function will catch the pipeline from Gutenberg
        crawler, precisely, the book item/object and continue
        to dump the data into the database.

        The following code will store the meta-data of the
        book item. After that, the zip file will be extracted
        by read_file_get_content function in order to get its
        content.
    """

    SQL_INSERT_QUERY = ''
    zip_path = dir_path + book['host_path'][0]

    author = Author(book['author'])
    author_queried_id = connect_to_database.test_if_author_exists(author)

    # Empty content variable for the storage of content
    content = ''

    """
        The test_if_author_exists function returns -1
        if the name of the author is not found on the database.

        Visit connect_to_database.py for more details.
    """
    if author_queried_id is -1:
        SQL_INSERT_QUERY += author.get_author_insert_query()

    """
        We do need to check the file type because somehow
        Gutenberg provides txt file
    """
    try:
        
        if zipfile.is_zipfile(zip_path):

                with zipfile.ZipFile(zip_path, 'r') as z:
                    z.extractall(path_to_store_txt)
                    """
                        There is a checking in the Document class to
                        see if author_queried_id is 0, which indicates
                        the author was not found in the database

                        In this case, the script will first insert the
                        info of that author into the database. Then,
                        the document will use that newly generated author_id
                        to do its job.

                        Otherwise, the script will just use the author_id
                        returned by the connect_to_database.test_if_author_exists(author)
                        function.
                    """
                    content = read_file_get_content(z.namelist()[0])

        else:
            content = read_file_get_content(zip_path)

    except NotImplementedError:
        print "Broken zip file"
        return False
    except IOError:
        print "File not found"
        return False

    SQL_INSERT_QUERY += Document(-1, author_queried_id, book['title'], book['rdate'],
                                 book['loc_class'], content, book['gutenberg_url']).get_doc_insert_query()

    connect_to_database.execute_insert_query(SQL_INSERT_QUERY)


def read_file_get_content(file_path):
    """
        This function will read the file stored on the computer
        and then return the contents in it.

        To begin with, the function will set the default encodeing
        to utf-8.
    """
    reload(sys)
    sys.setdefaultencoding('utf-8')

    try:
        with open(path_to_store_txt + file_path, 'r') as doc_file:

            contin = False
            content = ''

            for line in doc_file.readlines():
                if '*** START OF THE PROJECT GUTENBERG' in line:
                    contin = True
                    continue

                if '*** END OF THE PROJECT GUTENBERG' in line:
                    break

                if contin:
                    content += line

        return unicode(content, 'utf-8', errors='strict')

    except IOError:
        raise IOError

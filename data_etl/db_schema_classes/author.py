import chardet
from psycopg2.extensions import QuotedString


class Author:

    def __init__(self, author_name):
        self.author_name = unicode(author_name, 'utf-8', errors='ignore').encode('utf-8')

    def get_author_insert_query(self):
        return "INSERT INTO author(author_name) VALUES ({});\n".format(QuotedString(self.author_name).getquoted())

    def get_if_author_existing_query(self):
        if self.author_name == 'none':
            return -1

        return "SELECT author_id FROM author WHERE author_name LIKE {};"\
            .format(QuotedString('%' + self.author_name + '%'))

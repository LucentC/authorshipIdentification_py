from psycopg2.extensions import QuotedString


class Author:

    def __init__(self, author_name):
        self.author_name = author_name.replace(',', '')
        self.author_first_name = self.author_name.split(' ')[0]
        self.author_last_name = self.author_name.split(' ')[-1]

    def get_author_insert_query(self):
        return "INSERT INTO author(author_name) VALUES ('{}');\n".format(self.author_name.encode('utf-8'))

    def get_if_author_existing_query(self):
        return "SELECT author_id FROM author WHERE author_name LIKE {} OR author_name LIKE {};"\
            .format(QuotedString('%' + self.author_first_name + '%' + self.author_last_name + '%'),
                    QuotedString('%' + self.author_last_name + '%' + self.author_first_name + '%'))
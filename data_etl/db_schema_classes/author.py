class Author:

    def __init__(self, authorName):
        self.authorName = authorName

    def get_author_insert_query(self):
        return "INSERT INTO author(author_name) VALUES ('{}');\n".format(self.authorName)

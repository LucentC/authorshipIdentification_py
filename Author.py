class Author:

    def __init__(self, authorName, authorType):
        self.authorName = authorName
        self.authorType = authorType

    def getAuthorSQLString(self):
        return "INSERT INTO author(author_name, author_type) VALUES ('" + self.authorName + "', '" + self.authorType + "');"
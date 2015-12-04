class Chapter:

    def __init__(self, chap_no):
        self.chap_no = chap_no

    def get_chapter_insert_query(self):
        return "INSERT INTO chapter DEFAULT VALUE;"
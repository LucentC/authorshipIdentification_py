class Chapter:

    def __init__(self, doc_id, chap_no):
        self.doc_id = doc_id
        self.chap_no = chap_no

    def get_chapter_number(self):
        return self.chap_no

    def get_chapter_insert_query(self):
        return "INSERT INTO chapter(doc_id, chapter_no) " \
               "VALUES ({}, {});\n".format(self.doc_id, self.chap_no)

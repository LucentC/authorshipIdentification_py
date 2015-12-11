class Chapter:

    def __init__(self, chap_no):
        self.chap_no = chap_no

    def get_chapter_number(self):
        return self.chap_no

    def get_chapter_insert_query(self):
        return "INSERT INTO chapter(doc_id, chapter_no) " \
               "VALUES (currval('document_doc_id_seq'), {});\n".format(self.chap_no)

class Paragraph:

        def __init__(self, para_no):
            self.para_no = para_no

        def get_para_insert_query(self):
            return "INSERT INTO paragraph(doc_id, chapter_id) " \
                   "VALUES (currval('document_doc_id_seq'), currval('chapter_chapter_id_seq'));"
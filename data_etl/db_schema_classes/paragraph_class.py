class Paragraph:

        def get_para_insert_query(self):
            return "INSERT INTO paragraph(doc_id, chapter_id) " \
                   "VALUES (currval('document_doc_id_seq'), currval('chapter_chapter_id_seq'));"
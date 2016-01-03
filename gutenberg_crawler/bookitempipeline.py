import json
import data_etl.plaintext_data_etl


class BookItemPipeline(object):

    def process_item(self, item, spider):
        data_etl.plaintext_data_etl.process_book_item(item)

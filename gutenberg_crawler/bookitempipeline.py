from scrapy.exceptions import DropItem
from scrapy.http.request import Request
from scrapy.pipelines.files import FilesPipeline
from data_etl import pipe_raw_data


class BookItemPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield Request(file_url)

    def item_completed(self, results, item, info):
        file_path = [x['path'] for ok, x in results if ok]
        if not file_path:
            raise DropItem('Something went wrong')
        item['host_path'] = file_path
        pipe_raw_data.process_book_item(item)

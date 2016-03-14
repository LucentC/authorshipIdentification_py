import scrapy
from BookItem import BookItem
from scrapy.crawler import CrawlerProcess
from scrapy.http.request import Request


class GutenbergSpider(scrapy.Spider):
    name = "gutenberg"
    allowed_domains = ["prj61.cs.cityu.edu.hk"]
    start_urls = [
        "http://prj61.cs.cityu.edu.hk/"
    ]

    def parse(self, response):
        for latter_url in response.xpath('//ul[@class="browser alpha"]/li/a/@href').extract():
            if 'authors' in latter_url:
                full_url = response.urljoin(latter_url)
                yield Request(full_url, callback=self.extract_link_to_doc)

    def extract_link_to_doc(self, response):
        for latter_url in response.xpath('//li/a/@href').extract():
            if 'etext' in latter_url:
                full_url = response.urljoin(latter_url)
                yield Request(full_url, callback=self.extract_document)

    def extract_document(self, response):

        book = BookItem()
        book.setdefault('author', 'none')
        book.setdefault('title', 'none')
        book.setdefault('lang', 'none')
        book.setdefault('loc_class', 'none')
        book.setdefault('rdate', 'none')
        book.setdefault('rdate', 'none')

        for table_cell in response.xpath('//tr'):
            header = table_cell.xpath('th/text()').extract()

            if len(header) == 0:
                book['file_urls'] = [response.urljoin(table_cell.xpath('td[2]/a/@href').extract()[0])]
                continue

            if header[0] == 'Author':
                book['author'] = table_cell.xpath('td/text()').extract()[0].encode('utf-8')
            elif header[0] == 'Title':
                book['title'] = table_cell.xpath('td/text()').extract()[0].encode('utf-8')
            elif header[0] == 'Language':
                book['lang'] = table_cell.xpath('td/text()').extract()[0].encode('utf-8')
            elif header[0] == 'LoC Class':
                book['loc_class'] = table_cell.xpath('td/text()').extract()[0].encode('utf-8')
            elif header[0] == 'Release Date':
                book['rdate'] = table_cell.xpath('td/text()').extract()[0].encode('utf-8')
            else:
                continue

        book['gutenberg_url'] = response.url
        return book


process = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    #   Gutenberg blocks crawlers/spiders by default
    #   By setting the 'USER_AGENT' parameter to spoof the identity to 'googlebot'
    #   it is possible to crawl the website without any restrictions
    'USER_AGENT': 'googlebot',
    'DOWNLOADER_CLIENTCONTEXTFACTORY': 'contextfactory.MyClientContextFactory',
    'DOWNLOAD_HANDLERS': {
        's3': None,
    },
    'ITEM_PIPELINES': {
        'bookitempipeline.BookItemPipeline': 1,
    },
    'FILES_STORE': '/tmp/gutenberg',
})
process.crawl(GutenbergSpider)
process.start()

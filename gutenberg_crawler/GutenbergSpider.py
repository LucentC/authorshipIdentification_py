import scrapy
from BookItem import BookItem
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
import data_etl.plaintext_data_etl


class GutenbergSpider(scrapy.Spider):
    name = "gutenberg"
    allowed_domains = ["gutenberg.org"]
    start_urls = [
        # Books by Bronte, Charlotte
        #"https://www.gutenberg.org/ebooks/author/408",
        # Books by Bronte, Emily
        #"https://www.gutenberg.org/ebooks/author/405",
        # Books by Shakespeare, William
        #"https://www.gutenberg.org/ebooks/author/65"
        # Books by Mark Twain
        #"https://www.gutenberg.org/files/74/74-h/74-h.htm"
        "http://localhost/test/test.html"
    ]

    def __init__(self):
        self.book = BookItem()
        dispatcher.connect(self.spider_exit(), signals.spider_closed)

    def parse(self, response):
        content = []

        for h1 in response.xpath('//h1/text()').extract():
            self.book['title'] = h1.strip()

        for h2 in response.xpath('//h2/text()').extract():
            if h2.strip().startswith('BY'):
                self.book['author_name'] = u' '.join(h2.strip().split()[1:])

        for p in response.css('p *::text').extract():
            text = u' '.join(p.strip().replace('\n', ' ').split())
            if text:
                content.append(text)

        self.book['content'] = u' '.join(content)

    def spider_exit(self):
        data_etl.plaintext_data_etl.process_book_item(self.book)



process = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    #   Gutenberg blocks crawlers/spiders by default
    #   By setting the 'USER_AGENT' parameter to spoof the identity to 'googlebot'
    #   it is possible to crawl the website without any restrictions
    #'USER_AGENT': 'googlebot',
    #'DOWNLOADER_CLIENTCONTEXTFACTORY': 'contextfactory.MyClientContextFactory'
})

process.crawl(GutenbergSpider)
process.start()

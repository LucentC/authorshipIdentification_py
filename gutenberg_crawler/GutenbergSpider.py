import scrapy
import BookItem
from scrapy.crawler import CrawlerProcess


class GutenbergSpider(scrapy.Spider):
    name = "gutenberg"
    allowed_domains = ["gutenberg.org"]
    start_urls = [
        # Books by Bronte, Charlotte
        #"https://www.gutenberg.org/ebooks/author/408",
        # Books by Bronte, Emily
        #"https://www.gutenberg.org/ebooks/author/405",
        # Books by Shakespeare, William
        "https://www.gutenberg.org/ebooks/author/65"
    ]

    def parse(self, response):
        print response.body
        # for sel in response.xpath('//ul/li'):
        #     title = sel.xpath('a/text()').extract()
        #     link = sel.xpath('a/@href').extract()
        #     desc = sel.xpath('text()').extract()
        #     print title, link, desc


process = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    #   Gutenberg blocks crawlers/spiders by default
    #   By setting the 'USER_AGENT' parameter to spoof the identity to 'googlebot'
    #   it is possible to crawl the website without any restrictions
    'USER_AGENT': 'googlebot',
    'DOWNLOADER_CLIENTCONTEXTFACTORY': 'contextfactory.MyClientContextFactory'
})

process.crawl(GutenbergSpider)
process.start()

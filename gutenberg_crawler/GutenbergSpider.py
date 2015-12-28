import scrapy
import BookItem
import os
from scrapy.crawler import CrawlerProcess
from scrapy.selector import HtmlXPathSelector


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

    def parse(self, response):
        # for h1 in response.xpath('//h1/text()').extract():
        #     print h1.strip()

        # for h2 in response.xpath('//h2'):
        #     text = h2.xpath('./text()').extract()[0].strip()
        #     for p in h2.xpath('./p'):
        #         print p

        for p in response.css('p *::text').extract():
            content = u' '.join(p.strip().replace('\n', ' ').split())
            if content:
                print content



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

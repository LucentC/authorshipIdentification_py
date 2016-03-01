import scrapy
import time
from BookItem import BookItem
from scrapy.crawler import CrawlerProcess
from scrapy.http.request import Request
from scrapy.pipelines.files import FilesPipeline
from bs4 import BeautifulSoup
#import data_etl.plaintext_data_etl


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
                break

    def extract_link_to_doc(self, response):
        for latter_url in response.xpath('//li/a/@href').extract():
            if 'etext' in latter_url:
                full_url = response.urljoin(latter_url)
                yield Request(full_url, callback=self.extract_document)
                break

    def extract_document(self, response):

        book = BookItem()

        for table_cell in response.xpath('//tr'):
            header = table_cell.xpath('th/text()').extract()

            if len(header) == 0:
                book['zip_link'] = response.urljoin(table_cell.xpath('td[2]/a/@href').extract()[0])
                continue

            if header[0] == 'Author':
                book['author'] = table_cell.xpath('td/text()').extract()
            elif header[0] == 'Title':
                book['title'] = table_cell.xpath('td/text()').extract()
            elif header[0] == 'Language':
                book['lang'] = table_cell.xpath('td/text()').extract()
            elif header[0] == 'LoC Class':
                book['loc_class'] = table_cell.xpath('td/text()').extract()
            elif header[0] == 'Release Date':
                book['rdate'] = table_cell.xpath('td/text()').extract()
            else:
                continue

        return book


    # def extract_document(self, response):
    #     book = BookItem()
    #     content = []
    #
    #     soup = BeautifulSoup(response.body_as_unicode())
    #     for tag in soup.findAll('i'):
    #         tag.unwrap()
    #
    #     for tag in soup.findAll('big'):
    #         tag.unwrap()
    #
    #     for tag in soup.findAll('em'):
    #         tag.unwrap()
    #
    #     for tag in soup.findAll('ins'):
    #         tag.unwrap()
    #
    #     for tag in soup.findAll('pre'):
    #         tag.decompose()
    #
    #     for tag in soup.findAll('a'):
    #         tag.decompose()
    #
    #     for tag in soup.findAll('style'):
    #         tag.decompose()
    #
    #     for tag in soup.findAll('br'):
    #         tag.decompose()
    #
    #     for tag in soup.findAll('img'):
    #         tag.decompose()
    #
    #     for tag in soup.findAll('div'):
    #         tag.decompose()
    #
    #     for tag in soup.findAll('span'):
    #         tag.decompose()
    #
    #     for tag in soup.findAll('h1'):
    #         book['title'] = u' '.join(tag.contents).strip()
    #
    #     for tag in soup.findAll('h2'):
    #         text = tag.contents[0].strip()
    #         if text.startswith('By') or text.startswith('by'):
    #             book['author_name'] = u' '.join(text.split()[1:])
    #
    #     for tag in soup.findAll('p'):
    #         for p in tag.contents:
    #             text = u' '.join(p.strip().replace('\n', ' ').split())
    #             if text:
    #                 content.append(text)
    #                 print text
    #
    #     # for h1 in soup.xpath('//h1/text()').extract():
    #     #     book['title'] = h1.strip()
    #     #
    #     # for h2 in soup.xpath('//h2/text()').extract():
    #     #     if h2.strip().startswith('BY') or h2.strip().startswith('by'):
    #     #         book['author_name'] = u' '.join(h2.strip().split()[1:])
    #     #
    #     # for p in soup.select('p'):
    #     #     text = u' '.join(p.strip().replace('\n', ' ').split())
    #     #     if text:
    #     #         content.append(text)
    #     #         print text
    #
    #     book['content'] = u' '.join(content)
    #     #return book


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
    # 'ITEM_PIPELINES': {
    #     'bookitempipeline.BookItemPipeline': 10
    # }
})
process.crawl(GutenbergSpider)
process.start()

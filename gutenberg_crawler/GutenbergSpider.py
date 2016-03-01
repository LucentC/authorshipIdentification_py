import scrapy
import time
from BookItem import BookItem
from scrapy.crawler import CrawlerProcess
from scrapy.http.request import Request
from bs4 import BeautifulSoup
import data_etl.plaintext_data_etl


class GutenbergSpider(scrapy.Spider):
    name = "gutenberg"
    allowed_domains = ["gutenberg.org"]
    start_urls = [
        "http://prj61.cs.cityu.edu.hk/"
    ]

    def parse(self, response):
        for latter_url in response.xpath('//ul[@class="browser alpha"]/li/@href').extract():
            print latter_url
            if 'authors' in latter_url:
                full_url = response.urljoin(latter_url)
                time.sleep(10)
                yield Request(full_url, self.extract_index)

    # def extract_index(self, response):
    #     # authors = []
    #     # for author in response.xpath('//h2/a/text()').extract():
    #     #     if u'\xb6' not in author:
    #     #         print author
    #     for h2 in response.xpath('//h2/following-sibling::ul/li[@class="pgdbetext"]'):
    #         lang = h2.xpath('./text()').extract()
    #         if lang and 'English' in lang[0]:
    #             doc_name = h2.xpath('./a/text()').extract()
    #             doc_path = h2.xpath('./a/@href').extract()
    #             full_url = response.urljoin(doc_path[0])
    #             time.sleep(10)
    #             yield Request(full_url, self.test(response, doc_name))
    #
    # def test(self, response, name):
    #     print name
    #
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
    # 'ITEM_PIPELINES': {
    #     'bookitempipeline.BookItemPipeline': 10
    # }
})
process.crawl(GutenbergSpider)
process.start()

import scrapy
from BookItem import BookItem
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
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
        #"https://www.gutenberg.org/files/1028/1028-h/1028-h.htm"
        "http://localhost/test/test.html"
    ]

    def parse(self, response):
        book = BookItem()
        content = []

        soup = BeautifulSoup(response.body_as_unicode())
        for tag in soup.findAll('i'):
            tag.unwrap()

        for tag in soup.findAll('pre'):
            tag.decompose()

        for tag in soup.findAll('a'):
            tag.decompose()

        for tag in soup.findAll('style'):
            tag.decompose()

        for tag in soup.findAll('br'):
            tag.decompose()

        for tag in soup.findAll('img'):
            tag.decompose()

        for tag in soup.findAll('div'):
            tag.decompose()

        for tag in soup.findAll('span'):
            tag.decompose()

        for tag in soup.findAll('h1'):
            book['title'] = u' '.join(tag.contents).strip()

        for tag in soup.findAll('h2'):
            text = tag.contents[0].strip()
            if text.startswith('BY') or text.startswith('by'):
                book['author_name'] = u' '.join(text.split()[1:])

        for tag in soup.findAll('p'):
            for p in tag.contents:
                text = u' '.join(p.strip().replace('\n', ' ').split())
                if text:
                    content.append(text)

        # for h1 in soup.xpath('//h1/text()').extract():
        #     book['title'] = h1.strip()
        #
        # for h2 in soup.xpath('//h2/text()').extract():
        #     if h2.strip().startswith('BY') or h2.strip().startswith('by'):
        #         book['author_name'] = u' '.join(h2.strip().split()[1:])
        #
        # for p in soup.select('p'):
        #     text = u' '.join(p.strip().replace('\n', ' ').split())
        #     if text:
        #         content.append(text)
        #         print text

        book['content'] = u' '.join(content)
        return book


process = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    #   Gutenberg blocks crawlers/spiders by default
    #   By setting the 'USER_AGENT' parameter to spoof the identity to 'googlebot'
    #   it is possible to crawl the website without any restrictions
    'USER_AGENT': 'googlebot',
    'DOWNLOADER_CLIENTCONTEXTFACTORY': 'contextfactory.MyClientContextFactory',
    'ITEM_PIPELINES': {
        'bookitempipeline.BookItemPipeline': 10
    }
})
process.crawl(GutenbergSpider)
process.start()

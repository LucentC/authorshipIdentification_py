from scrapy.item import Item, Field


class BookItem(Item):
    title = Field()
    author = Field()
    lang = Field()
    loc_class = Field()
    rdate = Field()
    files = Field()
    file_urls = Field()

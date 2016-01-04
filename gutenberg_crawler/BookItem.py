from scrapy.item import Item, Field


class BookItem(Item):
    title = Field()
    author_name = Field()
    content = Field()
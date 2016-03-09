from scrapy.item import Item, Field


class BookItem(Item):
    """
        Meta-data of novel
        Besides gutenberg_url, all other fields are set to
        'none' by default
    """
    author = Field()
    title = Field()
    lang = Field()
    loc_class = Field()
    rdate = Field()
    gutenberg_url = Field()

    """
        The following fields are required for the download
    """
    files = Field()
    file_urls = Field()
    host_path = Field()

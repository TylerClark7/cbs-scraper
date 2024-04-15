import scrapy


class CbsItem(scrapy.Item):

    title = scrapy.Field()
    publish_date = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()


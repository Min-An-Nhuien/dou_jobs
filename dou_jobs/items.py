import scrapy


class DouJobsItem(scrapy.Item):
    title = scrapy.Field()
    city = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    company = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()


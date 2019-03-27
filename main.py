from scrapy.crawler import CrawlerProcess
from dou_jobs.spiders import doujobs
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl(doujobs.DouJobsSpider)
process.start()

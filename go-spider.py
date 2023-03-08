from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

#from mycrawler.spiders.pageavailability import PageavailabilitySpider
from defacementcrawler import DefacementCrawler

process = CrawlerProcess(get_project_settings())
process.crawl(DefacementCrawler)
process.start()

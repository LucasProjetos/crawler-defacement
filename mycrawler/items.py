# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MycrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    status = scrapy.Field()
    desturl = scrapy.Field()
    referer = scrapy.Field()
    title = scrapy.Field()
    follow = scrapy.Field()
    offsite = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()

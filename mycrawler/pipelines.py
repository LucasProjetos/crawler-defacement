# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter

class MycrawlerPipeline(object):

    item_seen = []

    def open_spider(self, spider):
        self.jsonlines_all = JsonLinesItemExporter(open("mycrawler-all.jsonl", "wb"))
        self.jsonlines_all.start_exporting()

    def close_spider(self, spider):
        self.jsonlines_all.finish_exporting()

    def process_item(self, item, spider):
        if item['desturl'] in self.item_seen:
            raise DropItem("Duplicated Item: %s" % item['desturl'])
        self.item_seen.append(item['desturl'])
        self.jsonlines_all.export_item(item)
        return item


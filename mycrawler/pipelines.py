# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import base64
import gzip
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter
from scrapy.pipelines.files import FilesPipeline
from mycrawler.settings import FILES_STORE
from typing import DefaultDict, Optional, Set, Union
from os import PathLike
from io import BytesIO
from scrapy.utils.misc import md5sum

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

class MyFilesPipeline(FilesPipeline):

#    def persist_file(self, path: Union[str, PathLike], buf, info, meta=None, headers=None):
#        absolute_path = self._get_filesystem_path(path)
#        self._mkdir(absolute_path.parent, info)
#        absolute_path.write_bytes(gzip.compress(buf.getvalue()))
    def file_downloaded(self, response, request, info, *, item=None):
        path = self.file_path(request, response=response, info=info, item=item)
        buf = BytesIO(gzip.compress(response.body))
        checksum = md5sum(buf)
        buf.seek(0)
        self.store.persist_file(path, buf, info)
        return checksum

    def file_path(self, request, response=None, info=None, *, item=None):
        filename = base64.urlsafe_b64encode(request.url.encode('utf-8')).decode('utf-8')
#        pathfile = FILES_STORE
#        absolutename = f'%s/%s.html' % (pathfile, filename)
        absolutename = f'%s.gz' % filename
        return absolutename

# -*- coding: utf-8 -*-
from scrapy.exporters import JsonLinesItemExporter

class DemoPipeline(object):
    def __init__(self):
        self.fp = open("data.json", "wb")
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp.close()
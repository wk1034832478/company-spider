# -*- coding: utf-8 -*-
import scrapy


class B2bSpider(scrapy.Spider):
    name = 'b2b'
    allowed_domains = ['http://b2b.huangye88.com/']
    start_urls = ['http://http://b2b.huangye88.com//']

    def parse(self, response):
        pass

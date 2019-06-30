# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import CompanySpiderItem
from bloom_filter import BloomFilter
class B2bSpider(scrapy.Spider):
    name = 'b2b'
    # allowed_domains = ['http://b2b.huangye88.com/']
    start_urls = ['http://b2b.huangye88.com/']
    # bloom_filter 对象，检查url是否已经被爬取过，如果被爬取过就过滤掉
    bloom = BloomFilter(max_elements=100000000, error_rate=0.1)

    def parse(self, response):
        
        # 抓取企业信息
        cname = response.css("h1.big") 
        if cname:
            csi = CompanySpiderItem()
            csi["name"] = cname.css("::text").extract_first().strip()
            # 企业描述
            csi["description"] = response.css(".related-box .txt::text").extract()
            yield csi
        lias = response.css(".box .mach_list2 dl h4 a") 
        for a in lias:
            url = a.css("::attr(href)").extract_first()
            if self.checkInBloom(url) == False:
                self.bloom.add(url)
                yield scrapy.Request(url, callback=self.parse)

        lias = response.css(".page_tag.Baidu_paging_indicator a") 
        for a in lias:
            url = a.css("::attr(href)").extract_first()
            if self.checkInBloom(url) == False:
                self.bloom.add(url)
                yield scrapy.Request(url, callback=self.parse)
            else:
                print("重复的url")
        # 抓取具体的城市名录入口
        lias = response.css(".ad_list a") #::attr(hregitf)
        for a in lias:
            # 需要进一步爬取的内容
            url = a.css("::attr(href)").extract_first()
            if self.checkInBloom(url) == False:
                self.bloom.add(url)
                yield scrapy.Request(url, callback=self.parse)
            else:
                print("重复的url")
        # 获取每一页的详情
        lias = response.css(".main .box .qiyecont li a::attr(href)")
        for a in lias:
            # 需要进一步爬取的内容
            url = a.extract()
            if self.checkInBloom(url) == False:
                self.bloom.add(url)
                yield scrapy.Request(url, callback=self.parse)
            else:
                print("重复的url")

    def checkInBloom(self, url):
        return url in self.bloom
        
       

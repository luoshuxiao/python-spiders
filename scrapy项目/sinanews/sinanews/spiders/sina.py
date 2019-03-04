# -*- coding: utf-8 -*-
import scrapy

from sinanews.items import SinanewsItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sports.sina.com.cn']
    start_urls = ['http://sports.sina.com.cn/']

    def parse(self, response):
        result_list = response.selector.css('.ty-card-type10-makeup a::text').extract()
        for title in result_list:
            item = SinanewsItem()
            item['title'] = title
            yield item
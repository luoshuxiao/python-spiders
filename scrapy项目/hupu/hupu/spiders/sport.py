# -*- coding: utf-8 -*-
import scrapy

from hupu.items import HupuItem


class SportSpider(scrapy.Spider):
    name = 'sport'
    allowed_domains = ['bbs.hupu.com']
    start_urls = ['http://bbs.hupu.com/gear']

    def start_requests(self):
        """构造请求"""
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        for page in range(100):
            yield scrapy.Request(
                url=f'http://bbs.hupu.com/gear-{page+1}',
                headers=headers,
                method='GET',
                callback=self.parse,)  # 调用对应的解析方法，可以自定义多个解析方法

    def parse(self, response):
        """解析响应"""
        li_list = response.selector.xpath('//ul[@class="for-list"]//li')
        for li in li_list:
            item = HupuItem()
            item['author'] = li.xpath('./div[2]/a[1]/text()').extract_first()
            item['subject'] = li.css('.titlelink.box a::text').extract()
            item['time'] = li.xpath('./div[2]/a[2]/text()').extract_first()
            yield item
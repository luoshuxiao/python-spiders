# -*- coding: utf-8 -*-
from urllib.parse import urlencode

import scrapy

from jingdong.items import JingdongItem


class GoodsSpider(scrapy.Spider):
    name = 'goods'
    allowed_domains = ['search.jd.com']
    start_urls = 'https://search.jd.com/Search?'

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            data = {
                'keyword': keyword,
                'enc': 'utf-8',
                'wq': keyword,
            }
            param_str = urlencode(data)
            url = self.start_urls + param_str
            for page in range(100):
                yield scrapy.Request(url=url, callback=self.parse, meta={'page': page+1}, dont_filter=True)

    def parse(self, response):
        li_list = response.selector.xpath('//div[@id="J_goodsList"]/ul//li')
        for l_list in li_list:
            goods = JingdongItem()
            img_src = ''.join(l_list.xpath('.//div[@class="p-img"]/a/img/@src').extract_first())
            price = ''.join(l_list.xpath('.//div[@class="p-price"]//i/text()').extract_first())
            goods['img_src'] = img_src
            goods['price'] = price
            yield goods
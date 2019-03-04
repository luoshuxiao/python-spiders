# -*- coding: utf-8 -*-
import json

import scrapy

from youyaoqi.items import YouyaoqiItem, YouyaoqiDetailItem


class ComicSpider(scrapy.Spider):
    name = 'comic'
    allowed_domains = ['www.u17.com']
    start_urls = ['http://www.u17.com/']

    def get_headers(self):
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Host': 'www.u17.com',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        return headers

    def start_requests(self):
        headers = self.get_headers()
        url = 'http://www.u17.com/comic/ajax.php?mod=comic_list&act=comic_list_new_fun&a=get_comic_list'
        postdata = {
            'data[group_id]': 'no',
            'data[theme_id]': 'no',
            'data[is_vip]': 'no',
            'data[accredit]': 'no',
            'data[color]': 'no',
            'data[comic_type]': 'no',
            'data[series_status]': 'no',
            'data[order]': '2',
            'data[page_num]': '1',
            'data[read_mode]': 'no'
        }
        for page in range(416):
            postdata["data[page_num]"] = str(page+1)
            yield scrapy.FormRequest(
                url=url,
                headers=headers,
                method='POST',
                formdata=postdata,
                callback=self.parse,)  # 调用对应的解析方法，可以自定义多个解析方法

    def parse(self, response):
        result = json.loads(response.text)
        result_list = result['comic_list']
        for i in result_list:
            item = YouyaoqiItem()
            item['comic_id'] = i['comic_id']
            item['name'] = i['name']
            item['cover'] = i['cover']
            item['line2'] = i['line2']
            # 返回数据流
            yield item
            detail_url = f'http://www.u17.com/comic/{item["comic_id"]}.html'
            # 返回请求
            yield scrapy.Request(url=detail_url, headers=self.get_headers(), method='GET', callback=self.detail_pare)

    def detail_pare(self, response):
        result_list = response.selector.css('#chapter').xpath('.//a')
        comic_id = response.url.split('/')[-1].split('.')[0]
        for a in result_list:
            detail_item = YouyaoqiDetailItem()
            detail_item['title'] = a.xpath('./@title').extract_first()
            detail_item['comic_id'] = comic_id
            detail_item['link'] = a.xpath('./@href').extract_first()
            yield detail_item


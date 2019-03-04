# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YouyaoqiItem(scrapy.Item):
    # define the fields for your item here like:
    collection_name = 'youyaoqi'
    comic_id = scrapy.Field()
    name = scrapy.Field()
    cover = scrapy.Field()
    line2 = scrapy.Field()


class YouyaoqiDetailItem(scrapy.Item):
    # define the fields for your item here like:
    collection_name = 'youyaoqi_detail'
    comic_id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()

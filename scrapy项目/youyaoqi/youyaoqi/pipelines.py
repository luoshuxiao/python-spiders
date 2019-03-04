# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymongo

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class YouyaoqiMysqlPipeline(object):
    """构造一个mysql管道类"""
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            username=crawler.settings.get('MYSQL_USERNAME'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self):
        self.db.close()

    def process_item(self, item, spider):
        if item.collection_name == 'youyaoqi':
            sql = 'insert into youyaoqi (comic_id, name, cover, line2) values (%s, %s, %s, %s)'
            self.cursor.execute(sql, (item['comic_id'], item['name'], item['cover'], item['line2']))
        else:
            sql = 'insert into youyaoqi_detail (comic_id, title, link) values (%s, %s, %s)'
            self.cursor.execute(sql, (item['comic_id'], item['title'], item['link']))
        self.db.commit()
        return item


class YouyaoqiMongoPipeline(object):
    """构造一个mongodb管道类"""
    def __init__(self, uri, database):
        self.uri = uri
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('MONGO_URI'),
            database=crawler.settings.get('MONGO_DB'),
            )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[self.database]

    def close_spider(self):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.collection_name].insert(dict(item))
        return item


class YouyaoqiImgPipeline(ImagesPipeline):
    """构造一个图片管道类"""
    def get_media_requests(self, item, info=None):
        """指明图片下载链接，包装成request对象"""
        if item.collection_name == 'youyaoqi':
            yield Request(item['cover'])
        else:
            pass

    def file_path(self, request, response=None, info=None):
        """生成下载下来的图片的文件名"""
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info=None):
        """判断图片是否下载成功，没有下载成功，抛出异常"""
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item
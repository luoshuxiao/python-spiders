from pymongo import MongoClient

client = MongoClient()
db = client.youyaoqi


def insert_info(item):
    db.manhua.insert(item)
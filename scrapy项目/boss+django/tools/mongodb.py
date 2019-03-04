from pymongo import MongoClient

client = MongoClient()
db = client.boss


def job_detail_insert_info(item, city):
    db[city].insert(item)

from django.shortcuts import render
from pymongo import MongoClient


def html(request):
    # 创建数据库对象
    client = MongoClient()
    # 指定某一个数据库
    db = client['youyaoqi']
    # 查询所有文档信息
    manhua_data = db.manhua.find()
    print(manhua_data)
    return render(request, 'html.html', {'data': manhua_data})
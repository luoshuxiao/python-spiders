
from django.shortcuts import render

from pymongo import MongoClient

from boss.settings import KEYWORDS
from tools.boss_job import change_name

obj_boss = MongoClient()
db = obj_boss['boss']


def index(request):
    if request.method == 'POST':
        name = request.POST.get('c_name')
        c_name = change_name(name)
        data = db[c_name].find()
        return render(request, 'index.html', {'keywords': KEYWORDS, 'city': name, 'data': data})
    data = db['chengdu'].find()
    return render(request, 'index.html', {'keywords': KEYWORDS, 'city': '成都', 'data': data})

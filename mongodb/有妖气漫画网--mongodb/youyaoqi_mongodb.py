import re

import requests
import json

from agent_helper import get_random_agent
from youyaoqi_mysql import *
from mongo_db import *

# db = get_connection()
# cursor = get_cursor(db)


def get_page(page):
    posturl = 'http://www.u17.com/comic/ajax.php?mod=comic_list&act=comic_list_new_fun&a=get_comic_list'
    session = requests.Session()
    postdata = {
        'data[group_id]': 'no',
        'data[theme_id]': 'no',
        'data[is_vip]': 'no',
        'data[accredit]': 'no',
        'data[color]': 'no',
        'data[comic_type]': 'no',
        'data[series_status]': 'no',
        'data[order]': 2,
        'data[page_num]': str(page),
        'data[read_mode]': 'no'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://www.u17.com',
        'Referer': 'http://www.u17.com/comic_list/th99_gr99_ca99_ss99_ob0_ac0_as0_wm0_co99_ct99_p1.html?order=2',
    }
    response = session.post(posturl, data=postdata, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_page(page):
    data = get_page(page)
    json_result = json.loads(data)
    print(json_result)
    for item in json_result['comic_list']:
        insert_info(item)


def main():
    for page in range(1, 10):
        parse_page(page)


# def save_picture():
#     """保存到本地"""
#     cursor.execute('use youyaoqi;')
#     selectsql = 'select cover from manhua;'
#     cursor.execute(selectsql.encode('utf-8'))
#     data = cursor.fetchall()  # 所有
#     print(data)
#     i = 0
#     for item in data:
#         print(item)
#         response = requests.get(item[0])
#         path = item[0].split('/')[5]
#         with open('./imgs/' + path, 'wb') as f:
#             f.write(response.content)
#             print(i)
#             i += 1
#     db.close()


if __name__ == '__main__':
    # save_picture()
    main()
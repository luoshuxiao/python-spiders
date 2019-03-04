import requests
import json

from agent_helper import get_random_agent
from qichamao_mysql import *

db = get_connection()
cursor = get_cursor(db)


def get_page(page):
    posturl = 'https://www.qichamao.com/cert-wall'
    session = requests.Session()
    postdata = {'page': str(page), 'pagesize': '9'}
    headers = {
        'Referer': 'https://www.qichamao.com/cert-wall/',
        'User-Agent': get_random_agent(),
        'Host': 'www.qichamao.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
    }
    response = session.post(posturl, data=postdata, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_page(page):
    data = get_page(page)
    json_result = json.loads(data)
    for item in json_result['dataList']:
        # company_name = item['CompanyName']
        # c_name = item['c_name']
        # c_phone = item['c_phone']
        # c_email = item['c_email']
        insert_data_mogujie(db, cursor, item)


def main():
    for page in range(2, 20):
        parse_page(page)
        print(page)


if __name__ == '__main__':
    main()
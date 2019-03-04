import json
import time

import requests

from lxml import etree
from tools.mongodb import *

from boss.settings import KEYWORDS

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.zhipin.com',
    'Referer': 'https://www.zhipin.com/job_detail/?query=python&scity=101270100&industry=&position=',
}


def change_name(name):
    if name == '北京':
        return 'beijing'
    if name == '上海':
        return 'shanghai'
    if name == '广州':
        return 'guangzhou'
    if name == '深圳':
        return 'shenzheng'
    if name == '杭州':
        return 'hangzhou'
    if name == '天津':
        return 'tianjin'
    if name == '西安':
        return 'xian'
    if name == '苏州':
        return 'suzhou'
    if name == '武汉':
        return 'wuhan'
    if name == '厦门':
        return 'xiamen'
    if name == '长沙':
        return 'changsha'
    if name == '成都':
        return 'chengdu'
    if name == '郑州':
        return 'zhengzhou'
    if name == '重庆':
        return 'chongqing'


def get_city_dict():
    city = {}
    url = 'https://www.zhipin.com/job_detail/?query=python&scity=100010000&industry=&position='
    response = requests.get(url, headers=headers)
    html = response.content.decode('utf-8')
    e_html = etree.HTML(html)
    a_list = e_html.xpath('//li[@class="child-li selected"]/ul//a')
    for a in a_list[1:]:
        a_href = a.xpath('./@href')[0]
        c_name = a.xpath('./text()')[0]
        c_num = a_href.split('/')[1][1:]
        collection_name = change_name(c_name)
        city[collection_name] = c_num
    return city


def get_ajax_data(page, city_num):
    url = f'https://www.zhipin.com/mobile/jobs.json?page={str(page)}&city={city_num}&query={KEYWORDS}'
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def get_all_page():
    cities = get_city_dict()
    for c_name in cities:
        print(f'当前爬取城市：{c_name}')
        for page in range(100):
            try:
                li_html = get_ajax_data(page+1, cities[c_name])['html']
                parse(li_html, c_name)
                print(f'当前页码:{page+1}')
            except Exception as e:
                print(f'{c_name}职位爬取完成！')
                break


def parse(html, c_name):
    e_html = etree.HTML(html)
    li_list = e_html.xpath('//li')
    for li in li_list:
        detail = li.xpath('./a/@href')[0]
        company_name = li.xpath('./a/div/div[2]/text()')[0]
        salary = li.xpath('./a/div/div[1]/span/text()')[0]
        address = li.xpath('./a/div/div[3]/em[1]/text()')[0]
        experience = li.xpath('./a/div/div[3]/em[2]/text()')[0]
        education = li.xpath('./a/div/div[3]/em[3]/text()')[0]
        job_name = li.xpath('./a/div/div[1]/h4/text()')[0]
        job_describe = job_detail(detail)
        dict_item = {
            'job_name': job_name,
            'salary': salary,
            'experience': experience,
            'education': education,
            'company_name': company_name,
            'detail': detail,
            'address': address,
            'job_describe': job_describe}
        job_detail_insert_info(dict_item, c_name)


def job_detail(href):
    url = 'https://www.zhipin.com' + href
    response = requests.get(url, headers=headers)
    html = response.content.decode('utf-8')
    e_html = etree.HTML(html)
    describe = ''.join(e_html.xpath('//div[@class="detail-content"]/div[1]/div/text()')).strip()
    return describe


def main():
    start = time.time()
    print(f'开始时间：{start}')
    get_all_page()
    end = time.time()
    print(f'开始时间：{end}')
    print(f'总共时间：{(end-start)/60}min')


if __name__ == '__main__':
    main()

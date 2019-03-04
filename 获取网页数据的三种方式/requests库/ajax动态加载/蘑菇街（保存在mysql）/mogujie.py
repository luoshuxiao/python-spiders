# 蘑菇街，数据属于动态加载，在开发者工具的Network中的XHR下查看ajax的响应数据

import requests
import json
import re

from mysql_helper import *

db = get_connection()
cursor = get_cursor(db)


def get_page():
    url = 'https://list.mogujie.com/search?callback=jQuery21103638300469383555_1551076139001&_version=8193&ratio=3%3A4&cKey=15&page=1&sort=pop&ad=0&fcid=50240&action=clothing&acm=3.mce.1_10_1hf4o.109499.0.wuiN5rj4h3vWR.pos_0-m_406352-sd_119-mf_15261_1087727-idx_0-mfs_5-dm1_5000&ptp=1._mf1_1239_15261.0.0.oZ2AphU7&_=1551076139002'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None


def parse_page(html):

    #  方法一：正则匹配取出有效数据  获取的数据：/**/jQuery21102294156122079547_1550628385626(有效数据);
    # pattern = re.findall(r'/\*\*/jQuery21102294156122079547_1550628385626\((.*?)\);', html)[0]
    #  方法二：用字符串下标范围，取出有效数据
    index = html.index('(')  # 找出（ 的下标
    index1 = html.index(')')  # 找出 ） 的下标
    pattern = html[index+1:index1:]

    result_dict = json.loads(pattern)
    result_list = result_dict['result']['wall']['docs']
    for item in result_list:
        insert_data_mogujie(db, cursor, item)
    return result_list


def main():
    print(parse_page(get_page()))
    close_cursor(db)


if __name__ == '__main__':
    main()



# 瓜子二手车网数据（正则匹配解析获取的html页面，直接获取页面即可得到数据）

import requests
import re
import json


# 获取网页页面
def get_html(page):
    headers = {
        "Cookie": "uuid=24e367d2-7348-4af0-f5c2-6f9f0c064049; ganji_uuid=5426077132895528005504; preTime=%7B%22last%22%3A1550495820%2C%22this%22%3A1550495795%2C%22pre%22%3A1550495795%7D; lg=1; clueSourceCode=10103000412%2300; sessionid=ebd72519-418f-44c4-eb8e-e78bc3e12d53; cainfo=%7B%22ca_s%22%3A%22pz_sogou%22%2C%22ca_n%22%3A%22pz_bt%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22%25E5%25A4%25A7%25E4%25BC%2597%25E9%2580%2594%25E9%2594%25902018%25E6%25AC%25BE%25E6%258A%25A5%25E4%25BB%25B7%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%2289589737999%22%2C%22scode%22%3A%2210103000412%22%2C%22ca_transid%22%3A%228873993585063702976%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22ca_b%22%3A%22-%22%2C%22ca_a%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%2224e367d2-7348-4af0-f5c2-6f9f0c064049%22%2C%22sessionid%22%3A%22ebd72519-418f-44c4-eb8e-e78bc3e12d53%22%7D; cityDomain=cd; rfnl=https://www.guazi.com/www/?ca_s=pz_sogou&ca_n=pz_bt&scode=10103000412; antipas=7715pg5730Z5e85O3540288Z434",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    url = 'https://www.guazi.com/cd/buy/o' + str(page) + '/'
    response = requests.get(url, headers=headers)
    print(response.content.decode('utf-8'))
    return response.content.decode('utf-8')


def pares_html(html):
    # 解析汽车标题
    pattern = re.compile('<li data-scroll-track=".*?" >.*?title="(.*?)"', re.S)
    title = re.findall(pattern, html)
    print(title)
    print(len(title))
    # 购买年份，行驶公里
    pattern = re.compile('<div class="t-i">(.*?)年.*?</span>(.*?)公里.*?</div>')
    year_dis = re.findall(pattern, html)
    print(year_dis)
    print(len(year_dis))
    # 现价
    pattern = re.compile('<div class="t-price">.*?<p>(.*?)<span>万</span></p>', re.S)
    now_price = re.findall(pattern, html)
    print(now_price)
    print(len(now_price))
    # 原价
    pattern = re.compile('<i class=\'i-blue\'>.*?</i><em class=\'line-through\'>(.*?)</em>', re.S)
    old_price = re.findall(pattern, html)
    print(old_price)
    print(len(old_price))
    result = []
    for i in range(len(title)):
        if re.fullmatch('<span.*', now_price[i]):
            old_price.insert(i, '补贴')
        # a = [title[i], '/'.join(year_dis[i]), now_price[i], old_price[i]]
        # result.append(a)
    print(len(old_price))
    return result


def get_all_html():
    result_list = []
    for i in range(1):
        page = i * 40
        print(str(i)*10)
        html = get_html(page)
        result_list.append(pares_html(html))
    return result_list


def main():
    get_all_html()


if __name__ == '__main__':
    main()
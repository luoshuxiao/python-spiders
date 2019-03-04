#  adidas官网男鞋数据（ajax动态加载，网页滑动到底部时自动请求下一个ajax并刷新数据）
#  在开发者工具的Network中的XHR下查看ajax的响应数据


import json
import requests


def get_one_ajax(g, i):
    """
    取第g页的第i个个ajax刷新的数据
    :param g: 页码
    :param i: ajax加载数
    :return: ajax数据（json）
    """
    url = 'https://www.adidas.com.cn/plp/waterfall.json?commingsoontype=&ni=62&pf=25-40%2C25-60%2C25-60%2C25-40%2C25-60%2C25-60&cf=2-8%2C2-8&pr=-&fo=p25%2Cp25%2Cc2%2Cp25%2Cp25%2Cc2&pn='+ str(g) +'&pageSize=120&c=%E9%9E%8B%E7%B1%BB-%E9%9E%8B%E7%B1%BB&p=undefined-%E7%94%B7%E5%AD%90%26undefined-%E4%B8%AD%E6%80%A7%26undefined-%E7%94%B7%E5%AD%90%26undefined-%E4%B8%AD%E6%80%A7&isSaleTop=false&cp='+ str(i) +'&ps=1&iz=120&ci=496'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None


def parse_one_ajax(html):
    """
    解析数据
    :param html:  待解析的json数据
    :return: 解析后的有效数据（list）
    """
    html = json.loads(html)
    try:
        data = html['returnObject']['view']['items']
    except Exception as e:
        data = []
    finally:
        return data


def parse_all_page():
    """
    获取所有页面，所有ajax加载的数据
    :return: 所有数据（list）
    """
    one_page_data = []
    for i in range(6):
        i += 1
        for j in range(6):
            j += 1
            one_page_data += parse_one_ajax(get_one_ajax(i, j))
        print(f'前{i}页共:{len(one_page_data)}男鞋')
    return one_page_data


def main():
    print(parse_all_page())
    # print(len(parse_all_page()))


if __name__ == '__main__':
    main()
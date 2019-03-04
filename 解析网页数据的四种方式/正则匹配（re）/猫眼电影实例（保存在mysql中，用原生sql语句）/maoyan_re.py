#  猫眼电影（正则匹配解析爬取的网页数据，直接获取页面就能获得数据）
#   保存图片
#  保存爬取到的数据到指定文件
#   保存数据到数据库


import requests
import re
import json

from mysql_helper import *

# 与数据库建立连接
db = get_connection()
#  获取游标
cursor = get_cursor(db)


# 获取网页
def get_page(page):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    url = 'http://maoyan.com/board/4?offset=' + str(page)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None


# 获取所有页面
def get_all_pages():
    pages_list = []
    for i in range(10):
        page = i * 10
        print(str(page) + ('=' * 10))
        html = get_page(page)
        result = parse_page(html)
        pages_list.append(result)
    return pages_list


# 保存图片,写入文件
def save_cover_image(cover_url):
    response = requests.get(cover_url)
    filename = cover_url.split('/')[-1].split('@')[0]
    with open('./static/images/%s' % filename, 'wb') as f:
        f.write(response.content)


# 解析网页
def parse_page(html):
    # 片名：
    pattern = re.compile('movieId.*?>.*?<img.*?<img.*?alt="(.*?)" class.*?', re.S)   # re.S表示消除空格符
    movie_names = re.findall(pattern, html)
    print(movie_names)
    # 主演：
    pattern = re.compile(r'<p class="star">(.*?)</p>', re.S)
    actors = re.findall(pattern, html)
    actors_list = [actor.strip() for actor in actors]
    print(actors_list)
    # 上映时间：
    pattern = re.compile(r'<p class="releasetime">(.*?)</p>', re.S)
    releasetimes = re.findall(pattern, html)
    releasetimes = [releasetime.strip() for releasetime in releasetimes]
    print(releasetimes)
    # 图片
    pattern = re.compile('movieId.*?>.*?<img.*?<img.*?data-src="(.*?)" alt.*?', re.S)
    imgs = re.findall(pattern, html)
    imgs = [img.strip() for img in imgs]
    print(imgs)
    # 排名
    pattern = re.compile('<i class="board-index board-index-(.*?)">.*?</i>', re.S)
    rank = re.findall(pattern, html)
    rank = [r.strip() for r in rank]
    print(rank)
    # 评分
    pattern = re.compile('<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>', re.S)
    scores = re.findall(pattern, html)
    scores = [''.join(score) for score in scores]
    print(scores)
    # 详细信息链接
    pattern = re.compile('<div class="movie-item-info">.*?<p class="name"><a href="(.*?)" title', re.S)
    details = re.findall(pattern, html)
    details = [detail.strip() for detail in details]
    print(details)
    #  组装json
    result_list = []
    for i in range(len(movie_names)):
        result_dict = {}
        result_dict['move_name'] = movie_names[i]
        result_dict['actor'] = actors_list[i]
        result_dict['releastime'] = releasetimes[i]
        result_dict['img'] = imgs[i]
        # 保存图片到本地
        save_cover_image(imgs[i])

        result_dict['rank'] = rank[i]
        result_dict['score'] = scores[i]
        result_dict['detail'] = details[i]
        # 将数据插入数据库
        insert_data(db, cursor, result_dict)

        result_list.append(result_dict)
    return result_list


# 保存爬取的数据
def save_json_file(result):
    with open('maoyan.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


def main():
    html = get_all_pages()
    print(html)
    save_json_file(html)


if __name__ == '__main__':
    main()
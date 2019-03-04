# 靓汤（BeautifulSoup）解析爬取的html页面

from bs4 import BeautifulSoup
import requests
import re


# 取页面HTML
def get_one_page():
	url = "http://sports.sina.com.cn/nba/"
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre" 
	}
	response = requests.get(url, headers=headers)
	# print(response.status_code)
	if response.status_code == 200:
		text = response.content.decode('utf-8')
		return text
	return None


def	parse_with_bs4(html):
	# html = '<p><div><a></a></div></p>'
	# print(html)
	soup = BeautifulSoup(html, 'lxml')
	
	# 让页面标签整齐的输出
	# print(soup.prettify())
	# head标签里面title的文字内容
	# print(soup.title.string)
	# 取整个指定的标签
	# print(soup.head)
	# print(type(soup.head))
	# 遇到的第一个p标签对象
	# print(soup.p)
	# 获取标签名
	# print(soup.p.name)
	#  获取属性值
	# print(soup.img.attrs["src"])
	# print(soup.img.attrs)
	# print(soup.img.attrs['src'])
	# print(soup.img['src'])
	# print(soup.p)
	#  获取p标签内的所有标签对象
	# print(soup.p.contents)

	# print(list(soup.a.parents))
	# print(list(soup.a.parents)[0].attrs['class'])

	# print(soup.head.title.string)
# 获取class为news-list-b的标签下的class为list下的class为item下的p标签下的a标签
# 	result = soup.select('.news-list-b .list .item p a')
# 	for item in result:
# 		print(item.string)
# 		print(item['href'])
#  获取属性class = "-live-layout-row layout_sports_350_650"的标签对象（class属性值有多个）
	result = soup.select('.-live-layout-row.layout_sports_350_650')
	print(result)

	# l = soup.select('.ct_t_01 a')
	# for item in l:
	# 	print(item.string)
	# 	print(item['href'])
	# print(len(l))
	# item = soup.select('#syncad_1 p')[0]
	# print(item)
	# print(item.contents)
	# print(len(item.contents))
	# item = soup.select('.b_time')[0].string
	# print(item)


def main():
	html = get_one_page()
	# print(html)
	parse_with_bs4(html)


if __name__ == '__main__':
	main()
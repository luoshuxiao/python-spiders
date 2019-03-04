#  美团网（ajax动态，一次性加载完数据，在开发者工具的Network中的XHR下查看ajax的响应数据）

import requests
import re
import json


# 获取网页
def get_page():
	url = 'http://cd.meituan.com/meishi/b6119/'
	headers = {
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)" 
	}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		return response.content.decode('utf-8')
	return None


def main():
	html = get_page()
	print(html)
	pattern = re.compile('"poiInfos":(.*?)},"comHeader"', re.S)
	meituan_list = re.findall(pattern, html)
	meituan_result = json.loads(meituan_list[0])
	print(len(meituan_result))
	for item in meituan_result:
		print(item['title'])


if __name__ == '__main__':
	main()
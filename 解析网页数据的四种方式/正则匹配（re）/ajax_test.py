import requests
from urllib.parse import urlencode
import json
from spider_save_helper import save_item

'''
https://list.mogujie.com/search?callback=jQuery21109528018020686176_1536678057418&_version=8193&ratio=3%3A4&cKey=15&page=1&sort=pop&ad=0&fcid=10059141&action=sports
'''

def get_page(page):
	params = {
		'callback': 'jQuery21109528018020686176_1536678057418',
		'_version': 8193,
		'ratio': '3%3A4',
		'cKey': 15,
		'page': page,
		'sort': 'pop',
		'ad': 0,
		'fcid': '10059141',
		'action': 'sports'
	}
    # urlencode将参数params解析为符合url格式的字符串
	url = 'https://list.mogujie.com/search?' + urlencode(params)

	headers =  {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre" 
	}
	response = requests.get(url, headers=headers)
	print(response.status_code)
	if response.status_code == 200:
		text = response.content.decode('utf-8')
		return text
	return None


def get_images(json_dict):
	docs = json_dict['result']['wall']['docs']
	for item in docs:
		item_dict = {}
		item_dict['img'] = item['img']
		item_dict['title'] = item['title']
		item_dict['org_price'] = item['orgPrice']
		item_dict['price'] = item['price']
		yield item_dict

def parse_json(text):
	text = text.replace('/**/jQuery21109528018020686176_1536678057418(', '')[:-2]
	json_dict = json.loads(text)
	return json_dict

def get_pages():
	page = 1
	while True:
		text = get_page(page)
		json_dict = parse_json(text)
		is_end = json_dict['result']['wall']['isEnd']
		if is_end:
			return
		result = get_images(json_dict)
		for item in result:
			print(item)
			save_item(item)
		page += 1

def main():
	result_list = []
	get_pages()

if __name__ == '__main__':
	main()
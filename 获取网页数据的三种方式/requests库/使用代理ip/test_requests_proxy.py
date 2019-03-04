import requests

proxy = '185.41.112.29:57190'
proxies = {
	'http': 'http://' + proxy, 
	'https': 'https://' + proxy	
}
headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'	
}

try:
	response = requests.get('http://httpbin.org/get', headers=headers, proxies=proxies)
	print(response.text)
except requests.exceptions.ConnectionError as e:
	print('Error', e.args)
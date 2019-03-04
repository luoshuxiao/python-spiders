from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

proxy = '185.41.112.29:57190'
proxy_handler = ProxyHandler ({
	'http': 'http://' + proxy, 
	'https': 'https://' + proxy	
})

opener = build_opener(proxy_handler)
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'), 
					('Accept-Encoding', 'gzip, deflate')]

try:
	response = opener.open('http://httpbin.org/get')
	
	print(response.read().decode('utf-8'))
except URLError as e:
	print(e.reason)
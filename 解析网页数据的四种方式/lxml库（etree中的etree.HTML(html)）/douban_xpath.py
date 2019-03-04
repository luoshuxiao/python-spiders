#  豆瓣网，直接获取页面，用xpath解析获取到的html页面

import requests
import re
from lxml import etree


# 取页面HTML
def get_one_page():
	url = "https://www.douban.com/group/explore"
	headers = {
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)" 
	}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		text = response.content.decode('utf-8')
		return text
	return None


# 解析页面
def parse_with_xpath(html):
	etree_html = etree.HTML(html)
	print(etree_html)

	# channel_result = etree_html.xpath('//div[@class="channel-item"]')
	# for channel in channel_result:
	# 	title = channel.xpath('./div[@class="bd"]/h3/a/text()')[0]	
	# 	print(title)		

	# title_result = etree_html.xpath('//div[@class="channel-item"]/div[@class="bd"]/h3/a/text()')
	# print(title_result)

	# 匹配所有节点 //*
	# result = etree_html.xpath('//*')
	# print(result)
	# print(len(result))

	# 匹配所有子节点 //a    文本获取：text()
	# result = etree_html.xpath('//a/text()')
	# print(result)

	# 查找元素子节点 /
	# result = etree_html.xpath('//div/p/text()')
	# print(result)

	# 查找元素所有子孙节点 //
	# result = etree_html.xpath('//div[@class="channel-item"]')
	# print(len(result))
	# | 表示同时取多个节点
	# result = etree_html.xpath('//div[@class="channel-item"] | //span[@class="pubtime"]/../span/a/text()')
	# print(result)

	# 父节点 ..
	# result = etree_html.xpath('//span[@class="pubtime"]/../span/a/text()')
	# print(result)

	# 属性匹配 [@class="xxx"]
	# 文本匹配 text() 获取所有文本//text()
	# result = etree_html.xpath('//div[@class="article"]//text()')
	# print(result)

	# 属性获取 @href
	# result = etree_html.xpath('//div[@class="article"]/div/div/@class')[0]
	# print(result)
	# result = etree_html.xpath('//div[@class="bd"]/h3/a/@href')
	# print(result)

	# 属性多值匹配 contains(@class 'xx') (此时text()[1]表示取文本中的第一个文本)
	# result = etree_html.xpath('//div[contains(@class, "grid-16-8")]//div[@class="likes"]/text()[1]')
	# print(result)

	# 多属性匹配 or, and, mod, //book | //cd, + - * div = != < > <= >=
	# result = etree_html.xpath('//span[@class="pubtime" and contains(text(), "-12-29")]/text()')
	# print(result)

	# 按序选择 [1] -- 第一个， [last()] -- 最后一个， [position() < 3] -- 前两个， [last() -2] -- 倒数第3个
	# 节点轴
	# result = etree_html.xpath('//div/child::div[@class="likes"]/following-sibling::*//span[@class="pubtime"]/text()')
	# print(result)
	# print(len(result))

	# //li/ancestor::*  li所有祖先节点
	# //li/ancestor::div div这个祖先节点
	# //li/attribute::* attribute轴，获取li节点所有属性的值
	# //li/child::a[@href="link1.html"]  child轴，获取直接子节点
	# //li/descendant::span 获取所有span类型的子孙节点	
	# //li/following::* 选取文档中当前节点的结束标记之后的所有节点
	# //li/following-sibling::*     选取当前节点之后的所有同级节点

	# result = etree_html.xpath('//div[@class="channel-item"][1]/following-sibling::*')
	# print(result)
	# print(len(result))

	# results = etree_html.xpath('//div[contains(@class, "channel-group-rec")]//div[@class="title"]/following::*[1]/text()')
	# print([result.strip() for result in results])


def main():
	html = get_one_page()
	# print(html)
	parse_with_xpath(html)


if __name__ == '__main__':
	main()
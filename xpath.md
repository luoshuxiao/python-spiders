#lxml库(支持HTML和XML解析，xpath解析方式)
**xpath是XQuery的一个子集，XQuery是处理xml和html页面的路径查询语言，专用于xml中沿着路径（专业术语叫轴）查找数据用的，可以返回单个元素、文本元素、多个元素节点、属性节点等**

##1.安装并导入 -- pip install lxml
	导入库etree：
	from lxml import etree 
	将页面数据html转为etree对象：
	etree_html = etree.HTML(html)
##2.调用xpath方法解析：

	匹配对象中所有节点 --> //* 
	result = etree_html.xpath('//*') -- 结果是Elenment对象
	
	匹配所有a标签节点 --> //a
	result = etree_html.xpath('//a') -- 结果是Elenment对象
	
	获取文本 --> text()
	result = etree_html.xpath('//a/text()') -- 结果是元素是文本的列表
	
	
	查找元素子节点 --> /
	result = etree_html.xpath('//div/p/text()')
	
	查找元素class属性匹配的所有子孙节点 --> //
	result = etree_html.xpath('//div[@class="channel-item"]')
	
	查找多个节点 --> | (或者的意思)
	result = etree_html.xpath('//div[@class="channel-item"] | //span[@class="pubtime"]/../span/a/text()')
	
	查询获取节点的父节点 --> ..
	result = etree_html.xpath('//span[@class="pubtime"]/..')
	
	查询或者属性的值 
	result = etree_html.xpath('//div[@class="article"]/div/@class')
	
	属性多值匹配（包含）
	result = etree_html.xpath('//div[contains(@class, "grid-16-8")]
	
	多属性匹配 --> or, and, mod, //book | //cd, + - * div = != < > <= >=
	result = etree_html.xpath('//span[@class="pubtime" and contains(text(), "-12-29")]/text()')
	
	按顺序选择获取节点 -->
	 [1] -- 第一个， [last()] -- 最后一个， [position() < 3] -- 前两个， [last() -2] -- 倒数第3个 
	result = etree_html.xpath('//div[1]')
	result = etree_html.xpath('//div[last()]')
	
	
	其他按条件匹配获取节点方式：
	
	//li/ancestor::*  li所有祖先节点
	//li/ancestor::div div这个祖先节点
	//li/attribute::* attribute轴，获取li节点所有属性的值
	//li/child::a[@href="link1.html"]  child轴，获取直接子节点
	//li/descendant::span 获取所有span类型的子孙节点	
	//li/following::* 选取文档中当前节点的结束标记之后的所有节点
	//li/following-sibling::*     选取当前节点之后的所有同级节点
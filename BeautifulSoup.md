#BeautifulSoup -- 靓汤

##一.安装 -- pip install beautifulsoup4
	导入BeautifulSoup库:
	 from bs4 import BeautifulSoup
	
	调用解析器，生成网页数据html的解析对象：
	soup = BeautifulSoup(html, 'lxml')
	
	beautifulsoup的四种解析器：
	
	Python标准库 -- BeautifulSoup(html, 'html.parser') -- 速度 一般，容错能力好
	lxml HTML解析器BeautifulSoup(html, 'lxml') -- 速度快，容错好
	lxml xml解析器 BeautifulSoup(markup, 'xml') -- 速度快，唯一支持xml
	html5lib 解析器 BeautifulSoup(markup, 'html5lib') -- 容错性高，速度慢
	
	a = soup.prettify() -- 将网页格式化，有缩进的格式整齐输出  (print(a))
	title = soup.title.string -- 取网页title的内容
	head = soup.head -- 取head标签所有内容（有多个标签，只取第一个）
	name = soup.p.name -- 获取标签名
	
	获取标签的某一个属性值 -- 返回字符串
	print(soup.img.attrs["src"])
	print(soup.img['src'])
	
	获取该标签的所有属性值 -- 返回结果是一个字典
	print(soup.img.attrs)
	
	获取p标签中所有标签对象 -- 返回列表，元素是标签的bs对象
	a= soup.p.contents
	
	获取的标签对象可以继续选择 
	soup.head.title.string
	
	取节点下面所有子节点列表
	soup.p.contents
	
	
		soup.p.descendants -- 取节点所有子孙节点
		soup.a.parent -- 取父节点
		soup.a.parents --  取所有祖先节点
		soup.a.next_sibling -- 同级下⼀节点
		soup.a.previous_sibling -- 同级上⼀节点
		soup.a.next_siblings -- 同级所有后⾯节点
		soup.a.previous_siblings -- 同级所有前⾯节点
		列子：  list(soup.a.parents)[0].attrs['class'])
	
	方向选择器：
	
		根据属性和文本查找 -- 
		for ul in soup.find_all(name="ul"):
		 print(ul.find_all(name="li"))
		 for li in ul.find_all(name="li"):
		 print(li.string)
		soup.find_all(attrs={"id": "list-1"})
		
		css选择器：
		soup.select('.panel .panel_heading')
		soup.select('ul li')
		soup.select('#id1 .element')
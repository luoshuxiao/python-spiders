#selenium库 -- 模拟用户登陆，并解析网页

应用现状：

selenium模拟浏览器进行数据抓取无疑是当下最通用的数据采集方案，它通吃各种数据加载方式，能够绕过客户JS加密，绕过爬虫检测，绕过签名机制。它的应用，使得许多网站的反采集策略形同虚设。由于selenium不会在HTTP请求数据中留下指纹，因此无法被网站直接识别和拦截

selenium在运行的时候会暴露出一些预定义的Javascript变量（特征字符串），例如"window.navigator.webdriver"，在非selenium环境下其值为undefined，而在selenium环境下，其值为true（如下图所示为selenium驱动下Chrome控制台打印出的值）


大众点评网的验证码表单页，如果是正常的浏览器操作，能够有效的通过验证，但如果是使用selenium就会被识别，即便验证码输入正确，也会被提示“请求异常,拒绝操作”，无法通过验证


知道了屏蔽的原理，只要我们能够隐藏这些特征串就可以了。但是还不能直接删除这些属性，因为这样可能会导致selenium不能正常工作了。我们采用曲线救国的方法，使用中间人代理，比如fidder, proxy2.py或者mitmproxy，将JS文件（本例是yoda.*.js这个文件）中的特征字符串给过滤掉（或者替换掉，比如替换成根本不存在的特征串），让它无法正常工作，从而达到让客户端脚本检测不到selenium的效果

## 安装： pip install selenium

## 安装浏览器驱动： 
	查找到与自己装的浏览器先匹配的驱动进行下载
	淘宝镜像驱动下载地址：https://npm.taobao.org/mirrors/chromedriver
    最好将下载的chromdriver.exe ⽂件放到Python Scripts⽬录下或者配置PATH路径
## 导入selenium库,生成浏览器对象 

可以复制导入以下常用函数 

	from selenium import webdriver
	from selenium.common.exceptions import TimeoutException
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC
	from selenium.webdriver import ActionChains
生成浏览器对象：

	brower = webdriver.Chrome()

生成无头浏览器对象：

	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	brower = webdriver.Chrome(chrome_options=chrome_options)
设置网页窗口大小

    browser.set_window_size(1400, 700)
设置最大等待时间

    wait = WebDriverWait(browser, 5)

访问网页，生成网页页面对象

	browser.get('https://www.mkv99.com/vod-detail-id-9462.html')

## selenium相关函数方法：

	获取渲染数据后的页面内容
	a= browser.page_source
	
	获取当前页面的url
	browser.current_url
	
	获取当前页面的cookies
	browser.get_cookies()
	
	根据节点的id查找获取节点对象
	input1 = browser.find_element_by_id('1thUrlid第01集')
	
	获取节点属性值
	href = input1.get_attribute('href'))
	
	css选择器获取节点
	input_list = browser.find_elements_by_css_selector('.dwon2')
	
	获取节点在页面中坐标（左上角）
	input1.location
	
	获取节点的宽高
	input1.size

	利用xpath方法获取节点：
	input3 = browser.find_element_by_xpath('//*[@class="dwon2"]')
	通过name的值获取
	input4 = browser.find_element_by_name('CopyAddr1')
	a= input4.tag_name
	通过文本文字获取有该文字的一个标签
	input5 = browser.find_element_by_link_text('今日更新')
	通过文本文字获取有该文字的多个标签
	input6 = browser.find_elements_by_partial_link_text('下载')
	获取节点文本值
	input5.text

    让页面执行js代码（让页面滑动到底部）
    str_js = 'var scrollHeight = document.body.scrollHeight;window.scrollTo(0, scrollHeight);'
    browser.execute_script(str_js)


	通过css选择器选择节点，并且等到该节点能被点击时获取（在最大等待时间内） --
	next_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_topPage .fp-next')))
    通过xpath获取节点，并且等到该节点存在时获取（在最大等待时间内） --
    next_page = wait.until(EC.presence_of_element_located((By.XPATH, '//a')))
    通过text文本内容获取节点，并且等到该节点存在时获取（在最大等待时间内） --
    next_page = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '你好')))
    通过标签名获取节点，并且等到该节点存在时获取（在最大等待时间内） --
    next_page = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
                --其他方法参照具体情况调用--


	模拟用户点击next_page这个标签节点，其他模拟用户的事件在最下面 -- 
	next_page.click()

	模拟用户操作浏览器上节点对象的方法 -- （需指定节点对象来调用下列方法）
	click(on_element=None) ——单击鼠标左键
	click_and_hold(on_element=None) ——点击鼠标左键，不松开
	context_click(on_element=None) ——点击鼠标右键
	double_click(on_element=None) ——双击鼠标左键
	drag_and_drop(source, target) ——拖拽到某个元素然后松开
	drag_and_drop_by_offset(source, xoffset, yoffset) ——拖拽到某个坐标然后松开
	key_down(value, element=None) ——按下某个键盘上的键
	key_up(value, element=None) ——松开某个键
	move_by_offset(xoffset, yoffset) ——鼠标从当前位置移动到某个坐标
	move_to_element(to_element) --鼠标移动到某个元素
	move_to_element_with_offset(to_element, xoffset, yoffset) --移动到距某个元素（左上⾓坐标）多少距离的位置
	perform() ——执⾏链中的所有动作
	release(on_element=None) ——在某个元素位置松开鼠标左键
	send_keys(*keys_to_send) ——发送某个键到当前焦点的元素
	send_keys_to_element(element, *keys_to_send) ——发送某个键到指定元素
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

def f1(browser):
	# 访问页面
	browser.get('https://www.mkv99.com/vod-detail-id-9462.html')
	# # 获取渲染后的页面内容
	# print(browser.page_source)
	# # 获取当前网址
	# print(browser.current_url)
	# # 获取浏览器cookie
	# print(browser.get_cookies())

	# # 根据id获取单个节点
	input1 = browser.find_element_by_id('1thUrlid第01集')
	# print(input1)
	# # # 获取节点属性
	# print(input1.get_attribute('href'))
	
	# # 用css选择器获取单个节点
	# input_list = browser.find_elements_by_css_selector('.dwon2')
	# for item in input_list:
	# 	print(item.get_attribute('href'))
	# print(input2.get_attribute('href'))
	# # # 获取节点在页面的坐标（节点左上角）
	print(input1.location)
	# # # 获取节点的宽高
	print(input1.size)

	# # 用xpath方法获取单个节点
	# input3 = browser.find_element_by_xpath('//*[@class="dwon2"]')
	# print(input3.get_attribute('id'))

	# # 根据name获取单个节点
	# input4 = browser.find_element_by_name('CopyAddr1')
	# print(input4.tag_name)

	# # 根据链接文字获取单个节点
	# input5 = browser.find_element_by_link_text('今日更新')
	# # 获取包含下载的所有节点
	# input6 = browser.find_elements_by_partial_link_text('下载')
	# # 获取节点文本值
	# print(input5.text)
	# print(input6)
def f2(browser):
	browser.get('http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
	# 切换到指定iframe标签内的网站链接（网页里面嵌套的另外一个网站,老版本有，现在很少见）
	browser.switch_to.frame('iframeResult')	
	source = browser.find_element_by_css_selector('#draggable')
	target = browser.find_element_by_css_selector('#droppable')
	# 动作链（连续执行一连串的动作）
	actions = ActionChains(browser)
	# 将选定的源移动到目标的位置（将一个节点source拖到另外一个节点target）
	actions.drag_and_drop(source, target)
	actions.perform()


def main():
	# 使用chrome浏览器
	browser = webdriver.Chrome()
	# 使用Firefox浏览器
	# browser = webdriver.Firefox()
	# 使用Edge浏览器
	# browser = webdriver.Edge()
	# 使用Phantom浏览器(已经没用了)
	# browser = webdriver.PhatomJS()
	# 使用Safari浏览器
	# browser = webdriver.Safari()

	try:
		f2(browser)
	finally:
		# 关闭浏览器
		browser.close()

if __name__ == '__main__':
	main()
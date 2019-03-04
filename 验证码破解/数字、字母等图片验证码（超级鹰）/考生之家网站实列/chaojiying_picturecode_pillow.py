import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree
from PIL import Image
from io import BytesIO

from chaojiying import ChaojiyingClient


chrome_options = webdriver.ChromeOptions()

# 添加无头参数：无头浏览器状态运行爬虫-- 表示电脑桌面不打开浏览器
# chrome_options.add_argument('--headless')   没有界面，但是实质上是要模拟浏览器操作

browser = webdriver.Chrome(chrome_options=chrome_options)

# browser = webdriver.Chrome()
browser.set_window_size(1400, 700)
# 显式等待 针对某个节点的等待
wait = WebDriverWait(browser, 10)
# 超级鹰账号、密码
username = 'carmack'
password = 'Vff635241'

def get_page():
    url = 'http://bm.e21cn.com/log/reg.aspx'
    browser.get(url)
    html = browser.page_source
    return html


# 取浏览器窗口内全图
def get_big_image():
    browser.execute_script('window.scrollTo(0, 300)')
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot


# 取验证码坐标位置（左上角和右下角）
def get_position():
    img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#imgCheckCode')))
    loc = img.location
    size = img.size
    print(loc)
    print(size)
    x1 = loc['x']
    # 记住减去滚动高度
    y1 = loc['y'] - 300
    x2 = loc['x'] + size['width']
    y2 = y1 + size['height']
    return (x1, y1, x2, y2)


def parse_html(html):
    # etree_html = etree.HTML(html)
    screenshot = get_big_image()
    screenshot.save('full_screen.png')

    x1, y1, x2, y2 = get_position()
    crop_image = screenshot.crop((x1, y1, x2, y2))
    file_name = 'crop.png'
    crop_image.save(file_name)

    # 向超级鹰发送图片，获取该图片的验证码
    chaojiying = ChaojiyingClient(username,password,'96001')
    im = open(file_name, 'rb').read()
    captha_str = chaojiying.PostPic(im, 1006)['pic_str']
    #  http: // bm.e21cn.com / log / reg.aspx   网站账户密码
    username_code = 'carmack55'
    password_code = '123456'
    tel = '18511405897'

    print(captha_str)

    input_username = wait.until(EC.presence_of_element_located
                       ((By.CSS_SELECTOR, 'input#username')))
    input_password1 = wait.until(EC.presence_of_element_located
                       ((By.CSS_SELECTOR, 'input#pwd')))
    input_password2 = wait.until(EC.presence_of_element_located
                                 ((By.CSS_SELECTOR, 'input#pwd_Q')))
    input_tel = wait.until(EC.presence_of_element_located
                                 ((By.CSS_SELECTOR, 'input#tel')))
    input_check = wait.until(EC.presence_of_element_located
                                 ((By.CSS_SELECTOR, 'input#CheckCode')))
    sublime = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#btn_login')))
    input_username.send_keys(username_code)
    input_password1.send_keys(password_code)
    input_password2.send_keys(password_code)
    input_tel.send_keys(tel)
    input_check.send_keys(captha_str)
    time.sleep(2)
    sublime.click()


def main():
    html = get_page()
    parse_html(html)


if __name__ == '__main__':
    main()
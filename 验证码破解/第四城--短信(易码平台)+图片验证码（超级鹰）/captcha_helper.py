from PIL import Image
from io import BytesIO

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chaojiying import ChaojiyingClient


# 取浏览器窗口内全图
def get_big_image(browser):
    """
    取整个网页的大截图
    :param browser: 浏览器对象
    :return: 大图（Image对象）
    """
    # browser.execute_script('window.scrollTo(0, 300)')
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot


def get_captha_position(browser, class_str):
    """
    得到浏览器中验证码的坐标
    :param browser: 浏览器对象
    :param class_str: css选择器（定位网页中验证码节点元素）
    :return: 返回验证码的坐标
    """
    wait = WebDriverWait(browser, 5)
    captha = wait.until(EC.presence_of_element_located
                       ((By.CSS_SELECTOR, class_str)))
    location = captha.location
    size = captha.size
    x1 = location['x']
    y1 = location['y']
    width = size['width']
    height = size['height']
    x2 = x1 + width
    y2 = y1 + height
    print(x1, y1, x2, y2)
    print(width, height)
    return (x1, y1, x2, y2)


def get_captcha(browser, class_str):
    """
    向超级鹰发送截下来的验证码图片，超级鹰返回验证码，得到图片验证码
    :param browser: 浏览器对象
    :param class_str: css选择器（定位网页中验证码节点元素）
    :return: 验证码字符串
    """
    full_screen_img = get_big_image(browser)
    #  保存文件在当前文件夹下，文件名为mobile_login.png（完全可以不保存大图）
    full_screen_img.save('mobile_login.png')

    # 获取验证码左上角和右下角坐标
    x1, y1, x2, y2 = get_captha_position(browser, class_str)

    captha_img = full_screen_img.crop((x1, y1, x2, y2))
    captha_img.save('mobile_captha.png')

    # 根据具体情况修改账号、密码、和验证码类型代号
    chaojiying = ChaojiyingClient('carmack', 'Vff635241', '96001')
    im = open('mobile_captha.png', 'rb').read()
    captha_str = chaojiying.PostPic(im, 1006)['pic_str']
    return captha_str


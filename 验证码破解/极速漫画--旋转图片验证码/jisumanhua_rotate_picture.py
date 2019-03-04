import time
import os
import requests

from io import BytesIO
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from compare_picture import *

# 声明一个浏览器对象
browser = webdriver.Chrome()
# 调整浏览器页面大小
browser.set_window_size(1400, 700)
# 设置等待时长
wait = WebDriverWait(browser, 5)
# 登录的账号、密码
username = '18080541491'
password = '123456'
# 设置点击换一组验证码的最大点击次数
MAX_CHANGE_TIMES = 3
# 设置点击登录却登录不上的最大点击次数
MAX_LOGIN_TIMES = 3


def simulate_user():
    """模拟用户登陆极速漫画网站"""
    url = 'http://www.1kkk.com'
    browser.get(url)
    # 点击头像登录，进入图片验证码界面
    img_login = wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@class="header-avatar"]')))
    img_login.click()
    time.sleep(1)
    #  填入账户和密码
    input_user = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="txt_name"]')))
    input_password = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="txt_password"]')))
    input_user.send_keys(username)
    time.sleep(1)
    input_password.send_keys(password)
    global login_num  # 点击登录却登录不上的次数
    login_num = 0
    global change_num  # 点击换一组的次数
    change_num = 0
    while change_num < MAX_CHANGE_TIMES and login_num < MAX_LOGIN_TIMES:
        time.sleep(1)
        # 获取网站页面截图（有验证码）
        screen_img = browser.get_screenshot_as_png()
        # 将byte类型数据转换成Image对象
        screen = Image.open(BytesIO(screen_img))
        # 定位并获取4个图片验证码节点元素
        pictures = [wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//div[@class="form-wrap"]/div//div[{i+2}]'))) for i in range(4)]
        picture_num = 1
        for picture in pictures:
            img = get_cut_img(screen, picture)
            times = confirm_click_times(img, picture_num)
            picture_num += 1
            if click_picture(picture, times):
                #  图片正确，结束本次循环，换下一张图片
                continue
            else:
                # 每点一次换一组，统计次数加一
                change_num += 1
                # 结束for循环，回到while循环开始地方开始执行
                break
        else:
            # for循环正常结束，说明验证码已经完全正确，点击登录
            login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnLogin')))
            login.click()
            login_num += 1
            time.sleep(2)
            if check_login_status():
                break


def click_picture(picture, times):
    """
    点击图片验证码
    :param picture: 图片验证码节点元素
    :param times: 点击次数
    :return: 布尔值（1代表图片已点击至正确状态，0代表无法匹配图片）
    """
    if times == 0:
        return 1
    elif times is None:
        # 点击换一组验证码
        change_img = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="rotate-refresh"]')))
        change_img.click()
        return 0
    else:
        # 点击相应的次数，让验证码变正确
        for _ in range(times):
            picture.click()
        return 1


def check_login_status():
    """
    查看是否登录成功
    :return: 布尔值（1代表已登录，0代表未登录）
    """
    try:
        # 如果网页右上方头像标签有onmouseover="getuserinfo(this);"属性，说明已登陆
        wait.until(EC.presence_of_element_located((By.XPATH, '//img[@onmouseover="getuserinfo(this);"]')))
        print('恭喜，成功登录！')
        return 1
    except Exception as e:
        print('图片匹配成功，但登录不了')
        print('可能原因一：图片匹配算法不能百分之百确认两张图片是否匹配，存在算法漏洞；')
        print('可能原因二：账号或者密码错误。')
        if login_num < 2:
            print('正在重新尝试！请稍后...')
        return 0


def confirm_click_times(browser_img, picture_num):
    """
    确认图片验证码点击次数
    :param browser_img: 图片验证码Image对象
    :return: 点击次数（4除外，4表示无法在本地资源匹配验证码）
    """
    i = 0
    browser_p = PictureHash(browser_img)
    right_imgs = os.listdir('./static/imgs/')
    for img_path in right_imgs:
        i += 1
        img = Image.open('./static/imgs/' + img_path)
        if PictureHash(img).compare(browser_p):
            print(f'第{picture_num}张验证码与imgs文件中的第{i}张图片匹配，并且不用点击')
            return 0
        if PictureHash(img.rotate(90)).compare(browser_p):
            print(f'第{picture_num}张验证码与imgs文件中的第{i}张图片匹配，模拟点击一次')
            return 1
        if PictureHash(img.rotate(180)).compare(browser_p):
            print(f'第{picture_num}张验证码与imgs文件中的第{i}张图片匹配，模拟点击两次')
            return 2
        if PictureHash(img.rotate(270)).compare(browser_p):
            print(f'第{picture_num}张验证码与imgs文件中的第{i}张图片匹配，模拟点击三次')
            return 3
    else:
        print(f'第{picture_num}张验证码在imgs中没有相匹配的资源，'
              f'也可能是图片匹配算法对这张图片无效，模拟点击换一组')
        if change_num < 2:
            print('正在尝试换一组验证码进行匹配，请稍等！...')
        return None


def get_cut_img(screen_img, img):
    """
    剪切网页上的验证码图片
    :param screen_img: 整个网页大图（需包含验证码）
    :param img: 图片验证码在网页中的节点对象
    :return: 切下的图片数据
    """
    location = img.location
    size = img.size
    cut_image = screen_img.crop(
        (location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']))
    return cut_image


def get_picture():
    """下载300张极速漫画网站的图片验证码原始图片"""
    url = 'http://www.1kkk.com//image3.ashx?t=1550843570000'
    headers = {
        'Referer': 'http://www.1kkk.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36'
    }
    for i in range(300):
        response = requests.get(url, headers=headers)
        with open('./static/jisu_images/img' + str(i), 'wb') as f:
            f.write(response.content)
            print(i)


def split_picture(img_path):
    """
    从原始验证码中切出有效图片验证码
    :param img_path: 原始验证码图片地址
    :return: 有效验证码Image对象
    """
    img_file = Image.open(img_path)
    width = int(img_file.size[0])
    height = int(img_file.size[1])
    img1 = img_file.crop((0, 0, width/4, height/4))
    img2 = img_file.crop((width/4, 0, width/2, height/4))
    img3 = img_file.crop((width/2, 0, 3*width/4, height/4))
    img4 = img_file.crop((3*width/4, 0, width, height/4))
    return [img1, img2, img3, img4]


def compare_picture(picture1, picture2):
    """
    判断图片是否相同
    :param picture1: 第一张图片Image对象
    :param picture2: 第二张图片Image对象
    :return: 布尔值（True表示相同，False表示不同）
    """
    img1 = PictureHash(picture1)
    img2 = PictureHash(picture2)
    if img1.compare(img2):
        return 1
    else:
        return 0


def split_all_picture(file_name):
    """
    剪切文件中所有原始验证码图片，并保存
    :param file_name: 图片存放地址
    """
    img_list = os.listdir('./static/jisu_images/')
    for img in img_list:
        imgs = split_picture('./static/jisu_images/' + img)
        save_img(imgs, file_name)


def save_img(img_obj_list, file_name):
    """
    保存图片
    :param img_obj_list: 图片Image对象
    :param file_name: 目标文件夹名
    """
    num = 1
    for img_obj in img_obj_list:
        img_obj.save(f'./static/{file_name}/img{num}.png')
        num += 1


def del_repeat():
    """
    去除重复图片
    :return: 图片Image对象列表
    """
    right_list = os.listdir('./static/right_img/')
    img1 = Image.open('./static/right_img/img1.png')
    result_right_img = [img1]
    for img in right_list[1:]:
        img = Image.open(f'./static/right_img/{img}')
        for right_img in result_right_img[:]:
            return_img = compare_picture(img, right_img)
            if return_img:
                break
        else:
            result_right_img.append(img)
    return result_right_img


def main():
    start_time = time.time()
    # # 从网站下载验证码到本地保存到jisu_images
    # get_picture()

    # # 切图,并存入right_img
    # split_all_picture('right_img')

    # # 去掉旋转到正确位置后，重复的图片,并保存到imgs
    # result_list = del_repeat()
    # save_img(result_list, 'imgs')

    # 模拟用户访问网站,自动破解验证码并登陆
    simulate_user()
    end_time = time.time()
    print(f'''配置以及执行情况如下：
    判断图片相匹配的最低匹配度设置为：{COMPATIBLE}%
    模拟点击换一组的最大次数设置为：{MAX_CHANGE_TIMES}次
    模拟点击登录的最大次数设置为：{MAX_LOGIN_TIMES}次
    模拟点击换一组次数：{change_num}次
    模拟点击登录次数：{login_num}次
    程序主动休眠时间：{5+change_num+3*login_num}s
    程序实现该功能的运行时间：{end_time-start_time}s
    ''')
    if change_num == MAX_CHANGE_TIMES:
        print(f'已点击{MAX_CHANGE_TIMES}次换一组（程序设置的极限），依然无法破解，'
              f'请重启爬虫，或者降低图片匹配算法的匹配度，或者下载适量该网站的原始验证码图片，处理后，更新到本地图片资源库imgs文件夹中')
    if login_num == MAX_LOGIN_TIMES:
        print(f'已点击{MAX_LOGIN_TIMES}次登录（（程序设置的极限）），依然不能登录，'
              f'请检查账号、密码是否正确，或者重启爬虫程序, 或者优化图片匹配算法')


if __name__ == '__main__':
    main()
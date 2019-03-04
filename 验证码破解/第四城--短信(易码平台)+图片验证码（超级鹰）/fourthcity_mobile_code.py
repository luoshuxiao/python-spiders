import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from captcha_helper import get_captcha
from sms_helper import get_sms_message, get_mobile

browser = webdriver.Chrome()
browser.set_window_size(1400, 700)
wait = WebDriverWait(browser, 5)


def go_comment():
    try:
        url = 'https://passport.4c.cn/signup'
        browser.get(url)
        #  填入账户和密码
        input_mobile = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="mobile"]')))
        input_mobile.clear()
        # 获取手机号（超级鹰）
        mobile = get_mobile()
        # 填入手机号
        input_mobile.send_keys(mobile)
        #  点击获取短信验证码
        show_captcha_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="show-captcha"]')))
        show_captcha_button.click()
        time.sleep(2)
        #  获取图片验证码中的字符
        captcha_str = get_captcha(browser, '.captcha-img')
        print(captcha_str)
        # 输入验证码
        input_captcha = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="captcha"]')))
        input_captcha.clear()
        input_captcha.send_keys(captcha_str)
        #  点击获取短信验证码
        get_mobile_code = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="sendsms"]')))
        get_mobile_code.click()
        # 获取短信验证码
        message = get_sms_message(mobile)
        #  输入短信验证码
        input_code = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="code"]')))
        input_code.clear()
        time.sleep(1)
        input_code.send_keys(message)
        # 输入密码
        input_password = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="password"]')))
        input_password.clear()
        input_password.send_keys('123456')
        #  点击同意协议注册
        register_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="nextstep"]')))
        register_button.click()
        time.sleep(2)
        #  点击修改账户按钮
        update_name = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '修改')))
        update_name.click()
        #  输入新的名字
        input_password = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="nickname"]')))
        input_password.clear()
        names = '阶级姐姐哥哥妹妹蕾蕾奶奶美美美美美咩咩咩妹妹妹妹美美美是的妹妹顾客和我妹妹斯大林格妹妹勒看了几个里公开和妹妹你肯定会拿过来的反垄断法就不懂保驾护航可见的我是我搞了个'
        name = ''.join([random.choice(names) for _ in range(4)])
        input_password.send_keys(name)
        #  点击修改
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary"]')))
        submit_button.click()
        #  点击论坛
        communication = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '论坛')))
        communication.click()
        #  点击成都相亲
        communication = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '成都相亲')))
        communication.click()
        #  点击帖子
        time.sleep(3)
        communication = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="我说我会火～ 你信吗"]')))
        communication.click()
        #  让页面滑动到底部
        str_js = 'var scrollHeight = document.body.scrollHeight;window.scrollTo(0, scrollHeight);'
        browser.execute_script(str_js)
        #  输入评论信息
        text_area = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fastpostmessage')))
        text_area.clear()
        text_area.send_keys('喜欢就去追啊，追不到就表白啊，表白不答应就下药啊，药不到就强行上啊，上了就翻脸啊，翻脸就换对象啊，换了继续追啊，追了继续表白啊...')
        # 点击发表回复
        submit_answer = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fastpostsubmit')))
        submit_answer.click()
        time.sleep(120)
    except:
        time.sleep(2)
    finally:
        browser.quit()


def main():
    go_comment()


if __name__ == '__main__':
    main()
import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
# 设置等待时间
wait = WebDriverWait(browser, 5)


def download_music():
    browser.get('https://www.xiami.com/billboard/102')
    src_list = []
    for i in range(5):
        time.sleep(2)
        span = browser.find_element_by_xpath(f'//table/tbody/tr[{i+1}]/td[1]/div/span')
        # span = wait.until(EC.element_to_be_clickable((By.XPATH, f'//table/tbody/tr[{i+1}]/td[1]/div/span')))
        span.click()
        time.sleep(2)
        audio = browser.find_element_by_tag_name('audio')
        src = audio.get_attribute('src')
        # response = requests.get(src)
        # data = response.content
        # with open(f'./static/music/data{i+1}', 'wb') as f:
        #     f.write(data)
        src_list.append(src)
        # # 将页面向下滚动50px
        str_js = 'window.scrollTo(0, 50*%d);' % i
        browser.execute_script(str_js)

    return src_list


def main():
    list_src = download_music()
    print(len(list_src))


if __name__ == '__main__':
    main()
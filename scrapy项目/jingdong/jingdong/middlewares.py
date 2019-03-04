# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JingdongSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JingdongDownloaderSeleniumMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self, timeout=None):
        self.timeout = timeout
        browser = webdriver.Chrome()
        browser.set_window_size(1400, 600)
        self.browser = browser
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))

    def process_request(self, request, spider):
        page = request.meta.get('page', 1)
        if page == 1:
            self.browser.get(request.url)
        #  让页面滑动到底部
        str_js = 'var scrollHeight = document.body.scrollHeight;window.scrollTo(0, scrollHeight);'
        self.browser.execute_script(str_js)
        # #  等待网页加载2秒
        # time.sleep(2)
        #  让页面从底部一点一点的往上滑动
        for i in range(16, 0, -1):
            # js语句：scrollTo(x,y) x表示横轴滚动距离，y表示竖轴滚动距离
            str_js = 'var scrollHeight = document.body.scrollHeight;window.scrollTo(0, (%d * scrollHeight/16));' % (
                        i - 1)
            #  执行javascript语句
            time.sleep(3)
            self.browser.execute_script(str_js)

        html = self.browser.page_source

        # 将页面向下滚动一部分（因为下一页按钮被挡住了，不能点击）
        str_js = 'var scrollHeight = document.body.scrollHeight;window.scrollTo(0, scrollHeight/20);'
        self.browser.execute_script(str_js)
        next_page = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_topPage .fp-next')))
        next_page.click()

        return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8', status=200)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

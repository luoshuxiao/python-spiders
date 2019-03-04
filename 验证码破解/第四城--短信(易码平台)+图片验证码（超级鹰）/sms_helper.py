# -*- coding: utf-8 -*-
# python3.5

# 易码短信服务平台开放接口范例代码
# 语言版本：python版
# 官方网址：www.51ym.me
# 技术支持QQ：2114927217
# 发布时间：217-12-11

from urllib import request
import time
import re

header_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}

# 登陆/获取TOKEN
username = 'carmack'  # 账号
password = 'Vff123456'  # 密码
url = 'http://api.fxhyd.cn/UserInterface.aspx?action=login&username=' + \
    username+'&password='+password
TOKEN1 = request.urlopen(request.Request(
    url=url, headers=header_dict)).read().decode(encoding='utf-8')
if TOKEN1.split('|')[0] == 'success':
    TOKEN = TOKEN1.split('|')[1]
    print('TOKEN是'+TOKEN)
else:
    print('获取TOKEN错误,错误代码'+TOKEN1+'。代码释义：'
                                  '1001:参数token不能为空;1002:参数action不能为空;1003:参数action错误;1004:token失效;'
                                  '1005:用户名或密码错误;1006:用户名不能为空;1007:密码不能为空;1008:账户余额不足;'
                                  '1009:账户被禁用;1010:参数错误;1011:账户待审核;1012:登录数达到上限')

TOKEN = '01138099c52f07a264e5d5b27d17fb04e6b9a8dfb501'  # 输入TOKEN
# 获取账户信息
url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getaccountinfo&token='+TOKEN+'&format=1'
ACCOUNT1 = request.urlopen(request.Request(
    url=url, headers=header_dict)).read().decode(encoding='utf-8')
if ACCOUNT1.split('|')[0] == 'success':
    ACCOUNT = ACCOUNT1.split('|')[1]
    print(ACCOUNT)
else:
    print('获取TOKEN错误,错误代码'+ACCOUNT1)

ITEMID = '5242'  # 项目编号
EXCLUDENO = ''  # 排除号段170_171（有些网站不支持某些区间的电话的验证码）


def get_mobile():
    """
    获取手机号码
    :return: 易码平台生成的手机号
    """
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=' + \
        TOKEN+'&itemid='+ITEMID+'&excludeno='+EXCLUDENO
    MOBILE1 = request.urlopen(request.Request(
        url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if MOBILE1.split('|')[0] == 'success':
        MOBILE = MOBILE1.split('|')[1]
        print('获取号码是:\n'+MOBILE)
        return MOBILE
    else:
        print('获取TOKEN错误,错误代码'+MOBILE1)


def release_mobile(MOBILE):
    """
    释放号码
    :param MOBILE: 易码平台生成的电话号码
    """
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token=' + \
        TOKEN+'&itemid='+ITEMID+'&mobile='+MOBILE
    RELEASE = request.urlopen(request.Request(
        url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if RELEASE == 'success':
        print('号码成功释放')


def get_sms_message(MOBILE):
    """
    获取短信验证码，注意线程挂起5秒钟，每次取短信最少间隔5秒
    :param MOBILE: 手机号（易码平台产生）
    :return: 验证码
    """
    WAIT = 100  # 接受短信时长60s
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=' + \
        TOKEN+'&itemid='+ITEMID+'&mobile='+MOBILE+'&release=1'
    text1 = request.urlopen(request.Request(
        url=url, headers=header_dict)).read().decode(encoding='utf-8')
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1
    while (TIME2-TIME1) < WAIT and not text1.split('|')[0] == "success":
        time.sleep(5)
        text1 = request.urlopen(request.Request(
            url=url, headers=header_dict)).read().decode(encoding='utf-8')
        TIME2 = time.time()
        ROUND = ROUND+1

    ROUND = str(ROUND)
    if text1.split('|')[0] == "success":
        text = text1.split('|')[1]
        TIME = str(round(TIME2-TIME1, 1))
        print('短信内容是'+text+'\n耗费时长'+TIME+'s,循环数是'+ROUND)
    
        # 提取短信内容中的数字验证码
        pat = "验证码(.*?)，"
        IC = 0
        IC = re.findall(pat, text)
        if IC:
            print("验证码是:\n"+IC[0])
            return IC[0]
    else:
        print('获取短信超时，错误代码是'+text1+',循环数是'+ROUND)


# def main():
#     # mobile = get_mobile()
#     # print(mobile)
#
#     message = get_sms_message('15032968946')
#     print(message)
#
#     # time.sleep(1)
#     # release_mobile('18383808420')
# 
#
# if __name__ == '__main__':
#     main()


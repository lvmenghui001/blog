# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://sms.ihuyi.com/register.html
# 注意事项：
# （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
# （2）请使用APIID（查看APIID请登录用户中心->验证码短信->产品总览->APIID）及 APIkey来调用接口；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

# !/usr/local/bin/python
# -*- coding:utf-8 -*-
import http.client
import urllib
import random

host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

# 用户名是登录用户中心->验证码短信->产品总览->APIID
account = "C52017393"
# account = "C00526666"
# 密码 查看密码请登录用户中心->验证码短信->产品总览->APIKEY
password = "9bbcebd297cb83b015e49f9120a11c8c"
# password = "eb4104cb0fed0463bbaedbfc9ec018a0"

def send_sms(text, mobile):
    params = urllib.parse.urlencode (
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection (host, port=80, timeout=30)
    conn.request ("POST", sms_send_uri, params, headers)
    response = conn.getresponse ()
    response_str = response.read ()
    conn.close()
    return response_str

def main(phone):
    #生成验证码
    identify_code = ""
    for i in range(4):
        ch = chr (random.randrange(ord("0"), ord("9") + 1))
        identify_code += ch

    mobile = "%s" % phone
    text = "您的验证码是：%s。请不要把验证码泄露给其他人。" % identify_code
    # print(send_sms(text, mobile))
    print(text,mobile)
    return identify_code

# main("18574140305")
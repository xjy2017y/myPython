# -*- coding: UTF-8 -*-
import json
import re
from bs4 import BeautifulSoup
from format_json import FormatJson
from getobj import GetObj
from db import ConnectDB
from selenium import webdriver
import webbrowser
import urllib2
import random
import time
import sys
import cookielib

from aikaStart import flushIpAgent

list = []
'''cookie_jar = cookielib.LWPCookieJar()        #LWPCookieJar()是管理cookie的工具  cookie中存有个人的私有属性，所以要先拿到cookie的数据
cookie = urllib2.HTTPCookieProcessor(cookie_jar)   #默认的opener并不支持cookie。 那么我们先新建一个支持cookie的opener。urllib2中供我们使用的是HTTPCookieProcessor。
opener = urllib2.build_opener(cookie)
request = urllib2.Request("http://dev.kuaidaili.com/api/getproxy/?orderid=941022314792624&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&carrier=2&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&sep=1")
file_object = opener.open(request).read()
file = file_object.split("\r\n")
for i in file:
    iplist = {}
    iplist["http"] = i.strip()
    list.append(iplist)
# 随机选择一个代理
print list
opener.close()'''
for i in range(0,2):
    list = flushIpAgent()
    time.sleep(6)
proxy = random.choice(list)
# 使用选择的代理构建代理处理器对象

httpproxy_handler = urllib2.ProxyHandler(proxy)
opener = urllib2.build_opener(httpproxy_handler)
request = urllib2.Request("http://newcar.xcar.com.cn/416/config.htm")
response = opener.open(request)
xx  = response.read()
print xx

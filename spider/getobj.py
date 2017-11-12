# -*- coding: utf-8
import cookielib
import urllib2
import urllib
import re
from selenium import webdriver
import chardet
import time
from format_json import FormatJson
from common import *
class GetObj(object):

    def __init__(self,url,default = ""):
        if default == "":
            cookie_jar = cookielib.LWPCookieJar()        #LWPCookieJar()是管理cookie的工具  cookie中存有个人的私有属性，所以要先拿到cookie的数据
            cookie = urllib2.HTTPCookieProcessor(cookie_jar)   #默认的opener并不支持cookie。 那么我们先新建一个支持cookie的opener。urllib2中供我们使用的是HTTPCookieProcessor。
            self.opener = urllib2.build_opener(cookie)   #创建一个opener
            user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"   #修改默认请求头，为了避免自动化程序被拒绝，
            self.url=url          #填充url
            self.send_headers={'User-Agent':user_agent}  #设置
        else:
            self.opener.close() #关闭Opener
            httpproxy_handler = urllib2.ProxyHandler(default)
            self.opener = urllib2.build_opener(httpproxy_handler)
            user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"   #修改默认请求头，为了避免自动化程序被拒绝，
            self.url=url          #填充url
            self.send_headers={'User-Agent':user_agent}  #设置


    def getcodeing(self,obj):
        if obj:
            coding=chardet.detect(obj)["encoding"]   # chardet.detect(obj)返回的是{'confidence': 0.98999999999999999, 'encoding': 'GB2312'}数组格式，在根据字段取encoding值
            return coding   #返回编码类型



    def gethtml(self):
        request = urllib2.Request(self.url,headers=self.send_headers)
        try:
            soures_home={}
            while(True):
                response = self.opener.open(request)
                reurl = response.geturl()
                print reurl
                part = re.compile(r'()(userverify)()')
                xx = re.search(part,reurl)
                if hasattr(xx,'group'):
                    logger.info("需要验证！ "  )
                    driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
                    #     打开网页
                    driver.get(reurl)
                    time.sleep(15)
                    driver.close()
                else:
                    soures_home = self.opener.open(request).read()   #  打开该请求网址，并记录到soures_home中
                    break
        except urllib2.URLError,e:
            logger.info('URLError')
            logger.info(e.reason)
            return None
        except urllib2.HTTPError,e:
            logger.info('URLError')
            print "httpError!!!"
            return None
        return soures_home
    def getconf(self):
        #根据html结果获取配置项的json，并且格式化
        html=self.gethtml()
        coding=self.getcodeing(html)
        if html is not None:
            html=html.decode(coding,"ignore").encode('utf-8')
            c=re.compile(r'(var config =) ({.*})')
            o=re.compile(r'(var option =) ({.*})')
            conf_josn   =   re.search(c,html)
            option_josn =   re.search(o,html)
            #print conf_josn
            if hasattr(conf_josn,'group') and hasattr(option_josn,'group'):    #判断是否有group属性
                conf_josn = conf_josn.group(2)
                option_josn = option_josn.group(2)
                json=FormatJson()
                conf_json=json.format_json(conf_josn,"conf")     #json转成对象
                option_josn=json.format_json(option_josn,"option")
                config = json.json_plus(conf_json,option_josn)
                return config
            else:
                return None
        return None



# -*- coding: utf-8
import threading
import re
import time
import sys
import json
from bs4 import BeautifulSoup
from getobj import GetObj
from db import ConnectDB
from common import *
db=ConnectDB()
url="https://www.autohome.com.cn/"

#获取费第一级分类URL
def GetFirstType(url):
    obj =  GetObj(url)     #得到一个爬虫对象
    html = obj.gethtml()   #得到请求的页面内容
    coding = obj.getcodeing(html)   #得到编码类型
    soup = BeautifulSoup(html,"html5lib",from_encoding=coding)  #将html内容打开，用html5lib做解析器，用coding进行编码
    m=re.compile(r"navcar")     #python通过re模块提供对正则表达式的支持,查找“navcar”字段的字符
    content=soup.find_all("li",attrs={"class":m})   #搜索文档树， 找到<li>标签并且class = navcar
    url1={}
    for item in content:   #循环
        name=item.a.text           #获取子节点<a>的内容
        if name == u"电动车":     #排除掉电动车   中文前加u就是告诉python后面的是个unicode编码，存储时按unicode格式存储。
            continue
        href=item.a.get("href")        #获取链接
        href  = "http:"+href
        url1[name]=href               #存储到数组中
    return url1
    #print "%s : %s" % (name,href)

#数据入库函数

def SaveDataToCarInfo(table_name="",brand="",series="",type_name="",conf="",index=""):
    conf=json.loads(conf)
    for (k,v) in conf.items():
        spaceid = k
        if(v.has_key("0")):
            year = v["0"]
            x = re.compile(r'<(.[^>]*)>')
            year = re.sub(x,"",year)
            #x = re.compile(r'')
            year = year.split('.')[0]       #获取的年份
            print year
        else:
            year = "error"
        if(v.has_key("284")):
            peopleNum =v["284"]
            x = re.compile(r'<(.[^>]*)>')
            peopleNum = re.sub(x,"",peopleNum)
            print peopleNum
        else:
            peopleNum = "error"
        if(v.has_key("555")):
            engine = v["555"]
            x = re.compile(r'<(.[^>]*)>')
            engine = re.sub(x,"",engine)
            print engine
        else:
            engine = "error"
        if(v.has_key("287")):
            displacement = v["287"]
            x = re.compile(r'<(.[^>]*)>')
            displacement = re.sub(x,"",displacement)
            print displacement
        else:
            displacement = "error"

        if type_name == u"微型车":
            type = 0
        elif type_name ==u"小型车":
            type = 1
        elif type_name ==u"紧凑型车":
            type =2
        elif type_name == u"中型车":
            type=3
        elif type_name == u"中大型车":
            type= 4
        elif type_name == u"大型车":
            type = 5
        elif type_name == u"SUV":
            type = 6
        elif type_name ==u"MPV":
            type = 7
        elif type_name == u"跑车":
            type = 8
        elif type_name == u"皮卡":
            type = 9
        elif type_name == u"微面":
            type = 10
        elif type_name == u"轻客":
            type = 11
        db=ConnectDB()
        n = db.select(table_name="carinfo",field="vechiclesID",value=spaceid)
        if n != 0:
            logger.info("spaceid: %s exists " %  spaceid )
            continue
        db.insertTyre(table_name,spaceid,brand,series,type,peopleNum,year,engine,displacement,index)
        db.dbclose()


def SaveData(table_name="",brand="",series="",conf="",status="",URL_="",index="",level="",manufacturer = ""):
    conf=json.loads(conf)  #转化为python对象
    for (k,v) in conf.items():
        spaceid = k
        name = v["567"]
        x = re.compile(r'span>(.*?)<span')
        if name == '-':
            continue
        name1 = re.search(x,name)
        if hasattr(name1,"group"):
            name1 = name1.group(1)
        else:
            x = re.compile(r'</span>(.*?)$')
            name1 = re.search(x,name)
            if hasattr(name1,"group"):
                name1 = name1.group(1)
            else:
                x = re.compile(r'^(.*?)<span')
                name1 = re.search(x,name)
        print name1

        year = v["0"]
        x = re.compile(r'(</span>|>|^)(.*?)($|<|<span)')
        year = re.search(x,year)
        year = year.group(2)

        guide_price = v["219"]
        x = re.compile(r'(</span>|>|^)([1-9]\d*.\d*|0.\d*[1-9]\d*)($|<|</span>)')   #取小数
        temp = re.search(x,guide_price)          #在数组中搜索
        if hasattr(temp,"group"):
            guide_price = temp.group(2)
        else:
            guide_price = 0
        print guide_price

        structure = v["281"]
        structure = re.search(re.compile(r'(</span>|>|^)(.*?)($|<|<span)'),structure).group(2)
        print structure

        emission_standard = v["1072"]
        emission_standard = re.search(re.compile(r'(</span>|>|^)(.*?)($|<|<span)'),emission_standard).group(2)
        print emission_standard
        json_text=json.dumps(v,encoding='utf-8', ensure_ascii=False)
        db=ConnectDB()
        n = db.select(table_name="spider_json",field="spaceid",value=spaceid)
        if n != 0:
            logger.info("spaceid: %s exists " %  spaceid )
            continue
        db.insert(table_name=table_name,
                    spaceid=spaceid,
                    brand=brand,
                    series=series,
                    models=name1,
                    guide_price=guide_price,
                    level=level,
                    emission_standard=emission_standard,
                    structure=structure,
                    status=status,
                    manufacturer=manufacturer,
                    year=year,
                    index=index,
                    json_text="",
                    URL_=URL_)
        db.dbclose()

    
#线程函数
def thrad(type_name,url2):
    #logger.info("name：%s url: %s" % (type_name,url2))
    url2=url2.encode("utf-8")           #用utf-8编码
    obj = GetObj(url2)                  #得到一个爬虫对象
    html=obj.gethtml()                  #获取页面
    coding=obj.getcodeing(html)         #获取编码类型
    soup=BeautifulSoup(html,'html5lib',from_encoding=coding)
    

    #print "----------------------------------------------"
    #print type_name
    #print "----------------------------------------------"
    logger.info("start %s...." % type_name)
    content=soup.find("div",attrs={"class":["tab-content-item","current"]})    #find返回的不是列表是文本
    soup=BeautifulSoup(str(content),'html5lib')    #再返回一个soup对象
    index = soup.find_all('span',attrs={'class':"font-letter"})   #找到字典顺序
    box =  soup.find_all('div',attrs={'class':["uibox-con", "rank-list","rank-list-pic"]})
    for (index,box) in zip(index,box):
    #for item in box:
        #获取字母分割的DIV 同时获取字母索引
        index = index.text.strip()      #默认删除空白符
        brand_soup  = BeautifulSoup(str(box),'html5lib')     #返回一个soup对象
        brand_html=brand_soup.find_all('dl')
        for brand_item in brand_html:
            #品牌名称
            brand  = brand_item.dt.text.strip()        #品牌
            series_html = brand_item.dd
            series_soup=BeautifulSoup(str(series_html),'html5lib')   #根据<dd>标签找到子目录的soup
            manufacturer_name=series_soup.find_all('div',attrs={"class":"h3-tit"})       #品牌名称
            ul=series_soup.find_all('ul',attrs={"class":"rank-list-ul"})
            for (manufacturer,ul_tag) in zip(manufacturer_name,ul):
                #获取厂商名称
                manufacturer=manufacturer.text
                logger.info("start %s...." % manufacturer )
                logger.debug(ul_tag)
                soup=BeautifulSoup(str(ul_tag),'html5lib')
                w=re.compile(r's\d+')
                litag=soup.find_all('li',id=w)
                for item in litag:
                    #获取车系名称
                    series=item.h4.text
                    db=ConnectDB()      #建立数据库连接
                    n=db.select(table_name="carinfo",field="series",value=series)   #查询
                    db.dbclose()  #关闭连接
                    if n != 0:
                        logger.info("%s %s %s exists " % (type_name,brand, series) )    #如果找到，说明存在该条记录
                        continue
                    href=item.h4.a.get("href")                #如果没找到，则取得他的链接地址
                    price=item.div.text                       #记录价格
                    url_id=href.split("/")[3]                 #记录url_id
                    #print "●●%s %s %s" % (series,price,url_id)
                    #拼接在售车辆的配置页面URL
                    sale_conf_url="http://car.autohome.com.cn/config/series/%s.html" % url_id
                    #拼接停售车辆的配置页面URL
                    stop_sale_conf_url="http://www.autohome.com.cn/%s/sale.html" % url_id
                    url_dic={"sale_conf_url":sale_conf_url,"stop_sale_conf_url":stop_sale_conf_url}
                    #threads=[]
                    for (url_name,sale_url) in url_dic.items():
                        #在售
                        if url_name == "sale_conf_url":
                            status=u"在售"
                            #print sale_url
                            #def get_josn():
                            log_mess="%s:%s %s %s %s %s %s %s" % (status,type_name,index,brand,manufacturer,series,price,url_id)
                            obj=GetObj(sale_url)
                            conf=obj.getconf()
                            if conf:
                                #print conf
                                logger.info(log_mess)
                                """SaveData(table_name="spider_json",    #存储到数据库
                                    brand=brand,
                                    series=series,
                                    conf=conf,
                                    status=status,
                                    index=index,
                                    URL_=sale_conf_url,
                                    level=type_name,
                                    manufacturer = manufacturer)"""
                                SaveDataToCarInfo("carinfo",brand,series,type_name,conf,index)
                            else:
                                mess= u"没有找到相关配置"
                                logger.info("%s %s" % (log_mess,mess))
                                #print mess
                        else:
                
                            #停售
                            #def get_stop_conf():
                            status=u"停售"
                            obj=GetObj(sale_url)
                            html=obj.gethtml()
                            coding=obj.getcodeing(html)
                            soup=BeautifulSoup(html,'html5lib',from_encoding=coding)
                            filter_html=soup.find_all('div',attrs={"class":"models_nav"})
                            log_mess="%s:%s %s %s %s %s %s %s" % (status,type_name,index,brand,manufacturer,series,price,url_id)
                            if filter_html:
                                for item in filter_html:
                                    href=item.find('a',text=u'参数配置').get("href")
                                    stop_sale_conf_url_1=url+href
                                    obj=GetObj(stop_sale_conf_url_1)
                                    conf=obj.getconf()
                                    if conf:
                                        #print conf
                                        logger.info("%s %s" % (log_mess,href))
                                        """SaveData(table_name="spider_json",
                                            brand=brand,
                                            series=series,
                                            conf=conf,
                                            status=status,
                                            index=index,
                                            level=type_name,
                                            URL_=stop_sale_conf_url_1)"""
                                        #print u"在售品牌中的停售车辆"
                                        SaveDataToCarInfo("carinfo",brand,series,type_name,conf,index)
                                    else:
                                        mess= u"没有找到相关配置"
                                        logger.info("%s %s %s" % (log_mess,mess,href))
                                        #print mess
                            else:
                                mess= u"没有找到相关配置"
                                logger.info("%s %s" % (log_mess,mess))

def main():
    logger.info("start spider.....")
    url_1=GetFirstType(url)
    for type_name,url2 in url_1.items():            #items()方法用于返回字典dict的(key，value)元组对的列表
        '''t=threading.Thread(target=thrad,args=(type_name,url2))     #对每一种车型都开启一个线程
        t.start()                                                #线程准备就绪，等待调度
        while True:
            if(len(threading.enumerate()) < THARED_NUMBER + 1 ):      #threading.enumerate(): 返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。  这里限制线程数不大于6个
                break'''
        thrad(type_name,url2)
#daemon = Daemonize(app="app", pid=PID_FILE, action=main, keep_fds=keep_fds,logger=logger)
#daemon.start()

if __name__ == "__main__":
    print "start!!"
    main()
    print "finish!!!"

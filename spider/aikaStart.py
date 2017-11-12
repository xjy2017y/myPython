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
import urllib2
import random
import sys
import cookielib
db=ConnectDB()
url="http://newcar.xcar.com.cn/price/"
url2="http://newcar.xcar.com.cn"



def giveFirstLatter(first_latter,item):
   fname = first_latter+".txt"
   path = 'D:/pyLearning/spider-master/spider-master/spider/tmp/'+fname         #添加类型的记录path   需修改
   fobj = open(path,'r+')
   fileList = fobj.read().splitlines()
   fobj.close()
   column_tit = re.compile(r'column_tit')
   column_tit = item.find_all("div",attrs={"class":column_tit})
   width = re.compile(r'848px')
   width = item.find_all("td",attrs={"width":width})
   for (brand,width) in zip(column_tit,width):
        print "--" + brand.a.span.text.strip()
        brands = brand.a.span.text.strip()
        logger.info(u"--品牌"+brand.a.span.text+" start!...")
        item_list = re.compile(r'item_list')
        item_list = width.find_all("div",attrs={"class":item_list})
        for i in item_list:
            print "---"+i.a.get("href")
            text = i.a.get("href").strip()
            if text not in fileList:                #如果没在文本中找到的话，插入href 并写入数据库
                logger.info(u"---车型"+i.a.get("href")+" start!...")
                href =url2 + i.a.get("href") +"config.htm"
                logger.info(u"---链接地址 "+href)
                obj = GetObj(href)
                html = obj.gethtml()
                while(True):
                    if not html is None:
                        coding=obj.getcodeing(html)         #获取编码类型
                        soup=BeautifulSoup(html,'html5lib',from_encoding=coding)
                        base_title = re.compile(r'base_title')
                        base_title = soup.find_all("tr",attrs={"id":base_title})
                        soup2 = base_title[0]           #找到base_title的DOM
                        col = re.compile(r'col')
                        col = soup2.find_all("td",attrs={"scope":col})   #找到td
                        for i in col:
                            model =  i.a.text.strip()                #获取到model
                            logger.info("model "+model)
                            modid = i.get("id")
                            mod = re.compile(r'(mod_)(.*)')
                            carid = re.search(mod,modid)
                            if hasattr(carid,'group'):
                                carid = carid.group(2)
                                string = "bname_"+carid
                                db=ConnectDB()
                                n = db.select(table_name="carInfo1",field="vechiclesID",value=carid)
                                if n != 0:
                                    logger.info("vechiclesID: %s exists " %  carid )
                                    continue
                                series = re.compile(string)
                                series = soup.find("td",attrs={"id":series})
                                if not series is None:                           #获取到series
                                    series  =series.a.text.strip()
                                    logger.info("series "+string)
                                else:
                                    logger.error(string + "not found!!!!")
                                    series = "-"


                                string = "type_name_"+carid                         #获取到carType
                                carType = re.compile(string)
                                carType = soup.find("td",attrs={"id":carType})
                                if not carType is None:
                                    carType = carType.a.text.strip()
                                    logger.info("carType "+carType)
                                else:
                                    logger.error(string + "not found!!!!")
                                    series = "-"


                                string = "m_newseat_"+carid                 #获取到peopleNum
                                peopleNum = re.compile(string)
                                peopleNum = soup.find("td",attrs={"id":peopleNum})
                                if not peopleNum is None:
                                    peopleNum = peopleNum.text.strip()
                                    logger.info("peopleNum "+peopleNum)
                                else:
                                    logger.error(string + "not found!!!!")
                                    peopleNum = "-"


                                string = "syear_" + carid                   #获取到marketTime
                                marketTime = re.compile(string)
                                marketTime = soup.find("td",attrs={"id":marketTime})
                                if not marketTime is None:
                                    marketTime = marketTime.text.strip()
                                    logger.info("marketTime "+marketTime)
                                else:
                                    logger.error(string + "not found!!!!")
                                    marketTime = "-"

                                string = "m_disl_working_mpower_"+carid         #获取到engine
                                engine =re.compile(string)
                                engine = soup.find("td",attrs={"id":engine})
                                if not engine is None:
                                    engine = engine.text.strip()
                                    logger.info("engine "+engine)
                                else:
                                    logger.error(string + "not found!!!")
                                    engine = "-"


                                string ="m_mdisl_"+ carid
                                displacement = re.compile(string)
                                displacement = soup.find("td",attrs={"id":displacement})
                                if not displacement is None:
                                    displacement = displacement.text.strip()
                                    logger.info("displacement "+displacement)
                                else:
                                    logger.error(string + "not found!!!")
                                    displacement = "-"


                                db.insertTyre2("carInfo1",carid,brands,series,carType,peopleNum,marketTime,engine,displacement,first_latter,model)
                                db.dbclose()
                            else:
                                logger.error(modid+u" 该处无法获得汽车id!")
                                break
                        break
                    else:
                        time.sleep(360)
                        html = obj.gethtml()
                fobj = open(path,'a+')
                print u'写入'+first_latter+ ' '+text
                fobj.write(text+'\n')
                fobj.flush()
                fobj.close()
            else:
                logger.info(u"跳过"+i.a.get("href"))
                print u"跳过"+i.a.get("href")
                continue    #否则进行下一条判断
   print first_latter + u"已完成！！！"
   logger.info(first_latter+u"已完成！！！")
'''
def getobj2(opener,href):
    try:
        request = urllib2.Request(href)
        soures_home =opener.open(request).read()

    except urllib2.URLError,e:
            logger.info('URLError')
            logger.info(e.reason)
            return None
    except urllib2.HTTPError,e:
            logger.info('URLError')
            print "httpError!!!"
            return None
    return soures_home

def flushIpAgent():
    ipList = []
    cookie_jar = cookielib.LWPCookieJar()        #LWPCookieJar()是管理cookie的工具  cookie中存有个人的私有属性，所以要先拿到cookie的数据
    cookie = urllib2.HTTPCookieProcessor(cookie_jar)   #默认的opener并不支持cookie。 那么我们先新建一个支持cookie的opener。urllib2中供我们使用的是HTTPCookieProcessor。
    opener = urllib2.build_opener(cookie)
    request = urllib2.Request("http://dev.kuaidaili.com/api/getproxy/?orderid=941022314792624&num=100&area=%E4%B8%AD%E5%9B%BD&b_pcchrome=1&b_pcie=1&b_pcff=1&carrier=2&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&sep=1")
    file_object = opener.open(request).read()
    file = file_object.split("\r\n")
    for i in file:
        list = {}
        list["http"] = i.strip()
        ipList.append(list)
    # 随机选择一个代理
    opener.close()
'''
def GetFirstTypeAika(url):
    obj =  GetObj(url)     #得到一个爬虫对象
    html = obj.gethtml()   #得到请求的页面内容
    coding = obj.getcodeing(html)   #得到编码类型
    soup = BeautifulSoup(html,"html5lib",from_encoding=coding)  #将html内容打开，用html5lib做解析器，用coding进行编码
    container =re.compile(r"container")
    content=soup.find_all("div",attrs={"class":container})   #搜索文档树， 找到<li>标签并且class = navcar
    for item in content:
        first_latter = item.div.text.strip()
        print first_latter
        logger.info(u"字母"+first_latter+" start!...")
        if(first_latter >= 'B'):
            t = threading.Thread(target=giveFirstLatter,args=(first_latter,item))
            t.start()
            while True:
                if(len(threading.enumerate()) < THARED_NUMBER + 1 ):      #threading.enumerate(): 返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。  这里限制线程数不大于6个
                    break
    return
def main():
    logger.info("start spider.....")
    GetFirstTypeAika(url)
    logger.info("finish.....")
    return


if __name__ == "__main__":
    print "start!!"
    '''for line in file_object:
        ip = line.strip()
        xx = {}
        xx["http"] = ip
        ipList.append(xx)'''
    main()
    print "finish!!!"
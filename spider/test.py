# -*- coding: UTF-8 -*-
import json
import re
from bs4 import BeautifulSoup
from format_json import FormatJson
from getobj import GetObj
from db import ConnectDB
from selenium import webdriver
import webbrowser
import sys

#小型车可以
#微型车可以
#紧凑型车可以
#中型车 的人数
#大型车可以
#SUV
#MPV
#

reload(sys)
sys.setdefaultencoding('utf8')
url = "http://newcar.xcar.com.cn/2365/config.htm"
obj=GetObj(url)
html = obj.gethtml()
c = re.compile(r'(var specIDs =)(\[.*\])')
coding = obj.getcodeing(html)   #得到编码类型
soup = BeautifulSoup(html,"html5lib",from_encoding=coding)
print soup
temp = re.search(c,html)
if hasattr(temp,'group'):
    temp = temp.group(2)
else:
    driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
#    driver = webdriver.Firefox()
#     打开网页
    driver.get(url)
ss = json.loads(temp)
data = {}
data["spaceid"] = ss[0]
html=html.decode(coding,"ignore").encode('utf-8')
c=re.compile(r'(var config =) ({.*})')
conf_json= re.search(c,html)
if hasattr(conf_json,'group'):   #如果有group属性，即.group(n)
    xx = conf_json.group(2)
    print xx;
json2 = FormatJson()
conf_json=json2.format_json(xx,"conf")
#db=ConnectDB()
for (k,v) in conf_json.items():
    spaceid = k

    year = v["0"]
    x = re.compile(r'<(.[^>]*)>')
    year = re.sub(x,"",year)
    #x = re.compile(r'')
    year = year.split('.')[0]       #获取的年份
    print year

    peopleNum =v["284"]
    x = re.compile(r'<(.[^>]*)>')
    peopleNum = re.sub(x,"",peopleNum)
    print peopleNum


    engine = v["555"]
    x = re.compile(r'<(.[^>]*)>')
    engine = re.sub(x,"",engine)
    print engine

    displacement = v["287"]
    x = re.compile(r'<(.[^>]*)>')
    displacement = re.sub(x,"",displacement)
    print displacement
    db = ConnectDB()
    db.insertTyre("carinfo",spaceid,"","",1,peopleNum,year,engine,displacement,"S");
    db.dbclose()
"""for (k,v) in conf_json.items():
    spaceid = k
    name = v["<span class='hs_kw0_configpl'></span><span class='hs_kw1_configpl'></span>"]
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
    print unicode(str(v),'unicode-escape')
    #year = v[u"上市<span class='hs_kw11_configpl'></span>"]
    year = re.compile(r'.*"(.*?\\u4e0a\\u5e02.*?)".*')
    if hasattr(year,"group"):
        year = year.search(str(v)).group(1)
        year = v[unicode(year,'unicode-escape')]
        print year
    else:
        year = 0;

    guide_price = re.compile(ur'.*"(.*厂.*?)":.*')
    #guide_price  = guide_price.search(str(v)).group(1)
    guide_price = re.search(guide_price,unicode(str(v),'unicode-escape'))  #搜索
    temp = guide_price.group(1)
    x = re.compile(r'(</span>|>|^)([1-9]\d*.\d*|0.\d*[1-9]\d*)($|<|</span>)')   #取小数
    temp = re.search(x,v[temp])          #在数组中搜索
    if hasattr(temp,"group"):
        guide_price = temp.group(2)
    else:
        xxx = re.compile(ur''+guide_price.group(1)+".+?\"")
        guide_price = re.findall(xxx,unicode(str(v),'unicode-escape'))
        for x in guide_price:
            temp = x.strip('"')
            guide_price = v[temp]
            x = re.compile(r'(</span>|>|^)([1-9]\d*.\d*|0.\d*[1-9]\d*)($|<|</span>)')   #取小数
            temp = re.search(x,guide_price)          #在数组中搜索
            if hasattr(temp,"group"):
                guide_price = temp.group(2)
                break
    print guide_price

    structure=v[u"车身结构"]
    x = re.compile(r'(>|^)(.*)($|<)')
    structure = re.search(x,structure)
    structure = structure.group(2)
    print structure
    level="微型车"
    manufacturer = "xxxxxx"
    #manufacturer=v[u"厂<span class='hs_kw4_configpl'></span>"]  制造商不在这里传值了！！！！！！！！在spider里改
    emission_standard=v[u"变速箱"]    #变速箱
    x = re.compile(r'(>|^)(.*)($|<)')
    emission_standard = re.search(x,emission_standard)
    emission_standard = emission_standard.group(2)
    print emission_standard
    db=ConnectDB()
    n = db.select(table_name="spider_json",field="spaceid",value=spaceid)
    table_name = "spider_json"
    brand =u"通用"
    series =u"宝俊"
    status = u"在售"
    index = "A"
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
                    json_text="sssss",
                    URL_=url)
    db.dbclose()
    """

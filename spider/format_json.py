# -*- coding: utf-8
import json,sys,re
#import chardet
class FormatJson(object):
    def __init__(self):
        pass
    def format_json(self,a,option):
    
        if option == "conf":
            par_type = "paramtypeitems"
            par = "paramitems"
        elif option == "option":
            par_type = "configtypeitems"
            par = "configitems"
    
        comm_dic={}
        veh_dic={}
        for com in json.loads(a)["result"]["specsList"]: #loads方法是把json对象转化为python对象
            keys=com["specid"]      #记录了specid
            comm_dic[keys]={}       #对应的keys装载在comm_dic中
    
        json_data=json.loads(a)["result"][par_type]
        for item in json_data:
            base_name=item["name"]
            paramitems=item[par]
            for base in paramitems :
                veh_name=base["name"]   #
                if base.has_key("id"):
                    veh_id = base["id"]
                else:
                    print "没有ID！！！"
                    print keys
                    continue
                veh_list=base["valueitems"]
                for conf in veh_list:
                    keys=conf["specid"]
                    v_name=conf["value"]
                    if option == "option":
                        v_name=v_name.replace('&nbsp;','')
                        v_name=v_name.replace(u'●',u'有')
                        v_name=v_name.replace(u'-',u'无')
                    while(comm_dic[keys].has_key(str(veh_id))):   #避免重复键值
                        veh_id+=1
                    veh_dic[keys]={str(veh_id):v_name}
                for k,v in veh_dic.items():
                    comm_dic[k].update(veh_dic[k])
        #data=json.dumps(comm_dic,indent=2 ,encoding='utf-8', ensure_ascii=False)
        return comm_dic

    def json_plus(self,a,b):
        for k,v in a.items():
            b[k].update(a[k])    #将a添加到b中
        data = json.dumps(b,indent=2 ,encoding='utf-8', ensure_ascii=False)

        return data






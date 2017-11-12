# -*- coding: utf-8
import MySQLdb
import self as self

from config import *

class ConnectDB(object):
	def __init__(self):
		self.db=MySQLdb.connect(DB_HOST,DB_USER,PASSWORD,DB_NAME,charset="utf8")   #连接数据库
		self.cursor = self.db.cursor()
	def insert(self,table_name	="", 
                    spaceid		="",
                    brand		="",
                    series		="",
                    models		="",
                    guide_price	="",
                    level		="",
                    emission_standard="",
                    structure	="",
                    status		="" ,
                    manufacturer="",
                    year		="",
                    index		="",
                    json_text	="",
                    URL_ 		=""
					):
		sql='''insert into %s set 
                    spaceid		=\'%s\',
                    brand		=\'%s\',
                    series		=\'%s\',
                    models		=\'%s\',
                    guide_price	=\'%s\',
                    level		=\'%s\',
                    emission_standard=\'%s\',
                    structure	=\'%s\',
                    status		=\'%s\',
                    manufacturer=\'%s\',
                    year		=\'%s\',
                    font_letter	=\'%s\',
                    json_text	=\'%s\',
                    url 		=\'%s\'

								''' % (table_name,
									spaceid,
									brand,
									series,
									models,
									guide_price,
									level,
									emission_standard,
									structure,
									status,
									manufacturer,
									year,
									index,
									json_text,
									URL_)
		#print sql
		#try:
		self.cursor.execute(sql)
		self.db.commit()
		#except:
		#	self.db.rollback()
	def select(self,table_name="",field="",value=""):
		sql=''' select %s from %s where %s = \'%s\' ''' % (field,table_name,field,value)
		result=self.cursor.execute(sql)
		return result


	def insertTyre(self,table_name="",
				    spaceid="",
                    brand="",
                    series="",
                    carType="",
					peopleNum="",
					marketTime="",
					engine ="",
					displacement="",
				    first_latter=""
					):
		sql='''insert into %s set
		            vechiclesID=\'%s\',
                    brand=\'%s\',
                    series=\'%s\',
                    carType=\'%s\',
					peopleNum=\'%s\',
					marketTime=\'%s\',
					engine=\'%s\',
					displacement=\'%s\',
					first_latter=\'%s\'
								''' % (table_name,
									spaceid,
									brand,
									series,
									carType,
									peopleNum,
									marketTime,
									engine,
									displacement,
									first_latter)
		#print sql
		#try:
		self.cursor.execute(sql)
		self.db.commit()

	def insertTyre2(self,table_name="",
				    spaceid="",
                    brand="",
                    series="",
                    carType="",
					peopleNum="",
					marketTime="",
					engine ="",
					displacement="",
				    first_latter="",
					model=""
					):
		sql='''insert into %s set
		            vechiclesID=\'%s\',
                    brand=\'%s\',
                    series=\'%s\',
                    carType=\'%s\',
					peopleNum=\'%s\',
					marketTime=\'%s\',
					engine=\'%s\',
					displacement=\'%s\',
					first_latter=\'%s\',
					model=\'%s\'
								''' % (table_name,
									spaceid,
									brand,
									series,
									carType,
									peopleNum,
									marketTime,
									engine,
									displacement,
									first_latter,
									   model)
		#print sql
		#try:
		self.cursor.execute(sql)
		self.db.commit()


	def dbclose(self):
		self.db.close()
#db=ConnectDB()
##db.insert(table_name="json",spaceid=spaceid,json_data=json_data)
#n=db.select(table_name="spider_json",field="series",value=u"凯尊")
#db.dbclose()
		






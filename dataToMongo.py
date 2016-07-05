# -*- coding: utf-8 -*-
"""
Created on Tue Jul 05 17:29:13 2016

@author: pac
data to mongo
"""


'''#通用数据插入操作'''
def mongoConfig(coll,df):
    from pymongo import * 
    uri = "mongodb://name:password@ip/?authSource=database"
    Client= MongoClient(uri)
    db = Client.dm
    collection=db[coll]
    collection.insert_many(df.to_dict('records'))
    Client.close() #是否关闭链接



import time
import pandas  as pd
from credit import  getcreditInfo
dt_name= pd.read_csv('lyu.csv') #供应商与客户数据（lyu.csv,ylong.csv）
cust_id=dt_name.partner_id.tolist()
custvalues=dt_name.partner_name.tolist()
doneValue = []
#List=[]
#Data=[]


j=0
for  i in range(j,len(custvalues)):

	'''读取并保存记录'''
    print custvalues[i]
    if custvalues[i] not in doneValue:
      try:
          temp = getcreditInfo(custvalues[i])
          doneValue.append(custvalues[i])
          print temp       
      except:
           
           with open('D:\Users\pac\Documents\Python Scripts\modle\spider\datalog.txt','r+') as f:
               f.write(str(i))
               
           print 'i am sleepy now is:',time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
           time.sleep(600)
           j=i
           temp=[]
#      Data.append(temp)
#      List.append(i)
      time.sleep(5)
           
           
      '''写入四类记录'''
      if temp!=[]:          
          for item in temp:
              try :
                  tmp=item.getbase()
              except:
                  print 'baseinfo is not existed'
                  tmp=[]
              if tmp !=[]:                  
                  dfb=pd.DataFrame(pd.Series(tmp)).T
                  dfb[u'客户代码']=cust_id[i]
                  mongoConfig('infozg_base1',dfb) # infozg_base 基础信息
                  print dfb[u'工商注册号'], dfb[u'审核日期']
              if item.getbad()is not None:
                  for Dict1 in item.getbad(): 
                      df1=pd.DataFrame(pd.Series(Dict1)).T
                      df1[u'客户代码']=cust_id[i]
                      mongoConfig('infozg_badrd1',df1) # infozg_bad  不良记录
              if item.getgood()is not None:
                  for Dict2 in item.getgood(): 
                      df2=pd.DataFrame(pd.Series(Dict2)).T
                      df2[u'客户代码']=cust_id[i]
                      mongoConfig('infozg_goodrd1',df2)    # infozg_good     优良记录
              if item.getlost()is not None:
                  for Dict3 in item.getlost(): 
                      df3=pd.DataFrame(pd.Series(Dict3)).T
                      df3[u'客户代码']=cust_id[i]  
                      mongoConfig('infozg_lostrd1',df3)   # infozg_lost   失信记录
                      
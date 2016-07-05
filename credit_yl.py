
# coding: utf-8

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 16:39:22 2015
credit_info 类获取结果的基础信息、良好记录、失信记录、不良记录
getcreditInfo 传入name，返回所有结果
@author: lywen
"""
from readHtml import ReadHtml,ReadHtmlbase
import time
import urllib
import pandas as pd

def searchName(name='长虹电器股份有限公司',headers=None):
    """
    按输入查找公司的信用信息
    """
    
    now = int(time.time()*1000L)##获取当前时间的时间戳，获取时间的前13位##
    url = """http://www.creditchina.gov.cn/credit_info_search?t=%d"""%now
    
    data={
        'keyword':'%s'%name,
    'searchtype':'0',
    'objectType':'2',
    'areas':'',
    'creditType':'',
    'dataType':'1',
    'areaCode':'',
    'templateId':'',
    'exact':'0',
    'page':'1'
    }
    data = urllib.urlencode(data)
    http = ReadHtml(url,headers=headers,data=data,post=True)
    ###获取下一级链接的随机码
    return http

def nextDetail(http,headers):
    """
    获取搜索结果所有的数据数据
    """
    url="""http://www.creditchina.gov.cn/credit_info_detail?"""
    temp=[]
    for req in eval(http.getHtml().replace('null','None'))['result']['results']:
        data={'objectType':2,
             'encryStr':'%s'%(req['encryStr'].replace('\n',''))}
        data=urllib.urlencode(data)
        childhttp = ReadHtmlbase(url+data)
        temp.append(childhttp)
    return temp

    
def getcreditInfo(name):
    """
    获取搜索的所有信息
    
    """
    headers = {
            'Accept':'text/plain, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection':'keep-alive',
        'Content-Length':'191',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'Hm_lvt_0076fef7e919d8d7b24383dc8f1c852a=1467272309,1467273243,1467277124,1467595261; Hm_lpvt_0076fef7e919d8d7b24383dc8f1c852a=1467598746',
        'Host':'www.creditchina.gov.cn',
        'Origin':'http://www.creditchina.gov.cn',
        'Referer':'http://www.creditchina.gov.cn/search_all',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
        }
    html = searchName(name,headers=headers)
    nextHtml = nextDetail(html,headers)
    temp=[]
    for r  in nextHtml:
        credit = credit_info(r.getbs4Html())
        temp.append(credit)
    return temp
    
    
class credit_info(object):
    """
    获取纪录的基本信息，良好纪录，不良记录、失信记录
    """
    def __init__(self,html):
        div = html.findAll('div',attrs={'class','creditsearch-tagsinfo'})
        self.base = div[0]
        self.good = div[1]
        self.bad = div[2]
        self.lost = div[3]
    def getbase(self):
        """
        获取基础信息
        返回字典的形式
        企业名称：江苏奥宇建设工程有限公司
        归属地域：江苏
        法人：
        组织机构代码：
        工商注册号：320322000074937
        注册资金：6518.000000 万(元)
        住所：沛县东风路174号
        成立日期：2012-02-20
        营业期限： 2012-02-20 至 无固定期限
        经营范围：房屋工程建筑，铁路、道路、隧道和桥梁工程建筑，水利和港口工程建筑，工矿工程建筑，市政工程施工，土石方工程施工，拆除工程施工，提供施工设备服务，城市绿化管理，景观和绿地设施工程施工，建筑装饰，起重设备安装，城市绿化管理，建材销售，管道工程建筑，管道和设备安装，建筑钢结构工程安装，消防设施工程施工，火灾报警系统工程施工。(依法须经批准的项目，经相关部门批准后方可开展经营活动);;
        审核日期：2014-09-02
        """
        base = self.base
        return reduce(lambda y,z:dict(y,**z),map(lambda x:{x.text.replace(' ','').split(u'：')[0]:x.text.replace(' ','').split(u'：')[1]},base.findAll('li')))

    def getlost(self):
        """
        获取公司的失信记录
        返回列表形式的字典
        """

        lost = self.lost.findAll('ul',attrs={'class':"creditsearch-tagsinfo-ul clearfix"})
        if lost ==[]:
            return None
        else:

            return map(lambda m:
            reduce(lambda y,z:dict(y,**z),map(lambda x:{x.text.replace(' ','').replace('\n','').replace('\r','').split(u'：')[0]:x.text.replace(' ','').replace('\n','').replace('\r','').split(u'：')[1]},m.findAll('li'))),lost)

    def getgood(self):
        """
        获取公司的优良记录
        """
        good = self.good.findAll('ul',attrs={'class':"creditsearch-tagsinfo-ul clearfix"})
        if good ==[]:
            return None
        else:

            return map(lambda m:
            reduce(lambda y,z:dict(y,**z),map(lambda x:{x.text.replace(' ','').replace('\n','').replace('\r','').split(u'：')[0]:x.text.replace(' ','').replace('\n','').replace('\r','').split(u'：')[1]},m.findAll('li'))),good)
    
    def getbad(self):
        """
        获取公司的不良记录
        """
        bad = self.bad.findAll('ul',attrs={'class':"creditsearch-tagsinfo-ul"})
        if bad ==[]:
            return None
        else:
            return map(lambda m:
            reduce(lambda y,z:dict(y,**z),map(lambda x:{x.text.replace(' ','').replace('\n','').replace('\r','').split(u'：')[0]:x.text.replace(' ','').replace('\n','').replace('\r','').split(u'：')[1]},m.findAll('li'))),bad)
    
            
        
if __name__=='__main__':
    """data 是一个列表，如果有多条记录
    da = data[0]
    da.getbase() 获取记录的基础信息
    da.getlost() 获取记录的失信记录
    da.getbad() 获取记录的不良记录
    da.getgood() 获取记录的优良记录
    
    """
    
    data = getcreditInfo('长虹电器股份有限公司')
    

# coding: utf-8

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 16:39:22 2015

@author: lywen
"""
import urllib2
import urllib
from bs4 import BeautifulSoup
import json
import time
import traceback
import requests

class ReadHtml(object):
    """
    给定网页，返回网页源代码
    """
    def __init__(self,url, headers=None, data=None,timeout=5,post=False):
       
       
        try:
                
                self.req = requests.Session().post(url, data=data, headers=headers)
                    
                
                self.__html = self.req.text
                
                
        except Exception:
               traceback.print_exc()
               self.__html =None
                    
               
                
                
    def getHtml(self):
        """
        返回网页源代码
        """
        return self.__html
    
    def htmlToJson(self):
        """
        将网页joson转换为python字典
        """
        
        try:
            if self.__html is None:
                return None
            return json.loads(self.__html)
        except:
            return None
            
    def getbs4Html(self):

        if self.__html is None:
            return None
        return BeautifulSoup(self.__html)
            
        
        
class ReadHtmlbase(object):
    """
    给定网页，返回网页源代码
    """
    def __init__(self,url, headers=None, data=None,timeout=5,post=False):
       
       
        try:
                if headers is None:
                    req = urllib2.Request(url)
                    html = urllib2.urlopen(req, timeout=timeout)
                else:
                    if post:
                       req = requests.Session().post(url, data=data, headers=headers)
                    
                       html = req.text
                    else:
                        req = urllib2.Request(url,data=data,headers=headers)
                        html = urllib2.urlopen(req, timeout=timeout).read()
                
                self.__html = html
                
                
        except Exception:
               traceback.print_exc()
               self.__html =None
                    
               
                
                
    def getHtml(self):
        """
        返回网页源代码
        """
        return self.__html
    
    def htmlToJson(self):
        """
        将网页joson转换为python字典
        """
        
        try:
            if self.__html is None:
                return None
            return json.loads(self.__html)
        except:
            return None
            
    def getbs4Html(self):

        if self.__html is None:
            return None
        return BeautifulSoup(self.__html)
            
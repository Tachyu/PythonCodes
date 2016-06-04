#-*-coding:utf8-*-
 
import re
import string
import sys
import os
import urllib
import urllib2
import random
import time
from bs4 import BeautifulSoup
import requests
from lxml import etree
 
reload(sys) 
sys.setdefaultencoding('utf-8')
#0:17801066722
#1:icbmdf5@hotmail.com
#2:baidu_knight@sina.cn
cookies = [{"Cookie":r'_T_WM=409cf28f1fe73f170d19e9ae26460612; SUB=_2A256Lpz1DeRxGeNN6VsR8S7FzTmIHXVZ0CS9rDV6PUJbrdBeLRD1kW1LHeuRqpxAUsTxediZ1NVDW4nkzcpmlA..; SUHB=0pHxFemzYWcNOp; SSOLoginState=1462430885'},
           {"Cookie":r'_T_WM=1df41c6b3494f09cfd91641515c2094c; SUB=_2A256Lpw_DeTxGeNL6VMX-CrIzjSIHXVZ0CR3rDV6PUJbrdBeLUj5kW1LHetBxPAhCBrH5ep_vXoEXeMRKAecYg..; SUHB=0qjkXYcG22ZcoR; SSOLoginState=1462430831'}
          ,{"Cookie":r"_T_WM=bd2b3b424ba5ac4fe73c3c57746dced9; SUB=_2A256LpxYDeTxGeNH6lsV8y_IzDiIHXVZ0CQQrDV6PUJbrdBeLVbtkW1LHes57d4eFnUY7ntB0B1179LvyL3sAQ..; SUHB=0cS3cFZ0Wk3iC2; SSOLoginState=1462430728"}]

headers = [{'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}]

# proxies = [{"http": "http://49.119.168.132:80"},
          # {"http": "http://58.40.82.214:8118"},
          # {"http": "http://106.38.251.62:8088"}]
proxies = [
	{'http':'31.168.236.236:8080'},#以色列
	{'http':'43.226.162.107:80'},#日本
	{'http':'43.226.162.107:8000'},#日本
	{'http':'43.226.162.107:8080'},#日本
	{'http':'58.40.82.214:8118'},#上海市南汇区 电信ADSL
	{'http':'58.247.30.222:8080'},#上海市 联通
	{'http':'61.174.13.12:443'},#浙江省金华市 电信
	{'http':'61.235.125.26:81'},#广东省 铁通(全省通用)
	{'http':'62.117.96.138:3128'},#俄罗斯
	{'http':'82.102.162.162:80'},#以色列
	{'http':'82.102.162.163:80'},#以色列
	{'http':'84.23.107.195:8080'},#沙特阿拉伯
	{'http':'85.143.164.100:81'},#俄罗斯
	{'http':'106.38.251.62:8088'},#北京市 北京电信互联网数据中心
	{'http':'106.75.128.89:80'},#山东省济南市 天地网联科技有限公司
	{'http':'106.75.128.90:80'},#山东省济南市 天地网联科技有限公司
	{'http':'106.184.7.132:8088'},#日本 东京都千代田区KDDI通信公司
	{'http':'110.81.238.173:8088'},#福建省泉州市安溪县 电信
	{'http':'112.64.185.73:80'},#上海市 联通漕河泾IDC机房
	{'http':'112.65.88.220:8080'},#上海市 联通漕河泾IDC机房
	{'http':'115.160.156.91:80'},#香港 九仓电讯有限公司
	{'http':'117.135.251.131:80'},#贵州省 移动
	{'http':'117.135.251.134:80'},#贵州省 移动
	{'http':'117.135.251.135:80'},#贵州省 移动
	{'http':'117.135.251.136:80'},#贵州省 移动
	{'http':'117.177.250.151:80'},#四川省 移动
	{'http':'117.177.250.151:82'},#四川省 移动
	{'http':'117.177.250.151:8080'},#四川省 移动
	{'http':'117.177.250.152:80'},#四川省 移动
	{'http':'117.177.250.152:8080'},#四川省 移动
	{'http':'119.253.32.5:8080'},#北京市 联通
	{'http':'120.52.73.96:8080'},#中国 长城宽带
	{'http':'121.22.252.241:80'},#河北省秦皇岛市 联通
	{'http':'121.69.42.90:8118'},#北京市 成都鹏博士电信传媒集团股份有限公司旗下北京宽带通电信技术有限公司
	{'http':'121.69.45.162:8118'},#北京市 成都鹏博士电信传媒集团股份有限公司旗下北京宽带通电信技术有限公司
	{'http':'124.202.181.186:8118'},#北京市 电信通
	{'http':'124.202.214.26:8118'},#北京市 电信通
	{'http':'125.46.57.28:80'},#河南省郑州市 联通
	{'http':'146.184.0.116:80'},#美国
	{'http':'146.184.0.116:8080'},#美国
	{'http':'175.25.25.134:8118'},#北京市朝阳区 北京数据家科技有限公司(北苑路170号凯旋城C座26层)
	{'http':'180.76.135.145:3128'},#北京市 北京百度网讯科技有限公司
	{'http':'183.61.236.53:3128'},#广东省广州市 电信
	{'http':'183.129.134.226:8080'},#浙江省杭州市 电信
	{'http':'183.207.228.122:80'},#江苏省南京市 江苏移动自建代理服务器
	{'http':'183.239.167.122:8080'},#广东省 移动
	{'http':'183.252.18.131:8080'},#中国 移动
	{'http':'185.7.3.244:8080'},#土耳其
	{'http':'187.177.14.104:8080'},#墨西哥
	{'http':'202.99.29.102:80'},#北京市 联通ADSL
	{'http':'203.195.204.168:8080'},#广东省深圳市 腾讯公司
	{'http':'210.212.15.124:8080'},#印度
	{'http':'211.87.147.138:8888'},#山东省青岛市 青岛科技大学
	{'http':'213.136.79.124:80'},#德国
	{'http':'216.218.147.196:1080'},#美国 加利福尼亚州弗里蒙特市Hurricane Electric公司
	{'http':'218.3.177.19:8089'},#江苏省徐州市 电信
	{'http':'218.18.101.241:3128'},#广东省深圳市福田区 电信
	{'http':'218.26.120.170:8080'},#山西省太原市 联通
	{'http':'220.170.182.5:80'},#湖南省株洲市 电信
	{'http':'221.223.234.42:8118'},#北京市海淀区 联通
	{'http':'222.173.221.46:8118'},#山东省烟台市 电信
	{'http':'222.176.112.10:80'}#重庆市 电信
]
user_id = ''
word_Count = 0
def main():
  global cookies
  global headers
  global proxies
  global user_id
  global word_Count
  pageNum = 10
  
  if(len(sys.argv)==2):
    user_id = sys.argv[1]
  else:
    user_id = (raw_input(u"user_id: "))
  pageCount = 1
  result = "" 
  print u'爬取微博：%s 中....'%user_id
  try:
    for page in range(1,pageNum+1):
      ranSer = random.randint(0,len(proxies)-1)
      ranHea = random.randint(0,len(headers)-1)
      ranCoo = random.randint(0,len(cookies)-1)
      # ranCoo = 2
      print '----------------------'
      print 'Cookie: ' + str(ranCoo)
      # print 'Header: ' + headers[ranHea].values()[0]
      print 'Proxy:  ' + proxies[ranSer].values()[0]
     
      # 获取lxml页面
      # url = 'https://weibo.cn/u/%s?filter=1&page=%d'%(user_id,page) 
      url = 'https://weibo.cn/%s?filter=1&page=%d'%(user_id,page) 
      
      print 'url: ' + url
      lxml = requests.get(url, cookies = cookies[ranCoo], timeout=13,headers= headers[ranHea],proxies = proxies[ranSer]).content
      # 文字爬取
      selector = etree.HTML(lxml)
      content = selector.xpath('//span[@class="ctt"]')
     
      # 该页无内容时停止爬取
      if len(content) == 0:
          print u'爬取结束'
          break
      else:
        print u'\n第 %d 页'%pageCount
        print u'本页 %d 条'%len(content)
        result += getPageContent(content)
        print u'累计 %d 条'%word_Count
        pageCount += 1
        sleeptime = random.randint(0,2)
        print u'等待: %d 秒...'%sleeptime
        time.sleep(sleeptime)
  except Exception, e:
    print u'爬取发生意外!'
    print e
  finally:
    saveWeibo(result)

def getHotwords():
  global cookies
  global headers
  global proxies
  ran = random.randint(0,len(headers)-1)
  print ran
  url_hot = 'http://m.weibo.cn/p/index/?containerid=106003type%3D25%26filter_type%3Dfilms'	
  html = requests.get(url_hot, cookies = cookies[3], timeout=20,headers= headers[ran]).content
  print html
  bs = BeautifulSoup((html).decode('gbk'),'lxml')#3 and 1
  hotwds = bs.find(class_ = 'mct-a')
  file = open('hwds.txt','w+')
  print len(hotwds)
  for word in hotwds:
    file.write(str(word))
  print hotwds
     
def getPageContent(content):
  global word_Count
  result = ''
  for each in content:
    text = each.xpath('string(.)')
    text = text+"\n"
    result = result + text
    word_Count += 1
  return result

def saveWeibo(result):
  global user_id
  word_path = r'weiboData/%s'%user_id
  word_path += r'.txt'
  fo = open("%s"%word_path, "w")
  fo.write(result)
  print u'Done! FileName: %s'%word_path


main()
# getHotwords()
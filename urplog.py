#encoding:utf-8
import re
import string
import sys
import os
import io
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup 
import requests
import getpass
from lxml import etree
from pytesser import *
import lxml.html.soupparser as soupparser

reload(sys)
sys.setdefaultencoding('utf-8')

#登陆页面
loginpage = "http://121.194.57.131/"
targetpage = "http://121.194.57.131/loginAction.do"
my_class_url = 'http://121.194.57.131/xskbAction.do?actionType=1'				#1
my_grade_url = r'http://121.194.57.131/gradeLnAllAction.do?type=ln&oper=qb'		#2
my_info_url = 'http://121.194.57.131/xjInfoAction.do?oper=xjxx'					#3
ava_classroom_url = 'http://121.194.57.131/oneDayJasAction.do?oper=tjcx'		#4



def getPageCon(url):
	con = urllib2.urlopen(url)
	html = con.read()
	return html

	
if len(sys.argv) != 4:
	print 'choice list:'
	print '1: class_info'
	print '2: grade_info'
	print '3: personal_info'
	print '4: avalabel classroom\n'
	student_id = raw_input("ID: ")
	passWord = getpass.getpass("password: ")
	choice = int(raw_input("choice: "))
else:
	student_id = sys.argv[1]
	passWord = sys.argv[2]
	choice = int(sys.argv[3])
	
#MozillaCookieJar
cookiejar = cookielib.MozillaCookieJar()

# 将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
cookieSupport= urllib2.HTTPCookieProcessor(cookiejar)

httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)

#创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的
opener = urllib2.build_opener(cookieSupport, httpsHandler)

#将包含了cookie、http处理器、http的handler的资源和urllib2对象绑定在一起，安装opener,此后调用urlopen()时都会使用安装过的opener对象，
urllib2.install_opener(opener)

#验证码
v_yzm = ''

vrifycodeUrl = "http://121.194.57.131/validateCodeAction.do?"
#提取验证码text
while True:
    file = urllib2.urlopen(vrifycodeUrl)
    pic= file.read()
    picName = u'urf_login_temp.jpg'
    localpic = open(picName,"wb")
    localpic.write(pic)
    localpic.close()
    im = Image.open(picName)
    v_yzm =image_to_string(im)
    pattern = re.compile('\W')
    v_yzm = re.sub(pattern,'',v_yzm)
    print v_yzm
    print len(v_yzm)
    if len(v_yzm) == 4:
         break
    else:
        pass 

cookies = ''

for index, cookie in enumerate(cookiejar):
		cookies = cookies+cookie.name+'='+cookie.value+';';
		
cookie = cookies[:-1]
print "cookies:",cookie
 
 
#请求数据包
postData = {
	'zjh1':'',
	'tips':'',
	'lx':'',
	'evalue':'',
	'eflag':'',
	'fs':'',
	'dzslh':'',
	'zjh':student_id,
	'mm':passWord,
	'v_yzm':v_yzm,
	'':'',
	'':''
}	
# cookie = 'OUTFOX_SEARCH_USER_ID_NCOO=2050625549.045103; JSESSIONID=abcBLnvfCKWsxb8OAH1rv'
 
#post请求头部
headers = {
    'Cookie':cookie,
    'Host':'121.194.57.131',
	'Origin':'http://121.194.57.131',
	'Referer':'http://121.194.57.131/',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
	}
 
#合成post数据 
data = urllib.urlencode(postData)  
print  'data:',data

#创建request

#构造request请求
request = urllib2.Request(targetpage,data,headers)
try:
	#访问页面
	url_dic = {1:my_class_url,
               2:my_grade_url,
			   3:my_info_url,
			   4:ava_classroom_url}
			   
	html = getPageCon(url_dic[choice])
	
	file = open('urptest.html','w')
	file.write(html)
	file.close()
	print html
	
	# status = response.getcode()
	# print status
except  urllib2.HTTPError, e:
	 print e.code
	

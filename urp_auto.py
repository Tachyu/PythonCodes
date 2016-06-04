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
import pytesser
from lxml import etree
from pytesser import *
import lxml.html.soupparser as soupparser
import splinter
import time
from splinter import browser

reload(sys)
sys.setdefaultencoding('utf-8')

#登陆页面
loginpage = r"http://121.194.57.131/"
targetpage = r"http://121.194.57.131/loginAction.do"							#0
my_class_url = r'http://121.194.57.131/xskbAction.do?actionType=1'				#1
my_grade_url = r'http://121.194.57.131/gradeLnAllAction.do?type=ln&oper=qb'		#2
my_info_url = r'http://121.194.57.131/xjInfoAction.do?oper=xjxx'				#3
ava_classroom_url = r'http://121.194.57.131/oneDayJasAction.do?oper=tjcx'		#4
cho_class_url = r'http://121.194.57.131/xkMainAction.do?actionType=6'			#5

if len(sys.argv) == 1:
	print 'choice list:'
	print '1: class_info'
	print '2: grade_info'
	print '3: personal_info'
	print '4: avalabel classroom\n'
	print '5: choose class\n'
	student_id = raw_input("ID: ")
	passWord = getpass.getpass("password: ")
	choice = int(raw_input("choice: "))
elif len(sys.argv) == 2:
	student_id = '14281023'
	passWord = 'zmy10086'
	choice = int(sys.argv[1])
elif len(sys.argv) == 4:
	student_id = sys.argv[1]
	passWord = sys.argv[2]
	choice = int(sys.argv[3])



browser = splinter.Browser()
browser.visit(targetpage)
# time.sleep(2)
browser.fill('zjh',student_id)
browser.fill('mm',passWord)
#验证码
v_yzm = ''

vrifycodeUrl = "http://121.194.57.131/validateCodeAction.do?"
#提取验证码text
while True:
	file = urllib2.urlopen(vrifycodeUrl)
	pic = file.read()
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
        
browser.fill('mm',passWord)
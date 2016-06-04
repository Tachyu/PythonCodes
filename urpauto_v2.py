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
import random
import selenium
import shutil
from selenium import webdriver
from splinter import browser
import Image,ImageFilter

reload(sys)
sys.setdefaultencoding('utf-8')

#登陆页面
loginpage = r"http://121.194.57.131/"
jw_log_url = r"http://jwc.bjtu.edu.cn/login_introduce_s.html"
jump_url = 'http://jwc.bjtu.edu.cn:82/NoMasterJumpPage.aspx?URL=JWCApp&FPC=page:JwcApp'
welcome_url = r'http://jwc.bjtu.edu.cn:82/Welcome.aspx'

# 0.登陆
# 1.课程表
# 2.成绩
# 3.个人信息
# 4.可用教室
# 5.选课
# 6.评教
targetpage = r"http://121.194.57.131/loginAction.do"							#0
my_class_url = r'http://121.194.57.131/xskbAction.do?actionType=1'				#1
my_grade_url = r'http://121.194.57.131/gradeLnAllAction.do?type=ln&oper=qb'		#2
my_info_url = r'http://121.194.57.131/xjInfoAction.do?oper=xjxx'				#3
ava_classroom_url = r'http://121.194.57.131/oneDayJasAction.do?oper=tjcx'		#4
cho_class_url = r'http://121.194.57.131/xkMainAction.do?actionType=6'			#5
list_wj_url = r'http://121.194.57.131/jxpgXsAction.do?oper=listWj'				#6
cho_bxk_url = r'http://121.194.57.131/zytzAction.do?oper=bxqkc'					#7

start = time.clock()
browser = splinter.Browser()
browser.visit(jw_log_url)

if len(sys.argv) == 1:
	print u'''
	# 0.登陆\n
	# 1.课程表\n
	# 2.成绩\n
	# 3.个人信息\n
	# 4.可用教室\n
	# 5.选课\n
	# 6.评教\n
	'''
	student_id = raw_input("ID: ")
	passWord = getpass.getpass(r"password(jwc.bjtu): ")
	choice = int(raw_input("choice: "))
elif len(sys.argv) == 2:
	student_id = '14281023'
	passWord = '680016'
	choice = int(sys.argv[1])
elif len(sys.argv) == 4:
	student_id = sys.argv[1]
	passWord = sys.argv[2]
	choice = int(sys.argv[3])
browser.fill('TextBoxUserName',student_id)
browser.fill('TextBoxPassword',passWord)
browser.find_by_id('ButtonLogin').first.click()
# browser.visit(welcome_url)
browser.visit(jump_url)
time.sleep(1.0)
url_dic = {
               0:targetpage,
	           1:my_class_url,
			   2:my_grade_url,
			   3:my_info_url,
			   4:ava_classroom_url,
			   5:cho_class_url,
			   6:list_wj_url}	

#自动评教		
def autoRate():
	global browser
	list = browser.find_by_tag('img')[:]
	for i in range(len(list)):
		print i
		#若已评价则跳过
		try:
			item = browser.find_by_tag('img')[i].click()
			checks = browser.find_by_value('10_1')
			if len(checks) == 0:
				browser.back()
				print 'is rated, back!'
				continue
			for check in checks:
				check.click()
			#评价
			words = u'老师人很好！'
			browser.find_by_tag('textarea').first.fill(words)
			submit = browser.find_by_tag('img')[0]
			submit.click()
			time.sleep(0.2)
			browser.get_alert().accept
		except:
			pass
		

# 自动选课
def autoSel(classID):
	global browser
	list = browser.find_by_id(classID)[0]
	option_num = len(list.find_by_tag('option')) - 1
	
	for index in range(option_num):	
		list.find_by_tag('option')[index + 1].click()
		nextID = classID + '_ktzy' + str(index + 2)
		if index != option_num - 1:
			list = browser.find_by_id(nextID)[0]		
	submit = browser.find_by_tag('img')[0]
	submit.click()
		
	
				   
browser.visit(cho_bxk_url)
time.sleep(0.5)
# print browser.find_by_text('汇编与接口技术').first.click()
autoSel('80L132Q')
# autoRate()
# 80L132Q_ktzy4
	
# end = time.clock()
# print str(end - start) + ' 	s'
time.sleep(1.5)
# print browser.find_by_text('张铭宇')

# browser.find_by_text('选课管理').first.click()
# time.sleep(10)
# browser.quit()
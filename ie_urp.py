#encoding:utf-8
import re
import string
import sys
import os
import io
import urllib
import urllib2
import cookielib
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
from splinter import driver

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

iedriver = "E:\Python Sourse File\IEDriverServer.exe"
os.environ["webdriver.ie.driver"] = iedriver
driver = webdriver.Ie(iedriver)
driver.get(jw_log_url)
	
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

driver.find_element_by_id('TextBoxUserName').send_keys(student_id)
driver.find_element_by_id('TextBoxPassword').send_keys(passWord)
driver.find_element_by_id('ButtonLogin').click()
driver.get(jump_url)
time.sleep(1.0)
url_dic = {
			   0:targetpage,
			   1:my_class_url,
			   2:my_grade_url,
			   3:my_info_url,
			   4:ava_classroom_url,
			   5:cho_class_url,
			   6:list_wj_url}	
			   
def getCode(rand_code):
	global error_image
	global error_time
	#验证码
	v_yzm = ''
	#列出目录下的文件,获取截图文件
	files = os.listdir('temp')
	picName = u'temp/'
	for f in files:
		if f.find('urp_'+ str(ran_code)) != -1:
			picName += f.decode('gbk')
			break
	im = Image.open(picName)
	#裁切图片
	region = (318,288,398,308)
	cropImg = im.crop(region)
	bg = Image.new("RGB", cropImg.size, (255,255,255))
	bg.paste(cropImg,cropImg)
	bg = bg.convert('L')	
	#阈值化
	threshold = 150
	table = []
	for i in range(256):
		if i < threshold:
			table.append(0)
		else:
			table.append(1)
	bg = bg.point(table, '1')
	bg.show()
	v_yzm =image_to_string(bg)
	# print 'raw:' + v_yzm
	v_yzm = v_yzm.replace('NN','W')
	v_yzm = v_yzm.replace('?','f')
	v_yzm = v_yzm.replace('|','l')
	v_yzm = v_yzm.replace('_','')
	pattern = re.compile('\W')
	v_yzm = re.sub(pattern,'',v_yzm)
	
	if len(v_yzm) == 4:
		return v_yzm
	else:
		bg.save(r'errorReport/' +v_yzm + r'_s1.jpg')
		return ''
			
try_time = 0
driver.get(url_dic[choice])
driver.switch_to_alert().dismiss()

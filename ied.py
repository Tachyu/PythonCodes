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
from splinter import browser

reload(sys)
sys.setdefaultencoding('utf-8')

#登陆页面
loginpage = r"http://121.194.57.131/"
vrifycodeUrl = "http://121.194.57.131/validateCodeAction.do?"

# 0.登陆
# 1.课程表
# 2.成绩
# 3.个人信息
# 4.可用教室
# 5.选课
# 6.评教

targetpage = r'//*[@id="moduleTab"]/tbody/tr/td[1]/a'                        #0
my_class_xp = r'本学期课表'              #1
my_grade_xp = r'//*[@id="divCoHome"]/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table[2]/tbody/tr/td/a'     #2
my_info_xp = r'http://121.194.57.131/xjInfoAction.do?oper=xjxx'                #3
ava_classroom_xp = r'//*[@id="divCoHome"]/table/tbody/tr/td[1]/table/tbody/tr[7]/td/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table[2]/tbody/tr/td/a'       #4
cho_class_xp = r'//*[@id="moduleTab"]/tbody/tr/td[3]/a'           #5
list_wj_xp = r'//*[@id="divCoHome"]/table/tbody/tr/td[1]/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/a'              #6

iedriver = "E:\Python Sourse File\IEDriverServer.exe"
os.environ["webdriver.ie.driver"] = iedriver
driver = webdriver.Ie(iedriver)
    
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

#创建临时目录
try:
    os.mkdir('temp')
except:
    pass
    
#识别错误的验证码图片
error_image = Image.new("RGB", [100,100], (255,255,255))

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
    

while True and try_time < 10:
    driver.get(loginpage)
    driver.find_element_by_name('zjh').send_keys("14281023")
    driver.find_element_by_name('mm').send_keys('zmy10086')
    v_yzm = ''
    yzm_trytime = 0
    
    while len(v_yzm) != 4 and yzm_trytime < 5:
        if yzm_trytime != 0:
            driver.find_element_by_tag_name('a').click()
            time.sleep(0.1)
        ran_code = random.random()
        driver.save_screenshot('E:\\Python Sourse File\\temp\\urp_' + str(ran_code) + '.jpg')
        v_yzm = getCode(ran_code)
        yzm_trytime += 1
          
    driver.find_element_by_xpath('/html/body/table/tbody/tr/td/table[3]/tbody/tr/td[2]/form/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/input').send_keys(v_yzm)
    driver.find_element_by_id('btnSure').click()
    # time.sleep(0.2)
    
    try:
        print v_yzm
        driver.find_element_by_id('btnSure').click()
    except Exception as e:
        print 'Success!'
        break
    error_image.save(r'errorReport/' + v_yzm + r'_s2.jpg')
    try_time += 1

url_dic = {
               0:targetpage,
	           1:my_class_xp,
			   2:my_grade_xp,
			   3:my_info_xp,
			   4:ava_classroom_xp,
			   5:cho_class_xp,
			   6:list_wj_xp}	
# driver.get(url_dic[choice])
# driver.find_element_by_name(url_dic[choice])
time.sleep(1)
my_class_url = r'http://121.194.57.131/xskbAction.do?actionType=1'				#1
list_wj_url  = r'http://121.194.57.131/jxpgXsAction.do?oper=listWj'				#6

driver.get(my_class_url)
driver.switch_to_alert().dismiss()

#删除临时文件
files = os.listdir('temp')
for file in files:
	try:
		targetFile = os.path.join('temp',  file) 
		if os.path.isfile(targetFile):
			os.remove(targetFile)
	except Exception as e:	
		pass
print u'删除成功'
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
from PIL import Image
from PIL import ImageFilter
import winsound

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
targetpage = r"http://121.194.57.131/loginAction.do"                            #0
my_class_url = r'http://121.194.57.131/xskbAction.do?actionType=1'                #1
my_grade_url = r'http://121.194.57.131/gradeLnAllAction.do?type=ln&oper=qb'        #2
my_info_url = r'http://121.194.57.131/xjInfoAction.do?oper=xjxx'                #3
ava_classroom_url = r'http://121.194.57.131/oneDayJasAction.do?oper=tjcx'        #4
cho_class_url = r'http://121.194.57.131/xkMainAction.do?actionType=6'            #5
list_wj_url = r'http://121.194.57.131/jxpgXsAction.do?oper=listWj'                #6
cho_2_url = r'http://121.194.57.131/ctkcAction.do?actionType=1&xkjd=bxbtx'        #7
cho_3_url = r'http://121.194.57.131/bxXxBtxAction.do?actionType=2'
choe_4_url = r'http://121.194.57.131/bxXxBtxAction.do?actionType=3'

iedriver = "E:\IEDriverServer.exe"
os.environ["webdriver.ie.driver"] = iedriver
driver = webdriver.Ie(iedriver)

driver.maximize_window()
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
               6:list_wj_url,
               7:cho_2_url,
               8:cho_3_url
               }    
               
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
    print picName
    im = Image.open(picName)
    #裁切图片
    region = (1160,0,1245,26)
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
    v_yzm = v_yzm.replace('NN','W')
    v_yzm = v_yzm.replace('?','f')
    v_yzm = v_yzm.replace('|','l')
    v_yzm = v_yzm.replace('_','')
    pattern = re.compile('\W')
    v_yzm = re.sub(pattern,'',v_yzm)
    print v_yzm
    if len(v_yzm) == 4:
        return v_yzm
    else:
        return ''
            
try_time = 0
driver.get(url_dic[choice])
try:
    driver.switch_to_alert().dismiss()
except Exception as e:
    pass

        
isFind = False
while True and not isFind:
   time.sleep(1.5)
   driver.get(url_dic[choice])
   checkbox = driver.find_elements_by_tag_name('input')
   for it in checkbox:
     class_id = '80L019Q' + '_01'
     if it.get_attribute('value') == class_id:
        print class_id + ' is avalable!' 
        isFind = True
        #点击选框
        it.click()
        # winsound.PlaySound('C4_explosion_03.wav',winsound.SND_LOOP)
        break
oriLen = len(driver.find_elements_by_tag_name('input'))
yzm_textArea = driver.find_elements_by_tag_name('input')[1]
# for index, it in enumerate(yzm_textArea):
#     print str(index) + ':'
#     print it.get_attribute('name')
# yzm_textArea.send_keys('1234')
# print yzm_textArea.get_attribute('title')
#提交成功
isOK = False
tryTime = 0
# 处理验证码
while not isOK and tryTime < 10:
    driver.get(url_dic[choice])
    checkbox = driver.find_elements_by_tag_name('input')
    for it in checkbox:
        class_id = '80L019Q' + '_01'
        if it.get_attribute('value') == class_id:
            print class_id + ' is avalable!' 
            isFind = True
            #点击选框
            it.click()
    v_yzm = ''
    while len(v_yzm) != 4:
        driver.find_element_by_link_text('换一张').click()
        ran_code = random.random()
        driver.save_screenshot('F:\\Python Sourse File\\temp\\urp_' + str(ran_code))
        v_yzm = getCode(ran_code)
        time.sleep(0.1)
    
    yzm_textArea.send_keys(v_yzm)
    driver.find_elements_by_tag_name('img')[2].click()
    try:
        alert = driver.switch_to_alert()
        alert.accept()
        #检查是否成功选课
        nowLen = len(driver.find_elements_by_tag_name('input'))
        if nowLen != oriLen:
            isOK = True
        else:
            pass
    except Exception as e:
        pass
    tryTime += 1

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


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
from PIL import Image

reload(sys)
sys.setdefaultencoding('utf-8')

def getCode(rand_code):
    #验证码
    v_yzm = ''
    # #列出目录下的文件,获取截图文件
    # files = os.listdir('temp')
    # picName = u'F:/Python Sourse File/temp/'
    # for f in files:
    #     if f.find('urp_'+ str(rand_code)) != -1:
    #         picName += f.decode('gbk')
    #         break
    # print picName
    im = Image.open('F:/Python Sourse File/temp/urp_0.534786638381.jpg')
    #裁切图片
    region = (1160,0,1240,26)
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
    v_yzm = image_to_string(bg)
    # print 'raw:' + v_yzm
    v_yzm = v_yzm.replace('NN','W')
    v_yzm = v_yzm.replace('?','f')
    v_yzm = v_yzm.replace('|','l')
    v_yzm = v_yzm.replace('_','')
    pattern = re.compile('\W')
    v_yzm = re.sub(pattern,'',v_yzm)
    print v_yzm
    # if len(v_yzm) == 4:
    #     return v_yzm
    # else:
    #     return ''
getCode(0.534786638381)
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


iedriver = "E:\Python Sourse File\IEDriverServer.exe"
os.environ["webdriver.ie.driver"] = iedriver
driver = webdriver.Ie(iedriver)

driver.get('https://www.baidu.com/')
driver.find_element_by_link_text('新闻').click()
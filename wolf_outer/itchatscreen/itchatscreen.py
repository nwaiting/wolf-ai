#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
from win32gui import *
titles = set()
def foo(hwnd,mouse):
  #去掉下面这句就所有都输出了，但是我不需要那么多
  if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
    titles.add(GetWindowText(hwnd))

EnumWindows(foo, 0)
lt = [t for t in titles if t]
lt.sort()
for t in lt:
  print t
"""

"""
# -*- coding:utf-8 -*-
import os
import unittest
from selenium import webdriver
class Popup_window(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.url = 'file:///'+os.path.join(os.path.dirname(__file__),'window.html') #测试脚本和待测的html在同一目录下

    def test_Capture (self):
        driver = self.driver
        driver.get(self.url)
        now_handle = driver.current_window_handle #得到当前窗口句柄
        driver.find_element_by_id("baidu").click()
        all_handles = driver.window_handles #获取所有窗口句柄

for handle in all_handles:
    if handle != now_handle:
        driver.switch_to_window(handle)
        driver.find_element_by_id("kw").send_keys('python')
        driver.find_element_by_id("su").click()
        self.driver.implicitly_wait(30)
        driver.switch_to_window(now_handle) #返回window.html

def tearDown(self):
    # self.driver.quit()
    pass

if __name__ == "__main__":
    unittest.main()
"""

# encoding: utf-8
from PIL import Image, ImageGrab
import time
import argparse
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

parser = argparse.ArgumentParser()
parser.add_argument('p', help='Path to Save the Images.')
parser.add_argument('-W', help='Width of the Scraped Images', default=1000)
parser.add_argument('-H', help='Height of the Scraped Images.', default=600)
parser.add_argument('-d', help='Scrape Duration(Minute).', default=1)
parser.add_argument('-t', help='Total Scrape Time(Minute)', default=30)
args = parser.parse_args()
# 图片存放路径、图片尺寸、检测间隔、检测时长
path, width, height, duration, totalTime = args.p, int(args.W), int(args.H), float(args.d), float(args.t)
message = u'屏幕检测到异常截图，请及时查看您的电脑'
fromUser = 'user_to_send_email'
password = 'vaelgxgnybtlbafd' # 开启SMTP/POP3等，获得的校验码为密码，不是登陆密码
toUser = 'user_to_receive_email'
smtp_server = 'smtp.qq.com' # 可以是其他邮件代理服务器
send_once = False # 只发送一次邮件
start_time = int(time.time())

def inTotalTime():
    '''判断检测时间是否到时，上限时间totalTime'''
    now_time = int(time.time())
    elapseTimeByMinutes = (now_time - start_time) / 60.0
    if elapseTimeByMinutes < totalTime:
        return True
    else:
        return False
def _format_addr(s):
    '''调整邮件信息格式'''
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))
def sendMessage(message, fromUser, password, toUser, smtp_server):
    print "send message "
    return
    '''发送邮件'''
    msg = MIMEText(message, 'plain', 'utf-8')
    # 下面三项不标明可能被当作垃圾邮件，导致接收方收不到邮件
    msg['From'] = _format_addr(u'Mac管理员-%s' % fromUser) # 邮件中标明发件人
    msg['To'] = _format_addr(u'家长-%s' % toUser) # 邮件中标明收件人
    msg['Subject'] = Header(u'屏幕监测报告', 'utf-8').encode() # 邮件标题
    server = smtplib.SMTP_SSL(smtp_server, 465)
    # server.set_debuglevel(1) # 发送邮件过程中的详细信息
    server.login(fromUser, password)
    server.sendmail(fromUser, toUser, msg.as_string())
    server.quit()

def handleRudeImage(im):
    '''保存截图并发送邮件通知'''
    filename = str(int(time.time())) + '.jpg'
    im.save(path+filename, 'JPEG')
    global send_once
    if not send_once:
        sendMessage(message, fromUser, password, toUser, smtp_server)
        send_once = True

def screenScrape():
    '''屏幕截取、鉴黄与处置'''
    print " screenScrape =========="
    import os
    print os.getcwd()
    im = ImageGrab.grab().resize((width, height)).convert('YCbCr')
    w, h = im.size

    sx = im.getdata()
    count = 0
    for i, ycbcr in enumerate(sx):
        y, cb, cr = ycbcr
        if 86 <= cb <= 117 and 140 <= cr <= 168:
            count += 1
    print w,h,count
    if count > w * h * 0.0003:
        handleRudeImage(im)
#        print 'Sexy Playing'
#    else:
#        print 'Normal'
    im.close()

while inTotalTime():
    time.sleep(duration*3) # 间隔duration分钟对屏幕采样
    screenScrape()
# 程序正常退出提醒
sendMessage(u'监控程序正常退出', fromUser, password, toUser, smtp_server)

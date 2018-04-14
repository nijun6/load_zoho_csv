#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import random

msg = [u"来啊！！",u"人呢？！出来啊"]
driver = webdriver.Chrome()
driver.get('https://wx.qq.com/')
time.sleep(30)
driver.find_element_by_xpath(r'//*[@id="J_NavChatScrollBody"]/div/div[2]/div/div[3]/h3/span').click()
print "ok"
#for x in xrange(1,20):
while True:
    num = random.randint(0,12)
    driver.find_element_by_xpath(r'//*[@id="editArea"]').send_keys(msg[num])
    time.sleep(1)
    driver.find_element_by_xpath(r'//*[@id="chatArea"]/div[3]/div[3]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath(r'//*[@id="editArea"]').clear()

print 'over'
#driver.close()
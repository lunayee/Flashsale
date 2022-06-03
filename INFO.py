import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
import time


class TopPost:

    def __init__(self):
        self.dri = 0

    def Chrome(self,url):
        global driver
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-notifications')
        path = Service('E:/Vivaldi/driver/chromedriver.exe')
        driver = webdriver.Chrome(service=path,options=option)
        driver.get(url)
        self.dri = driver
        return driver

    def _log_fb(self):
        self.Chrome('https://www.facebook.com/')
        username = driver.find_element(By.NAME,'email')
        password = driver.find_element(By.NAME,'pass')
        login = driver.find_element(By.NAME,'login')
        username.send_keys("z55442211@yahoo.com.tw")
        password.send_keys("AsdZxc556622")
        login.click()
        time.sleep(1)
        self.dri = driver
        return driver
        
    
    def getPost(self,url):
        self.dri.get(url)
        showmany = WebDriverWait(self.dri, 10).until(EC.presence_of_element_located((By.XPATH,"//*[text()='顯示更多']"))).click()
        context = WebDriverWait(self.dri, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[role="feed"]')))
        return context.text


# x = TopPost().fb
# x.get('https://www.facebook.com/taiwanauction/')

# showmany = WebDriverWait(x, 10).until(EC.presence_of_element_located((By.XPATH,"//*[text()='顯示更多']"))).click()
# context = WebDriverWait(x, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[role="feed"]')))
# print(context.text,"---")
x = TopPost()
x._log_fb()
print(x.getPost('https://www.facebook.com/taiwanauction/'))

    
# if __name__ == '__main__':
#     #bt4()
#     log_fb()

from email.message import Message
from unicodedata import name
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import concurrent.futures
import threading
import time
import re
import urls


class TopPost:

    def __init__(self):
        self.dri = 0

    def Chrome(self, url):
        global driver
        options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values':{
                'images':2,
            }
        }
        options.add_argument('--disable-notifications')
        options.add_experimental_option('prefs',prefs)
        #path = Service('E:/Vivaldi/driver/chromedriver.exe') #家裡
        path = Service('D:/05_home/Flashsale/chromedriver.exe') #公司

        driver = webdriver.Chrome(service=path, options=options)
        driver.get(url)
        return driver


    def _log_fb(self):
        self.Chrome('https://www.facebook.com/')
        username = driver.find_element(By.NAME, 'email')
        password = driver.find_element(By.NAME, 'pass')
        login = driver.find_element(By.NAME, 'login')
        username.send_keys("z55442211@yahoo.com.tw")
        password.send_keys("AsdZxc556622")
        login.click()
        time.sleep(1)
        self.dri = driver
        return driver
    
    def wait(self,method,rule):
        return WebDriverWait(self.dri, 10).until(EC.presence_of_element_located((method, rule)))

    def isdriver(self,url):#確保瀏覽器開啟
        return self.dri.get(url) if self.dri != 0 else self.Chrome(url)

    def getHref(self, url):  # 抓取第一篇文章url
        self.isdriver(url)
        actions = ActionChains(self.dri)
        arrow = self.wait(By.CSS_SELECTOR,'span:nth-child(2) > span > a')
        actions.move_to_element(arrow).perform()
        if "%" in url:
            context = self.wait(By.CSS_SELECTOR,'[href*="story_fbid"]')
        else :
            context = self.wait(By.CSS_SELECTOR,'[href*="posts"]')
        href = context.get_attribute("href")
        return href

    def getMessage(self, url):
        self.isdriver(url)
        self.wait(By.XPATH,'//*[text()="顯示更多"]').click() 
        context = self.wait(By.CSS_SELECTOR,'[data-ad-comet-preview="message"]')
        return context.text

    def getTop(self, url):  # 抓取置頂文
        self.isdriver(url)
        showmany =self.wait(By.XPATH,'//*[text()="顯示更多"]').click() 
        context = self.wait(By.CSS_SELECTOR,'div[role="feed"]')
        return context.text

    def findFirst(self, pattern, text):  # 找第一個
        return re.compile((r"{}").format(pattern)).search(text).group()

    def findAll(self, pattern, text):  # 找全部 包含空白
        return re.findall((r"{}").format(pattern), text)

    def findPrecise(self, pattern, text):  # 精確找全部 findPrecise(X, text)
        DATA = {}
        for clo, pa in pattern.items():
            DATA[clo] = [i.group() for i in re.finditer(pa, text)]
        return DATA

    def pageclose(self):
        return self.dri.close()


def collectPostUrl():
    PostUrl=[]
    for u in urls.flashstore:
        posturl = fb.getHref(u)
        PostUrl.append(posturl)
    return PostUrl

def getcontext(url):
    try:
        text = fb.getMessage(url)
        find_text = fb.findPrecise(X, text)
        find_text['url'] = url
        find_text['context'] = text
        test.append(find_text)
        return find_text
    except:
        return ("未知錯誤",url)
    


def debug():
    X = {'Address': "\w*(縣|市)\w*號", 'Time': "\d+\s*[:：]\s*\d+", 'Date': "(\d+[/／]\d+[/／]\d+)|(\d+[/／]\d+)|(即日起)|(\d+月\d+日)"}
    fb = TopPost()
    fb._log_fb()
    test = []
    start = time.time()

    for u in urls.flashstore:#78秒
        try:
            posturl = fb.getHref(u)
            text = fb.getMessage(posturl)
            find_text = fb.findPrecise(X, text)
            find_text['url'] = u
            find_text['context'] = text
            test.append(find_text)
            print(find_text)
        except ElementClickInterceptedException:#當前元素是不可以點選,但是確實存在在頁面上,有可能是被loading覆蓋了
            text = fb.getTop(u)
            find_text = fb.findPrecise(X, text)
            find_text['url'] = u
            find_text['context'] = text
            test.append(find_text)
            print(find_text)
        except:
            print("未知錯誤",u)
    end = time.time()
    print(end - start)

if __name__ =='__main__': ##229秒
    
    X = {'Address': "\w*(縣|市)\w*號", 'Time': "\d+\s*[:：]\s*\d+", 'Date': "(\d+[/／]\d+[/／]\d+)|(\d+[/／]\d+)|(即日起)|(\d+月\d+日)"}
    thread_list = []
    test = []
    fb = TopPost()
    fb._log_fb()
    posturl = collectPostUrl()
    semaphore = threading.BoundedSemaphore(5) #最大線程數5個
    start = time.time()
    try:
        for idx, url in enumerate(posturl):
            t = threading.Thread(name=f'Thread {idx}', target=getcontext, args=(url,))
            t.start()
            thread_list.append(t)
            print(t.name,' started')

    except:
        print("未知錯誤",url)
        

    for t in thread_list:
        t.join()
        print(t.name,' join')

    end = time.time()
    print(test)
    fb.pageclose()
    
    print(end - start)
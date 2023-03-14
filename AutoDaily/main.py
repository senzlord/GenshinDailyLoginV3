import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# op = webdriver.ChromeOptions()
# op.add_argument('headless')

chop = webdriver.ChromeOptions()
chop.add_argument("start-maximized")
# chop.add_argument("headless")
s=Service(r"./chromedriver/chromedriver.exe")
browser = webdriver.Chrome(options=chop, service=s)

## Login 1
url = "https://hoyolab.com/"
browser.get(url)
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1704274066, 'httpOnly': False, 'name': '_MHYUUID', 'path': '/', 'secure': False, 'value': '13dcaa23-61f6-4953-ab97-5124714d360e'})
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1704274086, 'httpOnly': False, 'name': 'ltoken', 'path': '/', 'secure': True, 'value': 'NnAQWylX8lqXzlCP4UmayTCYednSwgUkQl6b7ny6'})
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1672910885, 'httpOnly': False, 'name': 'cookie_token', 'path': '/', 'secure': True, 'value': 'TFoXT7doO1gF4NRHasySaD8R3dsAYhTLB9Wx0prs'})
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1704274054, 'httpOnly': False, 'name': 'DEVICEFP_SEED_ID', 'path': '/', 'secure': False, 'value': '222ccf3fc5399817'})
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1672824456, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.604659338.1672738057'})
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1704274086, 'httpOnly': False, 'name': 'ltuid', 'path': '/', 'secure': True, 'value': '101531102'})
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1704274054, 'httpOnly': False, 'name': 'DEVICEFP_SEED_TIME', 'path': '/', 'secure': False, 'value': '1672738054820'})
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1672910885, 'httpOnly': False, 'name': 'account_id', 'path': '/', 'secure': True, 'value': '101531102'})
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1707298056, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.1651800697.1672738057'})
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1704274054, 'httpOnly': False, 'name': 'mi18nLang', 'path': '/', 'secure': False, 'value': 'en-us'})
browser.add_cookie({'domain': 'hoyolab.com', 'expiry': 1704274066, 'httpOnly': False, 'name': 'DEVICEFP', 'path': '/', 'secure': False, 'value': '38d7ebc663047'})
time.sleep(3)

## Login 2 + Daily Page
url = "https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481"
browser.get(url)
browser.add_cookie({'domain': 'act.hoyolab.com', 'expiry': 1707298055, 'httpOnly': False, 'name': 'G_ENABLED_IDPS', 'path': '/', 'secure': False, 'value': 'google'})
time.sleep(3)

## Do Click for Daily
# print(dir(By))
browser.find_element(By.CSS_SELECTOR, "span[class^='components-home-assets-__sign-guide_---guide-close']").click() #Click Button Close
AllButton = browser.find_elements(By.CSS_SELECTOR, "div[class^='components-home-assets-__sign-content_---sign-item']") #Get All Daily Button
for button in AllButton:
    try:
        button.click()
    except Exception as e:
        print("An exception occurred: "+e)
        time.sleep(10)
        browser.quit()
    
# assert "Genshin" in browser.title
# elem = browser.find_element
# time.sleep(60)
# cookies = browser.get_cookies()
# for cookie in cookies:
#     print(cookie)

browser.quit()
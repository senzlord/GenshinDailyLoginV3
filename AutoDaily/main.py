from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import json
import pymongo
import os
from dotenv import load_dotenv

# Get Data From MongoDB
load_dotenv()
mongo_client_link = os.getenv('MONGO_CLIENT_LINK')
mongo_client_db = os.getenv('MONGO_CLIENT_DB')
mongo_client_collection = os.getenv('MONGO_CLIENT_COLLECTION')
mongo_client = pymongo.MongoClient(mongo_client_link)

# Select the database and collection
if mongo_client_db in mongo_client.list_database_names():
    db = mongo_client[mongo_client_db]
    print("The database exists.")
else:
    print("The database doesn't exists.")
    exit()
    
if mongo_client_collection in db.list_collection_names():
    collection = db[mongo_client_collection]
    print("The collection exists.")
else:
    print("The collection doesn't exists.")
    exit()

# Find all documents in the collection
LoginDocuments = collection.find()

# Print the documents
for Login in LoginDocuments:
    cookies = Login['cookies']
    cookies.sort(key=lambda x: x["domain"], reverse=True)
    for cookie in cookies:
        print(cookie['domain'][1:],cookie['expiry'],cookie['httpOnly'],cookie['name'],cookie['path'],cookie['secure'],cookie['value'])

    chop = webdriver.ChromeOptions()
    chop.add_argument("start-maximized")
    # chop.add_argument("headless")
    s=Service(r"./chromedriver/chromedriver.exe")
    browser = webdriver.Chrome(options=chop, service=s)

    ## Login 1
    url = "https://hoyolab.com/"
    browser.get(url)
    for cookie in cookies:
        if cookie['domain'][1:] == 'hoyolab.com':
            browser.add_cookie({'domain': cookie['domain'][1:], 'expiry': cookie['expiry'], 'httpOnly': cookie['httpOnly'], 'name': cookie['name'], 'path': cookie['path'], 'secure': cookie['secure'], 'value': cookie['value']})
    browser.refresh()
    time.sleep(3)

    ## Login 2 + Daily Page
    url = "https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481"
    browser.get(url)
    for cookie in cookies:
        if cookie['domain'][1:] == 'act.hoyolab.com':
            browser.add_cookie({'domain': cookie['domain'][1:], 'expiry': cookie['expiry'], 'httpOnly': cookie['httpOnly'], 'name': cookie['name'], 'path': cookie['path'], 'secure': cookie['secure'], 'value': cookie['value']})
    browser.refresh()
    time.sleep(3)

    ## Do Click for Daily
    browser.find_element(By.CSS_SELECTOR, "span[class^='components-home-assets-__sign-guide_---guide-close']").click() #Click Button Close
    AllButton = browser.find_elements(By.CSS_SELECTOR, "div[class^='components-home-assets-__sign-content_---sign-item']") #Get All Daily Button
    for button in AllButton:
        try:
            button.click()
        except Exception as e:
            print("An exception occurred: "+e)
            time.sleep(10)
            browser.deleteAllCookies()
            browser.quit()
            
    browser.deleteAllCookies()
    browser.quit()
    
    time.sleep(30)
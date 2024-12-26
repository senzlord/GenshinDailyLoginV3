from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as TE
from webdriver_manager.chrome import ChromeDriverManager

import time
import pymongo
import os
import platform
from dotenv import load_dotenv
from datetime import datetime

# Get Data From MongoDB
load_dotenv()
mongo_client_link = os.getenv('MONGO_CLIENT_LINK')
mongo_client_db = os.getenv('MONGO_CLIENT_DB')
mongo_client_collection = os.getenv('MONGO_CLIENT_COLLECTION')
mongo_client_log_collection = os.getenv('MONGO_CLIENT_LOG_COLLECTION')
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
    
# Check if the collection exists
if mongo_client_log_collection in db.list_collection_names():
    log_collection = db[mongo_client_log_collection]
    print("The log collection exists.")
else:
    print("The log collection doesn't exist. Creating it now.")
    log_collection = db[mongo_client_log_collection]
    # Create the collection by inserting a document
    log_collection.insert_one({"message": "Initializing log collection"})
    print("Log collection created and initialized.")

# Find all documents in the collection
LoginDocuments = collection.find()
ListAccountSuccess = []
ListAccountFail = []

# Print the documents
for Login in LoginDocuments:
    username = Login['username']
    cookies = Login['cookies']
    cookies.sort(key=lambda x: x["domain"], reverse=True)

    # Create a new Chrome browser instance with options
    chop = webdriver.ChromeOptions()
    if os.getenv('HEADLESS') == 'true':
        chop.add_argument("--headless")
    else:
        chop.add_argument("start-maximized")
    chop.add_argument("--no-sandbox")
    chop.add_argument("--disable-dev-shm-usage")

    # Use WebDriver Manager to automatically handle ChromeDriver
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chop)

    # Navigate to the given URL
    url = 'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481'
    browser.get(url)

    wait = WebDriverWait(browser, 10)

    # Login 2 + Daily Page
    target_domains = ['.hoyolab.com', '.hoyoverse.com']
    browser.get(url)
    for cookie in cookies:
        if any(domain in cookie['domain'] for domain in target_domains):
            print(f"Adding cookie for domain: {cookie['domain']}")
            # Dynamically construct the cookie dictionary
            dynamic_cookie = {key: cookie[key] for key in cookie if key != 'domain'}
            dynamic_cookie['domain'] = cookie['domain']
            # Add the cookie to the browser
            browser.add_cookie(dynamic_cookie)

    browser.refresh()
    
    print(f"Waiting for 10 seconds before clicking daily check-in content ...")
    for i in range(10, 0, -1):
        print(f"\r{i} seconds remaining...", end="")
        time.sleep(1)
    print("\n")

    ## Click Guide Modal
    modal_close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*=---guide-close]')))
    modal_close_button.click()
    
    # Access GenshinTest database
    try:
        ## Click daily check-in button
        click_daily_sign_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class*='components-home-assets-__sign-content-test_---sign-wrapper---']")))
        click_daily_sign_button.click()
        time.sleep(3)
        ## Check Modal is open or not after click daily check-in
        checker_modal_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class*=---dialog-close]')))
        checker_modal_close_button.click()
        user_data = {"username": username, 'timestamp': datetime.now()}
        log_collection.insert_one(user_data)
        print(f"{username} Check-in successful!")
        ListAccountSuccess.append(username)
    except TE:
        print(f"{username} Check-in unsuccessful! or Already Check-in!")
        ListAccountFail.append(username)
            
    browser.delete_all_cookies()
    browser.quit()
    
    print(f"Waiting for 10 seconds before clicking going to next account ...")
    for i in range(10, 0, -1):
        print(f"\r{i} seconds remaining...", end="")
        time.sleep(1)
    print("\n")
    
print("All Account Clear")
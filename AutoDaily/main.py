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
from dotenv import load_dotenv
from datetime import datetime
import random

def log_with_time(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def initialize_mongo():
    """Initialize MongoDB connection and collections."""
    load_dotenv()
    mongo_client = pymongo.MongoClient(os.getenv('MONGO_CLIENT_LINK'))

    # Select database
    mongo_client_db = os.getenv('MONGO_CLIENT_DB')
    if mongo_client_db in mongo_client.list_database_names():
        db = mongo_client[mongo_client_db]
        log_with_time("The database exists.")
    else:
        log_with_time("The database doesn't exist.")
        exit()

    # Select collection
    mongo_client_collection = os.getenv('MONGO_CLIENT_COLLECTION')
    if mongo_client_collection in db.list_collection_names():
        collection = db[mongo_client_collection]
        log_with_time("The collection exists.")
    else:
        log_with_time("The collection doesn't exist.")
        exit()

    # Check or create log collection
    mongo_client_log_collection = os.getenv('MONGO_CLIENT_LOG_COLLECTION')
    if mongo_client_log_collection in db.list_collection_names():
        log_collection = db[mongo_client_log_collection]
        log_with_time("The log collection exists.")
    else:
        log_with_time("The log collection doesn't exist. Creating it now.")
        log_collection = db[mongo_client_log_collection]
        log_collection.insert_one({"message": "Initializing log collection"})
        log_with_time("Log collection created and initialized.")

    return collection, log_collection

def initialize_browser():
    """Initialize Selenium WebDriver with options."""
    chop = webdriver.ChromeOptions()
    if os.getenv('HEADLESS') == 'true':
        chop.add_argument("--headless")
    else:
        chop.add_argument("start-maximized")
    chop.add_argument("--no-sandbox")
    chop.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chop)

def add_cookies_to_browser(browser, cookies, target_domains):
    """Add cookies to the browser for specified target domains."""
    for cookie in cookies:
        if any(domain in cookie['domain'] for domain in target_domains):
            log_with_time(f"Adding cookie for domain: {cookie['domain']}")
            dynamic_cookie = {key: cookie[key] for key in cookie if key != 'domain'}
            dynamic_cookie['domain'] = cookie['domain']
            browser.add_cookie(dynamic_cookie)

def click_close_button_if_exists(browser, wait):
    try:
        # Wait for the button to be present
        close_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.components-home-assets-__sign-guide_---guide-close---2VvmzE"))
        )
        close_button.click()
        log_with_time("Close button clicked successfully.")
        return True
    except TE:
        log_with_time("Close button not found.")
        return False

def perform_check_in(browser, wait, username, log_collection):
    """Perform daily check-in and handle modal popups."""
    try:
        time.sleep(10)

        # Close guide modal if it exists
        click_close_button_if_exists(browser, wait)

        # Click daily check-in button
        check_in_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class*='components-home-assets-__sign-content-test_---sign-wrapper---']"))
        )
        check_in_button.click()
        time.sleep(3)

        # Close the confirmation modal
        modal_close_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[class*=---dialog-close]'))
        )
        modal_close_button.click()

        # Log success
        log_collection.insert_one({"username": username, "timestamp": datetime.now()})
        log_with_time(f"{username} Check-in successful!")
        return True

    except TE:
        log_with_time(f"{username} Check-in unsuccessful! or Already Check-in!")
        return False

def main():
    collection, log_collection = initialize_mongo()
    accounts = collection.find()

    # Random sleep for 5-10 minutes
    sleep_time = random.randint(300, 600)
    log_with_time(f"Sleeping for {sleep_time} seconds before starting...")
    time.sleep(sleep_time)

    for account in accounts:
        username = account['username']
        cookies = account['cookies']
        cookies.sort(key=lambda x: x["domain"], reverse=True)

        # Initialize browser
        browser = initialize_browser()
        wait = WebDriverWait(browser, 10)

        # Navigate to daily check-in page
        url = 'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481'
        browser.get(url)

        # Add cookies
        target_domains = ['.hoyolab.com', '.hoyoverse.com']
        add_cookies_to_browser(browser, cookies, target_domains)
        browser.refresh()

        # Perform check-in
        perform_check_in(browser, wait, username, log_collection)

        # Clean up
        browser.delete_all_cookies()
        browser.quit()

        # Wait before next account
        log_with_time("Waiting for 10 seconds before switching to the next account...")
        time.sleep(10)

    log_with_time("All accounts processed.")

if __name__ == "__main__":
    main()

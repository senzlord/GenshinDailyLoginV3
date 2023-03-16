import time
import platform


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def driver(username,password,fill_password):
    # create a new Chrome browser instance
    chop = webdriver.ChromeOptions()
    chop.add_argument("start-maximized")
    # chop.add_argument("headless")
    if platform.system() == 'Windows':
        s = Service(r"../chromedriver/chromedriver.exe")
    elif platform.system() == 'Linux':
        s = Service(r"../chromedriver/chromedriver")
    else:
        print("Not Supported Yet.")
        exit()
    browser = webdriver.Chrome(options=chop, service=s)

    # navigate to the given URL
    url = 'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481'
    browser.get(url)

    wait = WebDriverWait(browser, 10)
    # wait for any modal to appear and close it if it has a close button with class "---guide-close"
    try:
        modal_close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*=---guide-close]')))
        modal_close_button.click()
    except:
        pass

    # wait for the "Sign In" button to be clickable
    signin_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mhy-hoyolab-account-block')))
    # click on the "Sign In" button to open the login page
    signin_button.click()

    # fill the input field with the username
    username_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.mhy-account-flow-form-input.input-item:nth-of-type(1) input')))
    username_input.send_keys(username)
    if fill_password.lower() == 'y':
        password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.mhy-account-flow-form-input.input-item:nth-of-type(2) input')))
        password_field.send_keys(password)
        
        # wait 3 seconds before click login
        time.sleep(3)
        login_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.mhy-login-button button.login-btn')))
        login_button.click()
        
        manual_timer = 60


    # wait for user to login for some seconds
    print(f"Waiting for \r{manual_timer} seconds for user login captcha...")
    for i in range(manual_timer, 0, -1):
        print(f"\r{i} seconds remaining...", end="")
        time.sleep(1)
    print("\n")

    # check login or not
    checklogin = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mhy-hoyolab-account-block')))
    checklogin.click()
    time.sleep(5)
    # saving state on select menu
    select_menu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mhy-hoyolab-account-block div.mhy-hoyolab-select-menu')))
    time.sleep(5)
    # Check if the style display is not none
    # if select_menu.value_of_css_property('display') == 'none':
    #     print('Please Retry Login!')
    #     exit()

    style_attribute = select_menu.get_attribute('style')
    if style_attribute:
        print('Please Retry Login!')
        exit()

    # get all cookies from hoyolab.com
    cookies = browser.get_cookies()
    hoyolab_cookies = [cookie for cookie in cookies if 'hoyolab.com' in cookie['domain']]

    # print the extracted cookies
    print(hoyolab_cookies)

    # close the browser instance
    browser.quit()

    return hoyolab_cookies
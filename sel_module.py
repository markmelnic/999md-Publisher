
import os, time
from datetime import datetime
from selenium import webdriver
import selenium.webdriver.chrome.options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

MAIN_LINK = "https://999.md/ro/"
LOGIN_LINK = "https://simpalsid.com/user/login"
ADD_LINK = "https://999.md/add"

# driver boot procedure
def boot():
    # manage notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    #  driver itself
    dv_path = os.path.abspath("chromedriver.exe")
    if not "\\" in dv_path:
        dv_path = os.path.abspath("chromedriver")
    dv = webdriver.Chrome(
        chrome_options=chrome_options, executable_path=dv_path
    )
    return dv

# kill the driver
def killb(dv):
    dv.quit()

# login procedure
def login(dv, username, password):
    dv.get(LOGIN_LINK)
    time.sleep(5)

    # username
    user_field = dv.find_element_by_name("login")
    for char in username:
        user_field.send_keys(char)

    # password
    password_field = dv.find_element_by_name("password")
    for char in password:
        password_field.send_keys(char)

    # sign in
    dv.find_element_by_class_name("login__form__footer__submit").click()
    print("*** Login successful.")

def publish(dv, data, path):
    dv.get(ADD_LINK)
    time.sleep(5)

    dv.find_element_by_xpath(data.get('d', 'category')[1:-1]).click()
    time.sleep(3)

    dv.find_element_by_xpath(data.get('d', 'subcategory')[1:-1]).click()
    time.sleep(3)

    title_field = dv.find_element_by_name("12")
    for char in data.get('d', 'title')[1:-1]:
        title_field.send_keys(char)

    desc_field = dv.find_element_by_name("13")
    for char in data.get('d', 'description')[1:-1]:
        desc_field.send_keys(char)

    price_field = dv.find_element_by_name("2")
    for char in data.get('d', 'price'):
        price_field.send_keys(char)

    try:
        type_field = dv.find_element_by_name("1021").find_elements_by_tag_name("option")
        type_field[int(data.get('d', 'type')[1:-1]) + 1].click()

        state_field = dv.find_element_by_name("593").find_elements_by_tag_name("option")
        state_field[int(data.get('d', 'state')[1:-1]) + 1].click()
    except selenium.common.exceptions.NoSuchElementException or AttributeError:
        pass

    for entry in os.scandir(path):
        if ".jpg" in entry.name:
            img_path = os.path.abspath(path + "/" + entry.name)
            #print(img_path)
            dv.find_element_by_id("fileupload-file-input").send_keys(img_path)
            time.sleep(2)

    dv.find_element_by_id("agree").click()
    for i in range(20):
        try:
            dv.find_element_by_xpath("//*[@id=\"js-add-form\"]/section["+str(i)+"]/div/div/button").click()
            break
        except selenium.common.exceptions.NoSuchElementException:
            pass
    time.sleep(5)

    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    print("*** Ad published at", dt)

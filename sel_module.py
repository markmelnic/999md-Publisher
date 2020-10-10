
import os, time
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

    #  driver itself
    dv = webdriver.Chrome(
        chrome_options=chrome_options, executable_path=r"./chromedriver.exe"
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

    type_field = dv.find_element_by_name("1021").find_elements_by_tag_name("option")
    type_field[int(data.get('d', 'type')[1:-1]) + 1].click()

    state_field = dv.find_element_by_name("593").find_elements_by_tag_name("option")
    state_field[int(data.get('d', 'state')[1:-1]) + 1].click()

    for entry in os.scandir(path):
        if ".jpg" in entry.name:
            dv.find_element_by_xpath("/html/body/div[3]/div/section/div/div[1]/section[2]/div/div[1]/form/section[4]/div/section[1]/div[2]/input").send_keys(os.path.abspath(path + "/" + entry.name))

    dv.find_element_by_id("agree").click()
    dv.find_element_by_xpath("//*[@id=\"js-add-form\"]/section[6]/div/div/button").click()
    time.sleep(5)

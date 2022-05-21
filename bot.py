import selenium
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import json
import random

ELEMENT_EXIST_CHECK_DELAY = 0.5     # Time delay between each element existence check in seconds
ELEMENT_EXIST_CHECK_TIMEOUT = 300   # Number of seconds to wait before timing out of element existence check

with open('config.json', 'r') as config_file:
    user_info = json.load(config_file)

driver = webdriver.Chrome()
driver.get('https://halo.lucozade.com/')


def get_element_after_loading(type, value):
    elem = None
    attempts = 0
    while not elem:
        try:
            elem = driver.find_element(by=type, value=value)
        except selenium.common.exceptions.NoSuchElementException:
            if attempts > (ELEMENT_EXIST_CHECK_TIMEOUT / ELEMENT_EXIST_CHECK_DELAY):    # timeout / delay = number of attempts
                print(f"Timed out trying to get element type={type}, value={value}")
                raise selenium.common.exceptions.TimeoutException
            sleep(ELEMENT_EXIST_CHECK_DELAY)
        attempts += 1
    return elem


def select_option_after_loading(parent, option_value):
    select_option = None
    attempts = 0
    while not select_option:
        try:
            options = parent.find_elements(by=By.TAG_NAME, value="option")
            for option in options:
                if option.get_property("value") == option_value:
                    select_option = option
                    break
            else:
                raise selenium.common.exceptions.NoSuchElementException
        except selenium.common.exceptions.NoSuchElementException:
            if attempts > (ELEMENT_EXIST_CHECK_TIMEOUT / ELEMENT_EXIST_CHECK_DELAY):
                print(f"Timed out trying to select option: {option_value}")
                raise selenium.common.exceptions.TimeoutException
            sleep(ELEMENT_EXIST_CHECK_DELAY)
        attempts += 1

    selector = Select(parent.find_element(by=By.TAG_NAME, value="select"))
    selector.select_by_value(option_value)


def fill_field(parent, field_name, value):
    elem = parent.find_element(by=By.NAME, value=field_name)
    elem.click()
    elem.send_keys(value)

# Click "non-essential cookies" in cookie popup
cookie_field = get_element_after_loading(By.CLASS_NAME, "cookie-interface-masker")
cookie_buttons = cookie_field.find_elements(by=By.CLASS_NAME, value="block-link")
cookie_buttons[2].click()


form_div = get_element_after_loading(By.CLASS_NAME, "infx-form-shell")

# Enter first name and email fields
fill_field(form_div, "firstName", user_info['first_name'])
fill_field(form_div, "email", user_info['email'])
fill_field(form_div, "confirmEmail", user_info['email'])

# Enter phone number
phone_section = form_div.find_element(by=By.CLASS_NAME, value="input-group-mobile")
phone_code = Select(phone_section.find_element(by=By.CLASS_NAME, value="select"))
phone_code.select_by_value("+44")
fill_field(phone_section, "mobile", "7911123456")

# Enter postcode
fill_field(form_div, "postcode", "SW1A 1AA")

# Select country and location dropdowns
dropdowns = form_div.find_elements(by=By.CLASS_NAME, value="styled-select")
select_option_after_loading(dropdowns[0], "NI")
select_option_after_loading(dropdowns[1], "Tesco")

form_div.find_element(by=By.NAME, value="age").click()
form_div.find_element(by=By.NAME, value="terms").click()

# Try to get past captcha
sleep((random.random() * 3) + 1.5)
captcha = form_div.find_element(by=By.TAG_NAME, value="iframe")
captcha.click()
sleep(1)

# Click "Next" button
btns = driver.find_elements(by=By.CLASS_NAME, value="button-text")
btns[1].click()

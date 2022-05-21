import selenium
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import json
import random

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
            if attempts > 600:  # Time out after 5 minutes
                raise selenium.common.exceptions.TimeoutException
            sleep(0.5)
        attempts += 1
    return elem


def fill_field(parent, field_name, value):
    elem = parent.find_element(by=By.NAME, value=field_name)
    elem.click()
    elem.send_keys(value)

# Click "non-essential cookies" in cookie popup
cookie_field = get_element_after_loading(By.CLASS_NAME, "cookie-interface-masker")
cookie_buttons = cookie_field.find_elements(by=By.CLASS_NAME, value="block-link")
cookie_buttons[2].click()


form_div = get_element_after_loading(By.CLASS_NAME, "infx-form-shell")


fill_field(form_div, "firstName", user_info['first_name'])
fill_field(form_div, "email", user_info['email'])
fill_field(form_div, "confirmEmail", user_info['email'])

phone_section = form_div.find_element(by=By.CLASS_NAME, value="input-group-mobile")
phone_code = Select(phone_section.find_element(by=By.CLASS_NAME, value="select"))
phone_code.select_by_value("+44")
fill_field(phone_section, "mobile", "7911123456")

fill_field(form_div, "postcode", "SW1A 1AA")

dropdowns = form_div.find_elements(by=By.CLASS_NAME, value="styled-select")


dropdowns[0].click()
sleep(2)
country = Select(dropdowns[0].find_element(by=By.TAG_NAME, value="select"))
country.select_by_value("NI")

location = Select(dropdowns[1].find_element(by=By.TAG_NAME, value="select"))
location.select_by_value("Tesco")

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

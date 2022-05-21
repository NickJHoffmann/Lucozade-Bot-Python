import selenium
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import json


class BotDriver:
    """Driver class for Lucozade Halo promotion site"""

    ELEMENT_EXIST_CHECK_DELAY = 0.5  # Time delay between each element existence check in seconds
    ELEMENT_EXIST_CHECK_TIMEOUT = 300  # Number of seconds to wait before timing out of element existence check
    LUCOZADE_URL = "https://halo.lucozade.com/"
    WAYPOINT_URL = "https://www.halowaypoint.com/redeem"

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.action = ActionChains(self.driver)

        with open('config.json', 'r') as file:
            self.user_info = json.load(file)

    def get_elements_after_loading(self, type, value, get_all=False, parent=None):
        """Retrieve an element after it loads into the page"""
        if parent is None:
            parent = self.driver

        elem = None
        attempts = 0
        while not elem:
            try:
                if get_all:
                    elem = parent.find_elements(by=type, value=value)
                else:
                    elem = parent.find_element(by=type, value=value)
            except selenium.common.exceptions.NoSuchElementException:
                if attempts > (
                        self.ELEMENT_EXIST_CHECK_TIMEOUT / self.ELEMENT_EXIST_CHECK_DELAY):  # timeout / delay = number of attempts
                    print(f"Timed out trying to get element type={type}, value={value}")
                    raise selenium.common.exceptions.TimeoutException
                sleep(self.ELEMENT_EXIST_CHECK_DELAY)
            attempts += 1
        return elem

    def select_option_after_loading(self, parent, option_value):
        """Select an option in a Select element after it loads in"""
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
                if attempts > (self.ELEMENT_EXIST_CHECK_TIMEOUT / self.ELEMENT_EXIST_CHECK_DELAY):
                    print(f"Timed out trying to select option: {option_value}")
                    raise selenium.common.exceptions.TimeoutException
                sleep(self.ELEMENT_EXIST_CHECK_DELAY)
            attempts += 1

        selector = Select(parent.find_element(by=By.TAG_NAME, value="select"))
        selector.select_by_value(option_value)

    def fill_field(self, parent, field_name, value):
        """Finds and inputs text to a text box with the given name"""
        elem = parent.find_element(by=By.NAME, value=field_name)
        self.action.move_to_element(elem).click().send_keys(value).perform()

    def redeem_waypoint_code(self, code, redirect_url=None):
        """Redeem a code on Waypoint"""
        input_field = self.get_elements_after_loading(By.CLASS_NAME, "text-input_input__11DMP")
        input_field.send_keys(code)

        redeem_btn_div = self.driver.find_element(by=By.CLASS_NAME, value="redeem-code_actions__hWk8H")
        redeem_btn = redeem_btn_div.find_element(by=By.TAG_NAME, value="button")
        redeem_btn.click()

        # Wait for code to finish submitting
        redeem_headers = self.driver.find_elements(by=By.TAG_NAME, value="h1")
        while len(redeem_headers) != 2 or redeem_headers[-1].text == "Redeem Your Code":
            sleep(1)
            try:
                redeem_headers = self.driver.find_elements(by=By.TAG_NAME, value="h1")
            except selenium.common.exceptions.NoSuchElementException:
                pass

        if redirect_url:
            self.driver.get(redirect_url)
        else:
            # Reload page if code has already been used, or click "new code" button on success
            if redeem_headers[-1].text == "WHOOPS!":
                sleep(0.5)
                self.driver.get(self.WAYPOINT_URL)
            else:
                self.driver.find_element(by=By.CLASS_NAME, value="redeem-code_actions__hWk8H").find_element(
                    by=By.TAG_NAME, value="button").click()

    def login_microsoft(self):
        """Login through Microsoft login portal if necessary"""
        try:
            self.driver.find_element(by=By.ID, value="i0116").send_keys(self.user_info["microsoft_id"])
            self.driver.find_element(by=By.ID, value="i0118").send_keys(self.user_info["microsoft_pw"])
            self.driver.find_element(by=By.ID, value="idSIButton9").click()
            sleep(0.5)
            for i in range(10):
                try:
                    self.driver.find_element(by=By.ID, value="idSIButton9").click()
                    break
                except selenium.common.exceptions.ElementNotInteractableException:
                    sleep(1)
            else:
                raise selenium.common.exceptions.TimeoutException
        except selenium.common.exceptions.NoSuchElementException:
            pass

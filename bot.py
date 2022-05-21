import selenium
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import json
import random

from util.botdriver import BotDriver

MAX_SUBMISSIONS = 120       # Submission cap for website


def main():
    bot = BotDriver()

    while bot.user_info["num_completed"] < MAX_SUBMISSIONS:
        bot.driver.get(bot.LUCOZADE_URL)

        # Click "non-essential cookies" in cookie popup
        cookie_field = bot.get_elements_after_loading(By.CLASS_NAME, "cookie-interface-masker")
        cookie_buttons = cookie_field.find_elements(by=By.CLASS_NAME, value="block-link")
        cookie_buttons[2].click()

        form_div = bot.get_elements_after_loading(By.CLASS_NAME, "infx-form-shell")

        # Enter first name and email fields
        bot.fill_field(form_div, "firstName", bot.user_info['first_name'])
        bot.fill_field(form_div, "email", bot.user_info['email'])
        bot.fill_field(form_div, "confirmEmail", bot.user_info['email'])

        # Enter phone number
        phone_section = form_div.find_element(by=By.CLASS_NAME, value="input-group-mobile")
        phone_code = Select(phone_section.find_element(by=By.CLASS_NAME, value="select"))
        phone_code.select_by_value("+44")
        bot.fill_field(phone_section, "mobile", "7911123456")

        # Enter postcode
        bot.fill_field(form_div, "postcode", "SW1A 1AA")

        # Select country and location dropdowns
        dropdowns = form_div.find_elements(by=By.CLASS_NAME, value="styled-select")
        bot.select_option_after_loading(dropdowns[0], "NI")
        bot.select_option_after_loading(dropdowns[1], "Tesco")

        form_div.find_element(by=By.NAME, value="age").click()
        form_div.find_element(by=By.NAME, value="terms").click()

        # Try to get past captcha
        sleep((random.random() * 3) + 1.5)
        captcha = form_div.find_element(by=By.TAG_NAME, value="iframe")
        bot.action.move_to_element(captcha).click().perform()
        sleep(1)

        # Click "Next" button
        attempts = 0
        while attempts < (bot.ELEMENT_EXIST_CHECK_TIMEOUT / bot.ELEMENT_EXIST_CHECK_DELAY):
            try:
                btns = bot.driver.find_elements(by=By.CLASS_NAME, value="button-text")
                btns[1].click()
                break
            except selenium.common.exceptions.ElementClickInterceptedException:
                sleep(bot.ELEMENT_EXIST_CHECK_DELAY)
            attempts += 1
        else:
            print("Captcha intercepted program and was not manually overridden before timeout, exiting program")
            exit(1)


        # Page 2

        page_2_check = bot.get_elements_after_loading(By.CLASS_NAME, "lz-campaign-xbox-question-one")
        page_2_dropdowns = bot.get_elements_after_loading(By.CLASS_NAME, "styled-select", get_all=True)
        bot.select_option_after_loading(page_2_dropdowns[0], "22")
        bot.select_option_after_loading(page_2_dropdowns[1], "19:00")

        # Click "Play" button
        btns = bot.driver.find_elements(by=By.CLASS_NAME, value="button-text")
        btns[1].click()


        # Page 3

        # Click "Click to explore" widget
        page_3_check = bot.get_elements_after_loading(By.CLASS_NAME, "lz-campaign-galaxy-container")
        sleep(2)
        page_3_check.click()
        sleep(1)
        page_3_check.click()

        btn = bot.get_elements_after_loading(By.CLASS_NAME, value="button-text")
        btn.click()

        # Click "Access Redemption Portal" button
        portal_check = bot.get_elements_after_loading(By.CLASS_NAME, "lz-campaign-xbox-feedback-container")
        btn = bot.driver.find_element(by=By.CLASS_NAME, value="button-text")
        btn.click()


        # Codes page

        code_div = bot.get_elements_after_loading(By.CLASS_NAME, "lz-campaign-xbox-prize-wrapper")
        codes = [f"{code.text}\n" for code in bot.get_elements_after_loading(By.CLASS_NAME, "lz-campaign-xbox-prize-code", get_all=True)]

        with open("codes.txt", 'w') as codes_file:
            codes_file.writelines(codes)

        # Increment number completed and save to config file
        bot.user_info["num_completed"] += 1
        with open(bot.CONFIG_FILE, 'w') as file:
            json.dump(bot.user_info, file, indent=4)

        bot.driver.delete_all_cookies()
        sleep(2)

        # Navigate to Waypoint to redeem code
        bot.driver.get(f"{bot.WAYPOINT_URL}")
        bot.login_microsoft()
        bot.redeem_waypoint_code(codes[-1])


if __name__ == "__main__":
    main()

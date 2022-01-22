import time
import json
from selenium.webdriver.common.by import By
from selenium import webdriver

# Refreshing the API key by visiting Riot Games Developer page and navigating the HTML

class RiotSafariDriver:

    """ Selenium driver based on Safari """

    def __init__(self,driver):
        self.driver = driver

    def visit_login_page(self):
        # Maximize window size
        self.driver.maximize_window()
        # Visit Login page
        self.driver.get("https://developer.riotgames.com")
        # Wait 5 seconds
        time.sleep(5)
        # Find Login Button
        element = self.driver.find_element(By.CLASS_NAME, "admin-title")
        # Click & wait 5 seconds
        element.click()
        time.sleep(5)

    def sign_in(self):
        # Visit the login Page
        self.visit_login_page()
        # Find username & password text boxes
        user_text_box = self.driver.find_element(By.NAME, "username")
        pass_text_box = self.driver.find_element(By.NAME, "password")
        # Send in keys
        user_text_box.send_keys('****')
        time.sleep(8)
        pass_text_box.send_keys('*****')
        # Click on "Sign In"
        time.sleep(7)
        sign_in = self.driver.find_element(By.XPATH, "//button[@title='Sign In']").click()

    def extract_keys(self):
        time.sleep(4)
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/form/div[3]/div/div[3]/div[2]/div[2]/input').click()
        text = self.driver.find_element(By.XPATH,'//*[@id="apikey"]').get_attribute("value")
        json_object = json.dumps({'api_key': text}, indent=4)
        with open("lol_api_key.json", "w") as outfile:
            outfile.write(json_object)

RiotSafariDriver(webdriver.Safari()).sign_in()
RiotSafariDriver(webdriver.Safari()).extract_keys()

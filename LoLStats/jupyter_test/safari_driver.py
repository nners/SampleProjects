# selenium-based Safari driver to log into Riot Games Developer Portal

import time

from selenium import webdriver

# Start a session
driver = webdriver.Safari()
# Visit Developer Portal
driver.get("https://developer.riotgames.com")
time.sleep(15)
# Click Login
element = driver.find_element(By.CLASS_NAME,"admin-title")
time.sleep(10)
element.click()
time.sleep(6)
# Get username & Password
username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")
# Send Keys

# Find regenerate keys button & click

# Click on Robot Check

# Find Show Key button & click

# Extract the API key
username.send_keys('*****')
time.sleep(4)
password.send_keys('******')

time.sleep(1)
# Find click button
sign_in = driver.find_element_by_xpath("//button[@title='Sign In']")
sign_in.click()

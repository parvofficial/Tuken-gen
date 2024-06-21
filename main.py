import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome
from bs4 import BeautifulSoup
import requests
import time

# Set up Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
driver = Chrome(options=options)

# Set up email and password
email = "unverified@email.com"
password = "PARVSHOP"

# Set up random username and date of birth
username = ''.join(random.choices(string.ascii_lowercase, k=10))
day = random.randint(1, 28)
month = random.randint(1, 12)
year = random.randint(1990, 2000)

# Navigate to Discord registration page
driver.get("https://discord.com/register")

# Fill in registration form
driver.find_element_by_name("email").send_keys(email)
driver.find_element_by_name("username").send_keys(username)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_name("day").send_keys(day)
driver.find_element_by_name("month").send_keys(month)
driver.find_element_by_name("year").send_keys(year)

# Click on register button
driver.find_element_by_xpath("//button[@type='submit']").click()

# Check if captcha is required
try:
    captcha_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='hcaptcha']"))
    )
    print("Captcha required. Please solve the captcha.")
    # Wait for user to solve captcha
    input("Press enter when captcha is solved...")
except:
    print("No captcha required.")

# Verify email
driver.get("https://discord.com/verify")
driver.find_element_by_name("email").send_keys(email)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_xpath("//button[@type='submit']").click()

# Get Discord token
token_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//meta[@name='csrf-token']"))
)
token = token_element.get_attribute("content")

# Save token to file
with open("tokens.txt", "a") as f:
    f.write(f"{token}\n")

print("Account created successfully!")

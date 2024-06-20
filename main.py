import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# Set up the email and password
email = "unverified@email.com"
password = "PARVSHOP"

# Set up the random username and date of birth
username = f"User{random.randint(1000, 9999)}"
day = random.randint(1, 28)
month = random.randint(1, 12)
year = random.randint(1990, 2005)
date_of_birth = f"{day}/{month}/{year}"

# Set up the Discord API endpoint
api_endpoint = "https://discord.com/api/v9/auth/register"

# Set up the Selenium webdriver
driver = webdriver.Firefox()  # Replace with your preferred browser

try:
    # Open the Discord registration page
    driver.get("https://discord.com/register")

    # Wait for the registration form to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    # Fill in the registration form
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("email").send_keys(email)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("date_of_birth").send_keys(date_of_birth)

    # Click the register button
    driver.find_element_by_xpath("//button[@type='submit']").click()

    # Wait for the captcha to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha")))

    # Print the captcha to the terminal
    print("Captcha:")
    print(driver.find_element_by_id("captcha").get_attribute("src"))

    # Wait for the user to solve the captcha
    input("Enter the captcha solution: ")

    # Submit the captcha solution
    driver.find_element_by_id("captcha-form").submit()

    # Wait for the account creation to complete
    WebDriverWait(driver, 10).until(EC.url_contains("https://discord.com/channels/@me"))

    print("Account created successfully!")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()

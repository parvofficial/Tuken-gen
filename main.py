import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytesseract import image_to_string
from PIL import Image
from io import BytesIO

def generate_random_username(length=10):
    """Generate a random username of a given length"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Set up the webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# Navigate to the Discord registration page
driver.get("https://discord.com/register")

# Fill in the registration form
username_input = driver.find_element_by_name("username")
username_input.send_keys(generate_random_username())
email_input = driver.find_element_by_name("email")
email_input.send_keys("unverified@email.com")
password_input = driver.find_element_by_name("password")
password_input.send_keys("PARVSHOP")
birth_month_input = driver.find_element_by_name("birth_month")
birth_month_input.send_keys("1")
birth_day_input = driver.find_element_by_name("birth_day")
birth_day_input.send_keys("1")
birth_year_input = driver.find_element_by_name("birth_year")
birth_year_input.send_keys("2000")

# Submit the registration form
register_button = driver.find_element_by_name("register")
register_button.click()

# Wait for the CAPTCHA to appear
try:
    captcha_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-test-selector='captcha']"))
    )
    print("CAPTCHA detected. Solving...")
    # Solve the CAPTCHA using pytesseract
    captcha_image = captcha_element.screenshot_as_png
    captcha_text = image_to_string(Image.open(BytesIO(captcha_image)))
    print(f"CAPTCHA solution: {captcha_text}")
    # Enter the CAPTCHA solution
    captcha_input = driver.find_element_by_name("captcha")
    captcha_input.send_keys(captcha_text)
except:
    print("No CAPTCHA detected. Continuing with registration.")

# Wait for the account to be created
WebDriverWait(driver, 10).until(EC.title_contains("Discord"))

# Get the token from the page
token = driver.execute_script("return localStorage.token")

# Save the token to a file
with open("token.txt", "w") as f:
    f.write(token)

print("Account created successfully! Token saved to token.txt")

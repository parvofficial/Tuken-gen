import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from captcha_solver import CaptchaSolver

# Set up Captcha solver API key
captcha_solver_api_key = "aee594e21340567ba0da575e6af5f104"

# Load proxies from proxies.txt
proxies = []
with open("proxies.txt", "r") as f:
    for line in f:
        proxies.append(f"http://{line.strip()}")

# Set up Discord registration page URL
discord_registration_url = "https://discord.com/register"

# Set up mail and password for initial registration
initial_mail = "testing120809@outlook.com"
initial_password = "PARVSHOP"

# Set up birth date details
birth_date = 27
birth_month = "September"
birth_year = 2000

# Set up display name
display_name = "PARV_TOKENS"

# Generate a random username
def generate_username():
    username = ""
    for i in range(12):
        username += random.choice("abcdefghijklmnopqrstuvwxyz1234567890")
    return username

# Create a new instance of the Chrome driver with proxy support
def create_driver(proxy):
    proxy_obj = Proxy()
    proxy_obj.proxy_type = ProxyType.MANUAL
    proxy_obj.http_proxy = proxy
    proxy_obj.ssl_proxy = proxy
    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy_obj.add_to_capabilities(capabilities)
    driver = webdriver.Chrome(desired_capabilities=capabilities)
    return driver

# Solve Captcha using Captcha solver API
def solve_captcha(driver):
    captcha_solver = CaptchaSolver(captcha_solver_api_key)
    captcha_img = driver.find_element_by_css_selector("img[src*='captcha']")
    captcha_img_url = captcha_img.get_attribute("src")
    captcha_solution = captcha_solver.solve_captcha(captcha_img_url)
    return captcha_solution

# Register a new Discord account and get the token
def register_account(proxy):
    driver = create_driver(proxy)
    driver.get(discord_registration_url)
    time.sleep(2)  # Wait for page to load

    # Generate a random username
    username = generate_username()

    # Fill in registration form
    email_input = driver.find_element_by_name("email")
    email_input.send_keys(initial_mail)
    display_name_input = driver.find_element_by_name("username")
    display_name_input.send_keys(display_name)
    username_input = driver.find_element_by_name("username")
    username_input.send_keys(username)
    password_input = driver.find_element_by_name("password")
    password_input.send_keys(initial_password)
    birth_date_input = driver.find_element_by_name("birthdate")
    birth_date_input.send_keys(f"{birth_date} {birth_month} {birth_year}")

    # Solve Captcha
    captcha_solution = solve_captcha(driver)
    captcha_input = driver.find_element_by_name("captcha")
    captcha_input.send_keys(captcha_solution)

    # Click on "Continue" button
    continue_button = driver.find_element_by_css_selector("button[type='submit']")
    continue_button.click()
    time.sleep(5)  # Wait for registration to complete

    # Get the token from the cookies
    token = driver.execute_script("return document.cookie.match(/__dcfduid=([^;]*)/)[1];")

    # Check if account was created successfully
    try:
        account_created_text = driver.find_element_by_css_selector("div[class*='account-created']").text
        if "Account created successfully!" in account_created_text:
            print("Account created successfully!")
            return token
    except:
        print("Failed to create account")
        return None

    driver.quit()

# Ask user how many accounts to create
num_accounts = int(input("How many accounts do you want to create? "))

# Create accounts
with open("tokens.txt", "a") as f:
    for i in range(num_accounts):
        proxy = random.choice(proxies)
        token = register_account(proxy)
        if token:
            f.write(token + "\n")
            print(f"Account {i+1} created successfully! Token saved to tokens.txt")
        time.sleep(10)  # Wait 10 seconds before trying again

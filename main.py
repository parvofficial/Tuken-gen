from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import json
import time

# Generate a random username
def generate_random_username(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Initialize Chrome with DevTools Protocol enabled
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

# Update this path to where your ChromeDriver is located
driver_path = 'C:/Users/<YourUsername>/Downloads/chromedriver.exe'  # Replace with your actual path

driver = webdriver.Chrome(executable_path=driver_path, options=options, desired_capabilities=caps)

# Navigate to the Discord registration page
driver.get('https://discord.com/register')

# Fill in the email field
email_field = driver.find_element(By.NAME, 'email')
email_field.send_keys('unverified@email.com')

# Fill in the username field
username_field = driver.find_element(By.NAME, 'username')
random_username = generate_random_username()
username_field.send_keys(random_username)

# Fill in the password field
password_field = driver.find_element(By.NAME, 'password')
password_field.send_keys('PARVSHOP')

# Fill in the date of birth fields
dob_month = driver.find_element(By.NAME, 'dateOfBirth.month')
dob_month.send_keys('September')

dob_day = driver.find_element(By.NAME, 'dateOfBirth.day')
dob_day.send_keys('27')

dob_year = driver.find_element(By.NAME, 'dateOfBirth.year')
dob_year.send_keys('2000')

# Click the "Continue" button
continue_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "button-38aScr")]')
continue_button.click()

# Wait for CAPTCHA to appear (if present)
try:
    # Wait until the CAPTCHA iframe is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[contains(@src, "https://www.google.com/recaptcha/")]'))
    )
    print("CAPTCHA detected. Please solve it.")
    
    # Wait for the CAPTCHA to be solved
    WebDriverWait(driver, 300).until_not(
        EC.presence_of_element_located((By.XPATH, '//iframe[contains(@src, "https://www.google.com/recaptcha/")]'))
    )
    print("CAPTCHA solved, proceeding with registration.")
except:
    print("No CAPTCHA detected or CAPTCHA solving timeout.")

# Wait for the registration to complete and capture the network traffic
time.sleep(5)

# Retrieve the network logs
logs = driver.get_log('performance')

# Find the request that contains the token
token = None
for log in logs:
    log_data = json.loads(log['message'])
    message = log_data['message']
    if 'Network.responseReceived' in message['method']:
        response = message['params']['response']
        if 'https://discord.com/api/v9/auth/login' in response['url']:
            request_id = message['params']['requestId']
            body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
            data = json.loads(body['body'])
            if 'token' in data:
                token = data['token']
                print(f"Retrieved token: {token}")
                break

# Save the token to a file
if token:
    with open('token.txt', 'w') as file:
        file.write(token)
    print("Token saved to token.txt")
else:
    print("Token not found.")

# Close the driver
driver.quit()

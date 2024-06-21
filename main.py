import discord
from discord.ext import tasks
import asyncio
import os
import random
import string
import pyautogui
import time

client = discord.Client()

async def create_account(email, num_accounts):
    tokens = []
    for _ in range(num_accounts):
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        try:
            await client.create_dm(email, "PARVSHOP", username, "2005", "9", "27")
            token = await client.http.get_token()
            tokens.append(token)
        except discord.errors.LoginFailure:
            print("Invalid email or password. Exiting...")
            return
        except discord.errors.CaptchaRequired:
            print("Captcha required. Solving manually...")
            pyautogui.screenshot('captcha.png', region=(500, 500, 300, 100))  # adjust the region to capture the captcha
            print("Please solve the captcha and press enter when done...")
            input()
            print("Captcha solved. Continuing...")
    with open("output.txt", "w") as f:
        for token in tokens:
            f.write(f"{email}:{token}\n")
    print(f"Created {num_accounts} accounts with tokens saved to output.txt")

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

def main():
    with open("input.txt", "r") as f:
        email = f.read().strip()

    print("1: Create account")
    print("2: Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        num_accounts = int(input("How many accounts do you want to create? "))
        client.loop.create_task(create_account(email, num_accounts))
        client.run("PARVSHOP")
    elif choice == "2":
        print("Exiting...")
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()

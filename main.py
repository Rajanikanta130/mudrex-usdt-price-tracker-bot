import os
import smtplib
import requests
import time
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
from email.message import EmailMessage

def fetch_price():
    url = 'https://mudrex.com/coins/usd-coin'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the price by looking for the ₹ symbol
        for text in soup.stripped_strings:
            if '₹' in text:
                return text
        return "Price not found"
    except Exception as e:
        print(f"Error fetching price: {e}")
        return "Error fetching price"

def send_email(price):
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    receiver_email = os.environ.get('SLACK_CHANNEL_EMAIL')
    
    if not all([sender_email, sender_password, receiver_email]):
        print("Missing email credentials in environment variables.")
        return

    msg = EmailMessage()
    msg.set_content(f"Hello team!\n\nThe current Mudrex USDT buying price is {price}.\n\nHave a great day!")
    msg['Subject'] = f'Mudrex Daily USDT Price: {price}'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        # Connect to Gmail's secure SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def wait_for_target_time():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    # Define our two target times for today
    target_morning = now.replace(hour=10, minute=0, second=0, microsecond=0)
    target_evening = now.replace(hour=17, minute=30, second=0, microsecond=0)
    
    # Find which target is closer and in the future (or just passed within 1 hour)
    target = None
    if 9 <= now.hour < 11:
        target = target_morning
    elif 16 <= now.hour < 18:
        target = target_evening
        
    if target:
        diff = (target - now).total_seconds()
        if diff > 0:
            print(f"Current time: {now.strftime('%I:%M:%S %p')}. Sleeping for {int(diff)} seconds until exactly {target.strftime('%I:%M:%S %p')}...")
            time.sleep(diff)
        else:
            print(f"Target time {target.strftime('%I:%M:%S %p')} has already passed by {int(-diff)} seconds. Running immediately.")
    else:
        print("Manual run outside of scheduled windows. Running immediately.")

if __name__ == '__main__':
    wait_for_target_time()
    print("Fetching Mudrex USDT price...")
    current_price = fetch_price()
    print(f"Fetched price: {current_price}")
    print("Sending email...")
    send_email(current_price)

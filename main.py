import os
import smtplib
import requests
import time
import re
import json
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
from email.message import EmailMessage

def fetch_price(retries=3, delay=5):
    url = 'https://mudrex.com/coins/usd-coin'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 1. Try to parse JSON-LD Product schema (most reliable, standard format)
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                if not script.string:
                    continue
                try:
                    data = json.loads(script.string)
                    if data.get('@type') == 'Product':
                        offers = data.get('offers', {})
                        price = offers.get('price')
                        if price is not None:
                            price_val = float(price)
                            if price_val > 0:
                                return f"₹{price_val:.2f}"
                            else:
                                print(f"Warning: JSON-LD price on attempt {attempt} is zero or negative: {price_val}")
                except Exception as parse_err:
                    print(f"JSON-LD parsing error on attempt {attempt}: {parse_err}")
            
            # 2. Fallback: Search for ₹ followed by a valid number in stripped strings (ignores sentences, volumes, high/low)
            price_pattern = re.compile(r'^₹\s*(\d{1,3}(,\d{3})*(\.\d+)?)$')
            for text in soup.stripped_strings:
                text_clean = text.strip()
                text_clean = re.sub(r'\s+', '', text_clean)
                match = price_pattern.match(text_clean)
                if match:
                    val_str = match.group(1).replace(',', '')
                    try:
                        val = float(val_str)
                        if val > 0:
                            return text_clean
                        else:
                            print(f"Warning: Regex-matched price on attempt {attempt} is zero or negative: {val}")
                    except ValueError:
                        continue
            
            print(f"Warning: Attempt {attempt} could not extract a valid non-zero price.")
            
        except Exception as e:
            print(f"Error fetching price on attempt {attempt}: {e}")
            
        if attempt < retries:
            print(f"Sleeping for {delay} seconds before retry...")
            time.sleep(delay)
            
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


if __name__ == '__main__':
    print("Fetching Mudrex USDT price...")
    current_price = fetch_price()
    print(f"Fetched price: {current_price}")
    print("Sending email...")
    send_email(current_price)

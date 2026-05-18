# Mudrex USDT Price Tracker Bot 📈

A serverless, free, and fully automated bot that fetches the daily USDT/USDC buying price from Mudrex and sends it directly to a Slack channel (or any email address) using GitHub Actions.

## 🌟 Why this exists?
If you are dealing with on-ramp/off-ramp crypto transactions in India and need to keep track of the daily USDT buying price on Mudrex, checking the website manually every day can be tedious. 

This bot automates the process completely for **free**, without needing to run any servers or pay for cloud hosting! It runs automatically at 10:00 AM IST and 5:30 PM IST.

## 🏗️ How it Works
This project uses three simple components:
1. **Python Script:** Uses `requests` and `BeautifulSoup` to scrape the live price from Mudrex's website.
2. **Email System:** Logs into a standard Gmail account (using a secure App Password) and sends the fetched price via email.
3. **GitHub Actions:** Acts as the "server". It wakes up twice a day, runs the Python script, and goes back to sleep.

Because Slack allows you to generate a specific email address for any channel, this script simply sends an email to that Slack-generated address, and the message instantly appears in your Slack channel!

---

## 🚀 How to Set This Up for Yourself

You can easily use this exact setup for your own workspace. Just follow these steps:

### Step 1: Fork the Repository
Click the **Fork** button at the top right of this page to create your own copy of this repository.

### Step 2: Get Your Slack Channel Email
1. Open Slack, right-click the channel you want the bot to post in, and go to channel details.
2. Go to the **Integrations** tab and find **"Send emails to this channel"**.
3. Copy the email address provided.

### Step 3: Get a Gmail App Password
*For security, you cannot use your normal Gmail password. You need a dedicated "App Password".*
1. Go to your [Google Account Settings](https://myaccount.google.com/).
2. Navigate to **Security** and ensure **2-Step Verification** is turned on.
3. Go to **2-Step Verification**, scroll to the bottom, and click **App passwords**.
4. Create a new one named "Mudrex Bot". Copy the 16-letter code it gives you.

### Step 4: Add GitHub Secrets
To keep your emails and passwords safe, you must add them as Secrets in your new GitHub repository:
1. Go to your forked repository on GitHub -> **Settings** -> **Secrets and variables** -> **Actions**.
2. Click **New repository secret** and add these three exactly as named:
   * `SENDER_EMAIL` (Your Gmail address, e.g., `you@gmail.com`)
   * `SENDER_PASSWORD` (Your 16-letter Google App Password)
   * `SLACK_CHANNEL_EMAIL` (The email address Slack gave you in Step 2)

### Step 5: Test it Out!
1. Go to the **Actions** tab in your repository.
2. Click on **Mudrex Price Fetcher** on the left.
3. Click **Run workflow** on the right side to manually trigger the bot.
4. Check your Slack channel!

## ⚙️ Customizing the Schedule
If you want the bot to run at different times, open the `.github/workflows/schedule.yml` file and edit the `cron` schedule. Note that GitHub Actions uses **UTC time**.

---
*Created by [Rajanikanta130](https://github.com/Rajanikanta130)*

import requests
import os
from telegram import Bot

bot_token = os.environ.get("BOT_TOKEN")
channel_id = os.environ.get("CHANNEL_ID")

url = "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub16.txt"

response = requests.get(url)
if response.status_code == 200:
    content = response.text.strip()
    lines = content.splitlines()

    bot = Bot(token=bot_token)
    for line in lines:
        if line.strip():
            try:
                bot.send_message(chat_id=channel_id, text=line)
            except Exception as e:
                print("خطا در ارسال:", e)
else:
    print("خطا در دریافت فایل:", response.status_code)

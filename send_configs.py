import os
import requests
from telegram import Bot

def main():
    bot_token = os.getenv("BOT_TOKEN")
    channel_id = os.getenv("CHANNEL_ID")

    url = "https://github.com/Epodonios/v2ray-configs/blob/main/Sub11.txt"

    response = requests.get(url)
    if response.status_code == 200:
        content = response.text.strip()
        lines = content.splitlines()

        # فقط خطوط 10 تا 60 رو انتخاب کن (یعنی ایندکس‌های 9 تا 59)
        selected_lines = lines[9:60]

        bot = Bot(token=bot_token)

        for line in selected_lines:
            if line.strip():
                try:
                    bot.send_message(chat_id=channel_id, text=line)
                except Exception as e:
                    print("خطا در ارسال پیام:", e)
    else:
        print("خطا در دریافت فایل کانفیگ:", response.status_code)

if __name__ == "__main__":
    main()

import os
import time
import requests
from telegram import Bot

def main():
    bot_token = os.getenv("BOT_TOKEN")
    channel_id = os.getenv("CHANNEL_ID")

    url = "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt"

    response = requests.get(url)
    if response.status_code == 200:
        content = response.text.strip()
        lines = content.splitlines()

        total = len(lines)
        bot = Bot(token=bot_token)

        for i, line in enumerate(lines, start=1):
            if line.strip():
                try:
                    # حذف اسم قبلی اگر وجود دارد
                    if '#' in line:
                        line = line.split('#')[0]
                    modified_line = f"{line}#@HedwingV2ray"

                    message = f"[{i}/{total}]\n{modified_line}"
                    bot.send_message(chat_id=channel_id, text=message)
                    time.sleep(1)
                except Exception as e:
                    print(f"❌ خطا در ارسال پیام {i}: {e}")
    else:
        print("❌ خطا در دریافت فایل کانفیگ:", response.status_code)

if __name__ == "__main__":
    main()

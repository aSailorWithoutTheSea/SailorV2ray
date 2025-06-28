import os
import time
import requests
from telegram import Bot
from telegram.error import RetryAfter, TimedOut

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
                    if '#' in line:
                        line = line.split('#')[0]
                    modified_line = f"{line}#@HedwingV2ray"
                    message = f"[{i}/{total}]\n{modified_line}"

                    bot.send_message(chat_id=channel_id, text=message)
                    time.sleep(2)  # تأخیر استاندارد بین پیام‌ها
                except RetryAfter as e:
                    wait_time = int(e.retry_after)
                    print(f"⏳ Flood control: صبر کن {wait_time} ثانیه...")
                    time.sleep(wait_time)
                except TimedOut:
                    print(f"⚠️ تایم‌اوت در پیام {i}، تلاش مجدد بعد از 10 ثانیه...")
                    time.sleep(10)
                except Exception as e:
                    print(f"❌ خطا در ارسال پیام {i}: {e}")
    else:
        print("❌ خطا در دریافت فایل کانفیگ:", response.status_code)

if __name__ == "__main__":
    main()

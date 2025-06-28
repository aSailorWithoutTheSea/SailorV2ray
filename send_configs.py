import requests
import os
import time
from telegram.bot import Bot  # نسخه مخصوص 13.15

# تنظیمات اولیه
RAW_URL = "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
COUNT_PER_RUN = 4
DELAY_BETWEEN_MESSAGES = 1

# خواندن لیست کانفیگ‌ها از ریموت
response = requests.get(RAW_URL)
lines = [line.strip() for line in response.text.splitlines() if line.strip()]
total_lines = len(lines)

# خواندن ایندکس قبلی
try:
    with open("last_index.txt", "r") as f:
        start_index = int(f.read().strip())
except:
    start_index = 0

# محاسبه بازه این اجرا
end_index = start_index + COUNT_PER_RUN
if end_index > total_lines:
    end_index = total_lines

# ساخت پیام
configs = []
for i in range(start_index, end_index):
    config = lines[i]
    if not config.startswith("#"):
        config = f"@HedwingV2ray\n{config}"
    configs.append(config)

# ارسال پیام
if configs:
    message = "\n\n".join(configs)
    bot = Bot(token=BOT_TOKEN)
    try:
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        print(f"✅ ارسال موفق: از {start_index + 1} تا {end_index}")
    except Exception as e:
        print(f"❌ خطا در ارسال پیام: {e}")
else:
    print("❌ هیچ کانفیگی برای ارسال نبود.")

# به‌روزرسانی اندیس
new_index = end_index if end_index < total_lines else 0
with open("last_index.txt", "w") as f:
    f.write(str(new_index))

import requests
import os
from telegram import Bot
from urllib.parse import unquote

# تنظیمات
RAW_URL = "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
COUNT_PER_RUN = 4  # تعداد کانفیگ در هر اجرا

# خواندن کانفیگ‌ها
response = requests.get(RAW_URL)
lines = [line.strip() for line in response.text.splitlines() if line.strip()]
total_lines = len(lines)

# خواندن آخرین ایندکس
try:
    with open("last_index.txt", "r") as f:
        start_index = int(f.read().strip())
except:
    start_index = 0

end_index = start_index + COUNT_PER_RUN
if end_index > total_lines:
    end_index = total_lines

# ساختن پیام
configs = []
for i in range(start_index, end_index):
    config_line = unquote(lines[i])
    message = f"@HedwingV2ray\n{config_line}"
    configs.append(message)

final_message = "\n\n".join(configs)

# ارسال به تلگرام
bot = Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHANNEL_ID, text=final_message)

print(f"✅ ارسال موفق: از {start_index+1} تا {end_index}")

# به‌روزرسانی فایل
new_index = end_index if end_index < total_lines else 0
with open("last_index.txt", "w") as f:
    f.write(str(new_index))

import requests
import time
from telegram import Bot
import os

# تنظیمات
RAW_URL = "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt"
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
COUNT_PER_RUN = 4           # هر اجرا 4 کانفیگ ارسال شود
BATCH_SIZE = 4             # همه کانفیگ‌ها در یک پیام (پس batch_size = count_per_run)
DELAY_BETWEEN_MESSAGES = 1  # فاصله در اینجا معنایی ندارد چون فقط یک پیام ارسال می‌شود

# خواندن کانفیگ‌ها
response = requests.get(RAW_URL)
lines = [line.strip() for line in response.text.splitlines() if line.strip()]
total_lines = len(lines)

# خواندن اندیس آخرین کانفیگ ارسال شده
index_file = "last_index.txt"
try:
    with open(index_file, "r") as f:
        start_index = int(f.read().strip())
except:
    start_index = 0

end_index = min(start_index + COUNT_PER_RUN, total_lines)

bot = Bot(token=BOT_TOKEN)

batch_configs = lines[start_index:end_index]
batch_texts = []
for config in batch_configs:
    if not config.startswith("#"):
        batch_texts.append(f"@HedwingV2ray\n{config}")
message_text = "\n\n".join(batch_texts)

try:
    bot.send_message(chat_id=CHANNEL_ID, text=message_text)
    print(f"✅ پیام برای کانفیگ‌های {start_index + 1} تا {end_index} ارسال شد.")
except Exception as e:
    print(f"❌ خطا در ارسال پیام: {e}")

# ذخیره اندیس جدید
new_index = 0 if end_index >= total_lines else end_index
with open(index_file, "w") as f:
    f.write(str(new_index))

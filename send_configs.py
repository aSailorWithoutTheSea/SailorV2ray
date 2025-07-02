import requests
import os
from telegram import Bot
from urllib.parse import unquote

# تنظیمات اصلی
RAW_URL = "https://raw.githubusercontent.com/aSailorWithoutTheSea/SailorV2ray/refs/heads/main/sublink.txt"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
COUNT_PER_RUN = 8

# مرحله ۱: گرفتن کانفیگ‌ها از گیت‌هاب
try:
    response = requests.get(RAW_URL)
    response.raise_for_status()
    lines = [line.strip() for line in response.text.splitlines() if line.strip()]
    total_lines = len(lines)
except requests.exceptions.RequestException as e:
    print(f"خطا در دریافت کانفیگ از URL: {e}")
    exit()

# مرحله ۲: خواندن ایندکس آخر
try:
    with open("last_index.txt", "r") as f:
        start_index = int(f.read().strip())
except:
    start_index = 0

# مرحله ۳: انتخاب کانفیگ‌های معتبر (رد Shadowsocks)
configs_to_send = []
i = start_index
valid_configs = 0

while i < total_lines and valid_configs < COUNT_PER_RUN:
    config_line = unquote(lines[i])
    i += 1  # باید اینجا افزایش پیدا کنه حتی اگر رد شد

    cleaned_line = config_line.strip().lower()
    if cleaned_line.startswith("ss://"):
        continue

    # اضافه کردن برچسب @HedwigV2ray
    hash_index = config_line.rfind('#')
    if hash_index != -1:
        modified_config_line = config_line[:hash_index] + "#@HedwigV2ray"
    else:
        modified_config_line = config_line + "#@HedwigV2ray"

    configs_to_send.append(modified_config_line)
    valid_configs += 1

# مرحله ۴: ارسال به تلگرام
if configs_to_send and BOT_TOKEN and CHANNEL_ID:
    try:
        bot = Bot(token=BOT_TOKEN)
        final_message = "\n\n".join(configs_to_send)
        bot.send_message(chat_id=CHANNEL_ID, text=f"<pre>{final_message}</pre>", parse_mode="HTML")
        print(f"✅ ارسال موفق: {valid_configs} کانفیگ (از ایندکس {start_index} تا {i - 1})")
    except Exception as e:
        print(f"❌ خطا در ارسال پیام به تلگرام: {e}")
else:
    if not configs_to_send:
        print("⚠️ هیچ کانفیگ معتبری برای ارسال وجود نداشت.")
    else:
        print("❌ BOT_TOKEN یا CHANNEL_ID تنظیم نشده‌اند.")

# مرحله ۵: به‌روزرسانی ایندکس
new_index = i if i < total_lines else 0
try:
    with open("last_index.txt", "w") as f:
        f.write(str(new_index))
    print(f"🔄 ایندکس بعدی: {new_index}")
except Exception as e:
    print(f"❌ خطا در ذخیره‌سازی ایندکس: {e}")

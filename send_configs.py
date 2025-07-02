import requests
import os
import base64
from telegram import Bot
from urllib.parse import unquote

# لینک‌هایی که base64 هستن
BASE64_URLS = [
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/main/mci/sub_1.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/main/mci/sub_2.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/main/mci/sub_3.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/main/mci/sub_4.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/main/mtn/sub_1.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/main/mtn/sub_2.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/main/mtn/sub_3.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/main/mtn/sub_4.txt",
]

# لینک‌های raw معمولی
RAW_URLS = [
    "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt"
]

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
COUNT_PER_RUN = 8

def fetch_configs():
    lines = []
    for url in BASE64_URLS:
        try:
            r = requests.get(url)
            r.raise_for_status()
            decoded = base64.b64decode(r.text).decode("utf-8", errors="ignore")
            lines.extend([line.strip() for line in decoded.splitlines() if line.strip()])
        except Exception as e:
            print(f"❌ خطا در decode فایل {url}: {e}")

    for url in RAW_URLS:
        try:
            r = requests.get(url)
            r.raise_for_status()
            lines.extend([line.strip() for line in r.text.splitlines() if line.strip()])
        except Exception as e:
            print(f"❌ خطا در دریافت فایل {url}: {e}")

    return lines

def read_last_index():
    try:
        with open("last_index.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0

def write_last_index(idx):
    try:
        with open("last_index.txt", "w") as f:
            f.write(str(idx))
    except Exception as e:
        print(f"❌ خطا در ذخیره ایندکس: {e}")

def read_sent_configs():
    try:
        with open("sent_configs.txt", "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def append_sent_configs(new_configs):
    try:
        with open("sent_configs.txt", "a", encoding="utf-8") as f:
            for cfg in new_configs:
                f.write(cfg + "\n")
    except Exception as e:
        print(f"❌ خطا در ذخیره sent_configs: {e}")

def main():
    lines = fetch_configs()
    total_lines = len(lines)
    if total_lines == 0:
        print("⚠️ هیچ کانفیگی دریافت نشد.")
        return

    start_index = read_last_index()
    sent_configs = read_sent_configs()

    configs_to_send = []
    new_sent_configs = []

    i = start_index
    valid_count = 0

    while i < total_lines and valid_count < COUNT_PER_RUN:
        line = unquote(lines[i])
        i += 1

        if line.strip().lower().startswith("ss://"):
            continue

        # اضافه کردن تگ فقط اگر موجود نبود
        if "#@hedwigv2ray" not in line.lower():
            if "#" in line:
                modified = line[:line.rfind("#")] + "#@HedwigV2ray"
            else:
                modified = line + "#@HedwigV2ray"
        else:
            modified = line

        if modified in sent_configs:
            continue

        configs_to_send.append(modified)
        new_sent_configs.append(modified)
        valid_count += 1

    if configs_to_send and BOT_TOKEN and CHANNEL_ID:
        try:
            bot = Bot(token=BOT_TOKEN)
            final_message = "\n\n".join(configs_to_send)
            message_text = f"<pre>{final_message}</pre>\n\n@HedwigV2ray"
            bot.send_message(chat_id=CHANNEL_ID, text=message_text, parse_mode="HTML")
            print(f"✅ ارسال موفق: {valid_count} کانفیگ (از ایندکس {start_index} تا {i - 1})")
        except Exception as e:
            print(f"❌ خطا در ارسال پیام به تلگرام: {e}")
    else:
        if not configs_to_send:
            print("⚠️ هیچ کانفیگ جدیدی برای ارسال وجود نداشت.")
        else:
            print("❌ BOT_TOKEN یا CHANNEL_ID تنظیم نشده‌اند.")

    new_index = i if i < total_lines else 0
    write_last_index(new_index)
    append_sent_configs(new_sent_configs)
    print(f"🔄 ایندکس بعدی: {new_index}")

if __name__ == "__main__":
    main()

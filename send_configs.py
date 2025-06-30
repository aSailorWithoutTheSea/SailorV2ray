import requests # برای ارسال درخواست‌های HTTP (مانند دریافت محتوا از URL)
import os       # برای دسترسی به متغیرهای محیطی (مانند توکن بات)
from telegram import Bot # برای تعامل با API تلگرام
from urllib.parse import unquote # برای دیکد کردن (بازگرداندن) رشته‌های URL کدگذاری شده

# تنظیمات اصلی اسکریپت
RAW_URL = "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt" # لینک خام فایل کانفیگ در گیت‌هاب
BOT_TOKEN = os.getenv("BOT_TOKEN")     # توکن ربات تلگرام که از متغیرهای محیطی خوانده می‌شود
CHANNEL_ID = os.getenv("CHANNEL_ID")   # شناسه کانال تلگرام که از متغیرهای محیطی خوانده می‌شود
COUNT_PER_RUN = 8                      # تعداد کانفیگ‌هایی که در هر بار اجرای اسکریپت ارسال می‌شوند

# مرحله ۱: خواندن کانفیگ‌ها از لینک خام گیت‌هاب
try:
    response = requests.get(RAW_URL) # ارسال درخواست GET به لینک
    response.raise_for_status() # در صورت بروز خطا در درخواست HTTP، استثنا (Exception) ایجاد می‌کند
    lines = [line.strip() for line in response.text.splitlines() if line.strip()] # جدا کردن خطوط، حذف فضای خالی اضافی و حذف خطوط خالی
    total_lines = len(lines) # تعداد کل کانفیگ‌های موجود در فایل
except requests.exceptions.RequestException as e:
    print(f"خطا در دریافت کانفیگ از URL: {e}")
    exit() # در صورت بروز خطا، اسکریپت متوقف می‌شود

# مرحله ۲: خواندن آخرین ایندکس پردازش شده
# این بخش برای حفظ وضعیت است تا در هر بار اجرا، کانفیگ‌های جدید ارسال شوند
try:
    with open("last_index.txt", "r") as f:
        start_index = int(f.read().strip()) # خواندن ایندکس شروع از فایل
except FileNotFoundError:
    start_index = 0 # اگر فایل وجود نداشت، از ابتدای لیست شروع می‌کند
except ValueError:
    print("خطا: محتوای فایل last_index.txt معتبر نیست. از 0 شروع می‌شود.")
    start_index = 0
except Exception as e:
    print(f"خطای ناشناخته در خواندن last_index.txt: {e}")
    start_index = 0

end_index = start_index + COUNT_PER_RUN # محاسبه ایندکس پایانی برای ارسال
if end_index > total_lines:
    end_index = total_lines # اطمینان از اینکه ایندکس پایانی از تعداد کل خطوط بیشتر نشود
    if start_index >= total_lines: # اگر به انتهای فایل رسیدیم، از اول شروع می‌کنیم
        start_index = 0
        end_index = COUNT_PER_RUN
        if end_index > total_lines: # اگر تعداد کل کمتر از تعداد در هر اجرا بود
            end_index = total_lines


# مرحله ۳: ساختن پیام برای ارسال
configs_to_send = [] # لیستی برای نگهداری کانفیگ‌های آماده ارسال
if start_index < end_index: # اطمینان از اینکه کانفیگی برای ارسال وجود دارد
    for i in range(start_index, end_index):
    config_line = unquote(lines[i])  # دیکد کردن خط کانفیگ

    # رد کردن کانفیگ‌هایی که Shadowsocks هستند
    if config_line.startswith("ss://"):
        continue  # اگر کانفیگ shadowsocks بود، نادیده بگیر

    # پیدا کردن موقعیت # در خط کانفیگ
    hash_index = config_line.rfind('#')

    if hash_index != -1:
        modified_config_line = config_line[:hash_index] + "#@HedwigV2ray"
    else:
        modified_config_line = config_line + "#@HedwigV2ray"

    message = modified_config_line
    configs_to_send.append(message)

else:
    print("هیچ کانفیگی برای ارسال در این اجرا وجود ندارد یا به انتهای لیست رسیده‌ایم.")

final_message = ""
if configs_to_send:
    final_message = "\n\n".join(configs_to_send) # ترکیب تمامی کانفیگ‌ها با دو خط جدید بینشان

# مرحله ۴: ارسال پیام به تلگرام
if final_message and BOT_TOKEN and CHANNEL_ID:
    try:
        bot = Bot(token=BOT_TOKEN) # ایجاد شیء بات تلگرام
        bot.send_message(chat_id=CHANNEL_ID, text=f"<pre>{final_message}</pre>", parse_mode="HTML") # ارسال پیام
        print(f"✅ ارسال موفق: از ایندکس {start_index} تا {end_index-1} (خطوط {start_index+1} تا {end_index})")
    except Exception as e:
        print(f"❌ خطا در ارسال پیام به تلگرام: {e}")
        print("لطفاً از صحت BOT_TOKEN و CHANNEL_ID اطمینان حاصل کنید.")
elif not (BOT_TOKEN and CHANNEL_ID):
    print("خطا: BOT_TOKEN یا CHANNEL_ID تنظیم نشده‌اند. لطفاً متغیرهای محیطی را بررسی کنید.")
else:
    print("پیامی برای ارسال به تلگرام وجود نداشت.")


# مرحله ۵: به‌روزرسانی فایل last_index.txt برای اجرای بعدی
new_index = end_index if end_index < total_lines else 0 # محاسبه ایندکس جدید برای شروع بعدی
try:
    with open("last_index.txt", "w") as f:
        f.write(str(new_index)) # ذخیره ایندکس جدید
    print(f"🔄 ایندکس بعدی برای شروع: {new_index}")
except Exception as e:
    print(f"❌ خطا در به‌روزرسانی last_index.txt: {e}")


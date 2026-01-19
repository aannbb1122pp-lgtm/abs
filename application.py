import sys
import subprocess

def install_packages():
    """تثبيت المكاتب المطلوبة تلقائياً"""
    packages = [
        'requests',
        'pyTelegramBotAPI',
        'telebot'
    ]
    
    print("🔧 جاري تثبيت المكاتب المطلوبة...")
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} مثبت بالفعل")
        except ImportError:
            print(f"📦 جاري تثبيت {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
                print(f"✅ تم تثبيت {package}")
            except:
                print(f"❌ فشل تثبيت {package}")
                return False
    
    # محاولة استيراد TikSign
    try:
        import TikSign
        print("✅ TikSign مثبت بالفعل")
    except ImportError:
        print("❌ لم يتم العثور على TikSign")
        print("📦 يجب تثبيت TikSign يدوياً")
        return False
    
    return True

# تثبيت المكاتب قبل تشغيل الكود
if install_packages():
    print("✅ تم تثبيت جميع المكاتب بنجاح!")
else:
    print("⚠️  قد تكون هناك مشاكل في تثبيت بعض المكاتب")

# ============== استيراد المكاتب ==============
import time
import requests
import json
import random
import string
from hashlib import md5
from urllib.parse import urlencode
import os
import telebot
from telebot import types
import threading
from TikSign import Argus, Ladon, Gorgon, Newparams, UserAgentTik

print("="*60)
print("🔗 TikTok Linker - AID 1233 (تطبيق TikTok)")
print("="*60)

# ============== بيانات بوت التيليجرام ==============
TELEGRAM_TOKEN = "8579338666:AAFXeAFvwvcDiRNeb5nMh4BgKOOBMowB2tc"  # ضع توكن بوتك هنا
ADMIN_ID = "7243259283"  # ضع ايدي حسابك هنا

# ============== حالة المستخدم ==============
user_states = {}

# ============== إنشاء البوت ==============
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ============== دالة توليد hex عشوائي ==============
def generate_random_hex(length=16):
    """توليد hex عشوائي"""
    return ''.join(random.choice('0123456789abcdef') for _ in range(length))

def generate_device_id():
    """توليد device_id"""
    return str(random.randint(1000000000000000000, 9999999999999999999))

def sign_tiktok_request(params_dict, payload_dict, aid=1233):
    """توليد توقيعات TikTok"""
    
    # تحويل البيانات إلى strings
    params_str = urlencode(params_dict) if params_dict else ""
    payload_str = urlencode(payload_dict) if payload_dict else ""
    
    unix_time = int(time.time())
    sec_device_id = "AadCFwpTyztA5j9L" + generate_random_hex(9)
    
    # توليد x-ss-stub
    x_ss_stub = None
    if payload_str:
        x_ss_stub = md5(payload_str.encode('utf-8')).hexdigest()
    
    # توليد التوقيعات
    signature_headers = Gorgon(aid).Encoder(
        params=params_str,
        data=payload_str,
        cookies=None,
        unix=unix_time
    )
    
    # إضافة التوقيعات الأخرى
    signature_headers.update({
        'content-length': str(len(payload_str)),
        'x-ss-stub': x_ss_stub.upper() if x_ss_stub else "",
        'x-ladon': Ladon.encrypt(unix_time, 1611921764, aid),
        'x-argus': Argus.get_sign(
            params_str,
            x_ss_stub,
            unix_time,
            platform=0,
            aid=aid,
            license_id=1611921764,
            sec_device_id=sec_device_id,
            sdk_version='v05.00.06-ov-android',
            sdk_version_int=167775296
        )
    })
    
    return signature_headers, params_str, payload_str, unix_time

def bind_facebook_to_tiktok(session_id, facebook_token):
    """الوظيفة الرئيسية للربط"""
    
    print(f"📱 السيشن: {session_id[:10]}...")
    print(f"🔑 التوكن: {facebook_token[:20]}...")
    
    # ============== المعلمات ==============
    device_id = generate_device_id()
    current_time = int(time.time())
    current_time_ms = int(time.time() * 1000)
    
    params = {
        'passport-sdk-version': '30990',
        'manifest_version_code': '350302',
        '_rticket': str(current_time_ms),
        'app_language': 'ar',
        'app_type': 'normal',
        'iid': device_id,
        'channel': 'googleplay',
        'device_type': '2201116SG',
        'language': 'ar',
        'host_abi': 'arm64-v8a',
        'locale': 'ar',
        'resolution': '1080*2266',
        'openudid': generate_random_hex(16),
        'update_version_code': '350302',
        'ac2': 'wifi',
        'cdid': generate_random_hex(32),
        'sys_region': 'EG',
        'os_api': '33',
        'timezone_name': 'Asia/Baghdad',
        'dpi': '440',
        'carrier_region': 'IQ',
        'ac': 'wifi',
        'device_id': device_id,
        'os_version': '12',
        'timezone_offset': '10800',
        'version_code': '350302',
        'app_name': 'musically_go',
        'ab_version': '35.3.2',
        'version_name': '35.3.2',
        'device_brand': 'Redmi',
        'op_region': 'IQ',
        'ssmix': 'a',
        'device_platform': 'android',
        'build_number': '35.3.2',
        'region': 'EG',
        'aid': '1233',
        'ts': str(current_time),
        'okhttp_version': '4.1.103.57-ul',
        'use_store_region_cookie': '1',
        'multi_login': '1',
        'mix_mode': '1',
    }
    
    # ============== البيانات المرسلة ==============
    payload = {
        'access_token': facebook_token,
        'account_sdk_source': 'app',
        'platform_app_id': '407',
        'expires_in': '0',
        'platform': 'facebook',
    }
    
    # توليد التوقيعات
    signature_headers, params_str, payload_str, unix_time = sign_tiktok_request(params, payload, aid=1233)
    
    # ============== الهيدرات الأساسية ==============
    try:
        user_agent = UserAgentTik().get(platform="android")
    except:
        user_agent = 'com.zhiliaoapp.musically/2023113030 (Linux; U; Android 12; en_US; SM-G988N; Build/SP1A.210812.016; Cronet/TTNetVersion:5c9698e5 2023-09-05)'
    
    base_headers = {
        'Host': 'api16-normal-c-alisg.tiktokv.com',
        'Connection': 'keep-alive',
        'sdk-version': '2',
        'x-tt-store-region': 'iq',
        'x-tt-store-region-src': 'did',
        'x-ss-req-ticket': str(int(time.time() * 1000)),
        'passport-sdk-version': '19',
        'x-tt-trace-id': f"00-{generate_random_hex(32)}-{generate_random_hex(16)}-01",
        'user-agent': user_agent,
        'accept-encoding': 'gzip, deflate, br',
        'x-tt-request-tag': 't=0;ct=0;ts=0;et=1',
        'x-vc-bdturing-sdk-version': '2.3.1',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': f'sessionid={session_id}; store-idc=alisg; store-country-code=iq',
    }
    
    # دمج الهيدرات
    headers = {**base_headers, **signature_headers}
    
    # ============== إرسال الطلب ==============
    try:
        url = "https://api16-normal-c-alisg.tiktokv.com/passport/auth/bind/"
        
        response = requests.post(
            url, 
            params=params, 
            data=payload_str,
            headers=headers, 
            timeout=30
        )
        
        print(f"📡 كود الاستجابة: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                
                if result.get('message') == 'success':
                    print("✅ تم الربط بنجاح!")
                    
                    # الحصول على معلومات الحساب
                    account_info = get_account_info(session_id)
                    
                    return True, result, account_info
                else:
                    error_msg = result.get('message', 'Unknown')
                    error_code = result.get('data', {}).get('error_code', 'N/A')
                    
                    print(f"❌ فشل: {error_msg} ({error_code})")
                        
                    return False, result, None
                    
            except json.JSONDecodeError:
                print(f"📄 الرد نصي")
                return False, {'text': response.text}, None
        else:
            print(f"❌ فشل الاتصال: {response.status_code}")
            return False, {'status': response.status_code, 'text': response.text}, None
            
    except Exception as e:
        print(f"💥 خطأ: {e}")
        return False, {'error': str(e)}, None

def get_account_info(session_id):
    """الحصول على معلومات الحساب بشكل مختصر"""
    
    try:
        url = "https://api16-normal-c-alisg.tiktokv.com/passport/user/account/info/"
        
        headers = {
            'User-Agent': 'com.zhiliaoapp.musically/2023113030 (Linux; U; Android 12; en_US; SM-G988N; Build/SP1A.210812.016; Cronet/TTNetVersion:5c9698e5 2023-09-05)',
            'Cookie': f'sessionid={session_id}'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('message') == 'success':
                user_info = data.get('data', {})
                return {
                    'email': user_info.get('email', '❌ غير معروف'),
                    'username': user_info.get('username', '❌ غير معروف'),
                    'followers': user_info.get('follower_count', 0),
                    'verified': user_info.get('is_verified', False)
                }
    except:
        pass
    
    return None

def try_with_wait(session_id, facebook_token):
    """محاولة الربط مع انتظارات قصيرة"""
    
    print("🔄 بدء عملية الربط...")
    
    # انتظارات قصيرة للسرعة
    wait_times = [2, 3, 5]
    
    for i, wait_time in enumerate(wait_times):
        print(f"⏳ المحاولة {i+1}: انتظر {wait_time} ثانية")
        time.sleep(wait_time)
        
        success, result, account_info = bind_facebook_to_tiktok(session_id, facebook_token)
        
        if success:
            return True, account_info
        
        if isinstance(result, dict) and result.get('data', {}).get('error_code') == 7:
            print(f"⚠️  كثرة محاولات")
            time.sleep(10)
            continue
            
        if isinstance(result, dict) and result.get('data', {}).get('error_code') == 16:
            print(f"⚠️  AID معطل")
            break
    
    return False, None

# ============== دوال بوت التيليجرام ==============
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """ترحيب واستقبال المستخدمين"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # إضافة كليشة المبرمج
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_bind = types.InlineKeyboardButton("🔗 ربط حساب تيك توك", callback_data='bind')
    markup.add(btn_bind)
    
    # إضافة صورة المبرمج أو رمز
    welcome_text = f"""
مرحباً {user_name}! 👋

أنا بوت ربط حساب تيك توك مع فيسبوك
المبرمج: @I00EI

اضغط على الزر لبدء الربط:
    """
    
    bot.reply_to(message, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """معالجة أزرار الإنلاين"""
    user_id = call.from_user.id
    
    if call.data == 'bind':
        user_states[user_id] = {"step": "waiting_for_session"}
        
        markup = types.InlineKeyboardMarkup()
        btn_cancel = types.InlineKeyboardButton("❌ إلغاء", callback_data='cancel')
        markup.add(btn_cancel)
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🔐 **الخطوة 1 من 2**\n\n"
                 "📱 أرسل **سيشن التيك توك**\n"
                 "_(يجب أن يكون نشطاً وصحيحاً)_",
            parse_mode="Markdown",
            reply_markup=markup
        )
    
    elif call.data == 'cancel':
        if user_id in user_states:
            del user_states[user_id]
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="✅ تم إلغاء العملية."
        )

@bot.message_handler(commands=['cancel'])
def cancel_process(message):
    """إلغاء العملية الحالية"""
    user_id = message.from_user.id
    
    if user_id in user_states:
        del user_states[user_id]
        bot.reply_to(message, "✅ تم إلغاء العملية.")
    else:
        bot.reply_to(message, "❌ لا توجد عملية جارية.")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """معالجة جميع الرسائل النصية"""
    user_id = message.from_user.id
    text = message.text.strip()
    
    if user_id not in user_states:
        bot.reply_to(message, "❌ استخدم /start أولاً")
        return
    
    state = user_states[user_id]
    
    if state["step"] == "waiting_for_session":
        # حفظ السيشن
        session_id = text
        
        user_states[user_id]["step"] = "waiting_for_token"
        user_states[user_id]["session_id"] = session_id
        
        bot.reply_to(message,
            "✅ **تم حفظ السيشن**\n\n"
            "🔑 **الخطوة 2 من 2**\n\n"
            "📤 أرسل **توكن الفيسبوك**\n"
            "_(Access Token الخاص بالفيسبوك)_"
        )
    
    elif state["step"] == "waiting_for_token":
        # حفظ التوكن
        facebook_token = text
        session_id = state.get("session_id", "")
        
        if not session_id:
            bot.reply_to(message, "❌ ابدأ من جديد /start")
            del user_states[user_id]
            return
        
        # إرسال رسالة الانتظار
        wait_msg = bot.reply_to(message, "⏳ **جاري الربط...**\nانتظر قليلاً...")
        
        # تشغيل عملية الربط في thread منفصل
        def run_binding():
            try:
                # بدء عملية الربط
                success, account_info = try_with_wait(session_id, facebook_token)
                
                # بناء النتيجة المختصرة
                if success:
                    result_text = "✅ **تم الربط بنجاح**\n\n"
                    
                    if account_info:
                        # نتيجة مختصرة جداً
                        result_text += f"👤 **الحساب:** {account_info['username']}\n"
                        result_text += f"📧 **البريد:** {account_info['email'][:20]}...\n"
                        result_text += f"👥 **المتابعين:** {account_info['followers']:,}\n"
                        
                        if account_info['verified']:
                            result_text += "✅ **حساب موثق**\n"
                    
                    result_text += "\n🔗 **تم ربط التيك توك بالفيسبوك**"
                else:
                    result_text = "❌ **فشل الربط**\n\nحاول مرة أخرى أو تأكد من البيانات"
                
                # حذف رسالة الانتظار وإرسال النتيجة
                try:
                    bot.delete_message(message.chat.id, wait_msg.message_id)
                except:
                    pass
                
                # إرسال النتيجة المختصرة
                bot.send_message(message.chat.id, result_text, parse_mode="Markdown")
                
                # إضافة زر للمبرمج
                markup = types.InlineKeyboardMarkup()
                btn_developer = types.InlineKeyboardButton("👨‍💻 المبرمج @I00EI", url="https://t.me/I00EI")
                markup.add(btn_developer)
                
                bot.send_message(message.chat.id, 
                    "👨‍💻 **المبرمج:** @I00EI\n\n"
                    "⚡ **للإبلاغ عن مشاكل أو طلب ميزات**",
                    reply_markup=markup
                )
                
            except Exception as e:
                error_text = f"⚠️ **خطأ:** {str(e)[:100]}"
                try:
                    bot.delete_message(message.chat.id, wait_msg.message_id)
                except:
                    pass
                bot.send_message(message.chat.id, error_text, parse_mode="Markdown")
        
        # تشغيل في thread منفصل
        thread = threading.Thread(target=run_binding)
        thread.start()
        
        # حذف حالة المستخدم
        del user_states[user_id]

# ============== التشغيل الرئيسي ==============
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("="*60)
    print("🤖 TikTok Linker Bot - التحكم عبر تيليجرام")
    print("المبرمج: @I00EI")
    print("="*60)
    
    # التحقق من التوكن
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "8579338666:AAEN...":
        print("\n❌ **يجب تعيين توكن البوت!**")
        print("🔧 **لتعيين التوكن:**")
        print("1. افتح @BotFather في تيليجرام")
        print("2. أنشئ بوت جديد")
        print("3. احصل على التوكن")
        print("4. ضع التوكن في السطر 79")
        print("\n🔑 **مثال التوكن:** 1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ")
        input("\n🔘 اضغط Enter للخروج...")
        exit()
    
    # التحقق من ايدي الأدمن
    if not ADMIN_ID:
        print("\n❌ **يجب تعيين ايدي الأدمن!**")
        print("🔧 **لتعيين الايدي:**")
        print("1. افتح @userinfobot في تيليجرام")
        print("2. أرسل /start")
        print("3. احصل على ايدي حسابك")
        print("4. ضع الايدي في السطر 80")
        input("\n🔘 اضغط Enter للخروج...")
        exit()
    
    # عرض معلومات البوت
    print(f"\n✅ **البوت جاهز للتشغيل**")
    print(f"🤖 توكن البوت: {TELEGRAM_TOKEN[:15]}...")
    print(f"👤 ايدي الأدمن: {ADMIN_ID}")
    
    print("\n📱 **لبدء الاستخدام:**")
    print("1. افتح البوت في تيليجرام")
    print("2. اضغط /start")
    print("3. اضغط على زر 'ربط حساب'")
    print("4. أرسل السيشن ثم التوكن")
    
    print("\n" + "="*60)
    print("🤖 جاري تشغيل بوت التيليجرام...")
    print("="*60)
    
    # تشغيل البوت
    try:
        print("✅ البوت يعمل الآن!")
        print("🔄 جاري الاستماع للرسائل...")
        bot.infinity_polling(timeout=60, long_polling_timeout=30)
    except KeyboardInterrupt:
        print("\n\n👋 تم إيقاف البوت.")
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")
        print("🔧 تأكد من صحة التوكن والإعدادات.")
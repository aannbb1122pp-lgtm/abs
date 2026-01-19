import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import datetime
import os
import threading
import random
import string
import logging

# 🔹 إعدادات البوت
TOKEN = "8444000059:AAGGnmjO9uOrnpyAiHSU4vncC1vN73Nrx2M"  # ⚠️ توكن البوت
OWNER_ID = 7243259283  # ⚠️ آيدي المالك
bot = telebot.TeleBot(TOKEN)

# 🔹 قائمة الـ hosts للفيسبوك
hosts = [
    "web-sg.tiktok.com",
    "api16-normal-no1a.tiktokv.eu",
    "api16-normal-c-alisg.tiktokv.com",
    "api19-normal-c-alisg.tiktokv.com",
    "api16-normal-c-useast2a.tiktokv.com",
    "api16-normal-useast5.tiktokv.us",
    "api16-core-aion-useast5.us.tiktokv.com",
    "api16-normal-aion-useast5.us.tiktokv.com",
    "api16-normal-apix-quic.tiktokv.com",
    "api16-normal-apix.tiktokv.com",
    "api16-normal-baseline.tiktokv.com",
    "api16-normal-c-useast1a.tiktokv.com",
    "api16-normal-c-useast1a.musical.ly",
    "api16-normal-quic.tiktokv.com",
    "api16-normal-useast5.us.tiktokv.com",
    "api16-normal-useast8.us.tiktokv.com",
    "api16-normal-va.tiktokv.com",
    "api16-normal-vpc2-useast5.us.tiktokv.com",
    "api16-normal-zr.tiktokv.com",
    "api16-normal.tiktokv.com",
    "api16-normal.ttapis.com",
    "api19-core-c-alisg.tiktokv.com",
    "api19-core-c-useast1a.tiktokv.com",
    "api19-core-useast5.us.tiktokv.com",
    "api19-core-va.tiktokv.com",
    "api19-core-zr.tiktokv.com",
    "api19-core.tiktokv.com",
    "api19-normal-c-useast1a.musical.ly",
    "api19-normal-c-useast1a.tiktokv.com",
    "api19-normal-useast5.us.tiktokv.com",
    "api19-normal-va.tiktokv.com",
    "api19-normal-zr.tiktokv.com",
    "api19-normal.tiktokv.com",
    "api2-19-h2.musical.ly",
    "api2.musical.ly",
    "api21-core-c-alisg.tiktokv.com",
    "api21-core-va.tiktokv.com",
    "api21-core.tiktokv.com",
    "api21-h2-eagle.tiktokv.com",
    "api21-h2.tiktokv.com",
    "api21-normal.tiktokv.com",
    "api21-va.tiktokv.com",
    "api22-core-c-alisg.tiktokv.com",
    "api22-core-c-useast1a.tiktokv.com",
    "api22-core-va.tiktokv.com",
    "api22-core-zr.tiktokv.com",
    "api22-core.tiktokv.com",
    "api22-h2-eagle.tiktokv.com",
    "api22-normal-c-alisg.tiktokv.com",
    "api22-normal-c-useast1a.tiktokv.com"
]

# 🔹 قائمة الـ hosts للتحقق من السيشن
check_hosts = [
    "api16-normal-c-alisg.tiktokv.com",
    "api16-normal-c-useast2a.tiktokv.com",
    "api16-normal-useast5.tiktokv.us"
]

# 🔹 متغيرات التخزين
user_data = {}
saved_tokens = {}      # تخزين التوكنات المحفوظة
user_sessions = {}     # تخزين السيشنات لكل مستخدم
banned_users = set()   # المستخدمين المحظورين
all_users = set()      # جميع المستخدمين الذين استخدموا البوت

# 🔹 إنشاء لوحة المفاتيح الرئيسية (زرين فقط)
def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton("📱 ربط فيسبوك"),
        KeyboardButton("📱 ربط جوجل")
    )
    return keyboard

# 🔹 لوحة المفاتيح للإدارة (للمالك فقط)
def admin_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton("👥 قائمة المستخدمين"),
        KeyboardButton("🚫 حظر مستخدم"),
        KeyboardButton("✅ فك حظر مستخدم"),
        KeyboardButton("📊 إحصائيات البوت"),
        KeyboardButton("🔙 رجوع")
    )
    return keyboard

# 🔹 دالة التحقق من السيشن للجوجل
def check_session(sessionid):
    headers = {
        'Cookie': f'sessionid={sessionid}',
        'Connection': 'close',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'gzip, deflate'
    }

    for host in check_hosts:
        try:
            url = f'https://{host}/passport/web/account/info/'
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data.get('message') == 'success':
                return data, host
            
            if data.get('data', {}).get('name') == 'session_expired':
                continue
                
        except Exception as e:
            continue
    
    return None, None

# 🔹 دالة الربط مع فيسبوك (نفس الكود تماماً)
def facebook_connect(chat_id, acc_token, session_id):
    try:
        url = 'https://web-sg.tiktok.com/passport/web/auth/bind//?multi_login=1&did=7570092379943339543&locale=en&app_language=en&aid=1459&account_sdk_source=web&sdk_version=2.1.11-tiktokbeta.3&language=en&verifyFp=verify_mhruofnv_06uAugEF_ZvJJ_4mvw_9uY3_Bp2YsZFHMFqR&target_aid=&standalone_aid=&shark_extra=%7B%22aid%22:1459,%22app_name%22:%22Tik_Tok_Login%22,%22channel%22:%22tiktok_web%22,%22device_platform%22:%22web_pc%22,%22device_id%22:%227570092379943339543%22,%22region%22:%22IQ%22,%22priority_region%22:%22%22,%22os%22:%22windows%22,%22referer%22:%22https:%2F%2Fwww.google.com%2F%22,%22root_referer%22:%22https:%2F%2Fwww.google.com%2F%22,%22cookie_enabled%22:true,%22screen_width%22:1536,%22screen_height%22:864,%22browser_language%22:%22en-US%22,%22browser_platform%22:%22Win32%22,%22browser_name%22:%22Mozilla%22,%22browser_version%22:%225.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F137.0.0.0+Safari%2F537.36%22,%22browser_online%22:true,%22verifyFp%22:%22verify_mhruofnv_06uAugEF_ZvJJ_4mvw_9uY3_Bp2YsZFHMFqR%22,%22app_language%22:%22en%22,%22webcast_language%22:%22en%22,%22tz_name%22:%22Asia%2FBaghdad%22,%22is_page_visible%22:true,%22focus_state%22:true,%22is_fullscreen%22:false,%22history_len%22:3,%22user_is_login%22:false,%22data_collection_enabled%22:false%7D&msToken=SEX-cSdC6qEVi_LHH8px2nrnrmasM2hfCX_6CpkrLUasqnBo-eeU9u7nR6aA6PH8X8AjisuHo265F9sIp7M0u_WGF9gAHiZLpfPTQzXgZ7ZHyTnDhYHN2KQlhEXHooVGOH3B8RmwWHkV8WaERh9ikTOR&X-Bogus=DFSzsIVuKPHjcMlrCOvONuhPmkwb&X-Gnarly=MKSHRmnPawafGBsllfJm6wv5Zgs/Ocl8tuyIzEQpSAiKsV9htlh4-PwWNW2nFOu2Xv26JYfRAddw2DUqIYe2wvr3vQakDYgF3F2vhGjbs8irNlq2JtoAj7BbeD2dngowU03z2dGEpSolVPpJD5K9-zHACFrOxFJ0epqvDOcEbfwQ8u4WtExaqMnsbSf51k4Bsf0RlFQjqXkSwjEbKwLl3ukglGJbk03fJ1G-6IBKg/HbpEhLetPZGX3Jk3d9eTDJ6AiBCXBsaMsMmyNCiFBf8kF-zlvFXbxVPdwA5HRsp3jfZ0tkR9tGx7hwGcvTw2l73Qw='
        
        headers = {
            'accept': 'application/json, text/javascript',
            'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,ar;q=0.6',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.tiktok.com',
            'priority': 'u=1, i',
            'referer': 'https://www.tiktok.com',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'tt-ticket-guard-iteration-version': '0',
            'tt-ticket-guard-version': '2',
            'tt-ticket-guard-web-version': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'x-tt-passport-csrf-token': '085422f2d07bcd2e3681d5e65dc53ed3',
        }
        
        data = {
            'platform_app_id': '397',
            'access_token': acc_token,
            'aid': '1459',
            'is_sso': 'false',
            'account_sdk_source': 'web',
            'region': 'IQ',
            'language': 'en',
            'locale': 'en',
            'did': '7557409039785903627',
            'platform': 'facebook',
        }
        
        cookies = {'sessionid': session_id}
        
        response = requests.post(url, cookies=cookies, headers=headers, data=data)
        re = response.text
        
        if "Session expired. Log in to continue" in re:
            bot.send_message(chat_id, "❌ السيشن اكسباير - ارجع استخرجه من الويب من جديد\nSession expired", parse_mode=None)
        elif '''{"data":{"captcha":"","desc_url":"","description":"","error_code":3053},"message":"error"}''' in re:
            bot.send_message(chat_id, "❌ هذا سيشن تطبيق ميصير - لازم سيشن ويب\nThis is App session not web", parse_mode=None)
        elif "Error validating access token" in re:
            bot.send_message(chat_id, "⛔ توكن فيسبوك عاطل - ارجع استخرجه\nFacebook Access Token is out of order", parse_mode=None)
        elif '''data":{"age_verification_type"''' in re:
            bot.send_message(chat_id, "✅ تم الربط بنجاح مع فيسبوك!\nروح للتيكتوك وسجل من خلال فيسبوك", parse_mode=None)
        else:
            bot.send_message(chat_id, f"🔵 النتيجة:\n{re[:1000]}", parse_mode=None)
            
    except Exception as e:
        bot.send_message(chat_id, f"❌ خطأ في الربط مع فيسبوك:\n{str(e)}", parse_mode=None)

# 🔹 دالة الربط مع جوجل (نفس الكود تماماً)
def google_connect(chat_id, acc_token, session_id):
    try:
        # حفظ السيشن للمستخدم
        if chat_id not in user_sessions:
            user_sessions[chat_id] = []
        
        user_sessions[chat_id].append({
            'session': session_id,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        
        # الكود الأصلي تماماً
        cookies = {
            'sessionid': session_id,
        }
        
        headers = {
            'accept': 'application/json, text/javascript',
            'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,ar;q=0.6',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.tiktok.com',
            'priority': 'u=1, i',
            'referer': 'https://www.tiktok.com',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'tt-ticket-guard-iteration-version': '0',
            'tt-ticket-guard-version': '2',
            'tt-ticket-guard-web-version': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'x-tt-passport-csrf-token': '2a91c3d97572bdf4735cc4b31a146038',
        }
        
        data = {
            'platform_app_id': '395',
            'access_token': acc_token,
            'aid': '1459',
            'is_sso': 'True',
            'account_sdk_source': 'web',
            'region': 'IQ',
            'language': 'en',
            'locale': 'en',
            'platform': 'google',
        }
 
        host = 'web-sg.tiktok.com'
        url = f'https://{host}/passport/web/auth/bind/?multi_login=1&did=7552729227348035079&locale=en&app_language=en&aid=1459&account_sdk_source=web&sdk_version=2.1.11-tiktokbeta.3&language=en&verifyFp=verify_mfuhknub_z3N3xO1f_tlmI_4nEj_8CeR_Jo4yNjAy2Skt&target_aid=&standalone_aid=&shark_extra=%7B%22aid%22:1459,%22app_name%22:%22Tik_Tok_Login%22,%22channel%22:%22tiktok_web%22,%22device_platform%22:%22web_pc%22,%22device_id%22:%227552729227348035579%22,%22region%22:%22IQ%22,%22priority_region%22:%22%22,%22os%22:%22windows%22,%22referer%22:%22%22,%22root_referer%22:%22https:%2F%2Fwww.google.com%2F%22,%22cookie_enabled%22:true,%22screen_width%22:2560,%22screen_height%22:1440,%22browser_language%22:%22en-US%22,%22browser_platform%22:%22Win32%22,%22browser_name%22:%22Mozilla%22,%22browser_version%22:%225.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F140.0.0.0+Safari%2F537.36%22,%22browser_online%22:true,%22verifyFp%22:%22verify_mfuhknub_z3N3xO1f_tlmI_4nEj_8CeR_Jo4yNjAy2Skt%22,%22app_language%22:%22en%22,%22webcast_language%22:%22en%22,%22tz_name%22:%22Asia%2FBaghdad%22,%22is_page_visible%22:true,%22focus_state%22:true,%22is_fullscreen%22:false,%22history_len%22:7,%22user_is_login%22:false,%22data_collection_enabled%22:false%7D&msToken=5ToZFYh3aju4r-MatfK2gJWHVPu4BQVPcg2ORvMovGBW-QkQ4CmQ-bzqr4rJOEgDlqsA9ykyV2-zlX-yenm00nOQpiiIb1tbotCV9MVdrwAA0Zki3RC_AWEVVZnzz9ZWZW0vhdfz&X-Bogus=DFSzswVujrngHx1KC9vyUQVRr3Ee&X-Gnarly=Mc9YddHCjf9vYZGUoHWH9VJ3sLWnkHtXH113POXmwX1OBsgqjXbATX63zRh8wNTWQFZ/Fr6xIIXejBothCunw423wPbhCDTeWQiIklbyGFzCN3AcQcb92OZSQTl55IF1Yq8Y-nsrWbUZgwTw22ZLmn4mabinpg5oRL/yfQbZrLhXSoBA08ka2nQCv/j0uq6mcmPwC-R2RbeNSpiZxei0y36iPvHaFulYM-kz8IwdBYOWaG6rlIhqmw2J44Y/e2isjiSODscS20dWbNsTDZuqMrznsFyFAtn4fd0ZXtQTBLpA'
        
        response = requests.post(url, cookies=cookies, headers=headers, data=data)
        result = response.json()
        
        # حفظ التوكن إذا كان الربط ناجح
        if 'age_verification_type' in str(result) or 'success' in str(result).lower():
            if chat_id not in saved_tokens:
                saved_tokens[chat_id] = []
            
            token_info = {
                'token': acc_token[:20] + "..." if len(acc_token) > 20 else acc_token,
                'full_token': acc_token,
                'session': session_id[:15] + "..." if len(session_id) > 15 else session_id,
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                'status': 'ناجح'
            }
            saved_tokens[chat_id].append(token_info)
            
            bot.send_message(chat_id, "✅ تم الربط بنجاح مع جوجل!\n✅ التوكن محفوظ في قائمة التوكنات", parse_mode=None)
                
        elif 'session_expired' in str(result).lower():
            bot.send_message(chat_id, "❌ السيشن منتهي الصلاحية\nيرجى الحصول على سيشن جديد من الويب", parse_mode=None)
        elif 'error' in str(result).lower():
            bot.send_message(chat_id, "❌ خطأ في التوكن أو البيانات", parse_mode=None)
        else:
            bot.send_message(chat_id, f"🔵 نتيجة العملية:\n{str(result)[:800]}", parse_mode=None)
            
    except Exception as e:
        bot.send_message(chat_id, f"❌ خطأ في التنفيذ:\n{str(e)[:500]}", parse_mode=None)

# 🔹 دالة فك ربط (إلغاء ربط)
def fk_function(chat_id, session_id):
    try:
        HOSTS = ["api16-normal-c-alisg.tiktokv.com", "api16-normal-no1a.tiktokv.eu", "api16-normal-aion-useast5.us.tiktokv.com"]
        
        def get_info():
            for h in HOSTS:
                try:
                    response = requests.get(f'https://{h}/passport/web/account/info/', 
                                          headers={'Cookie': f'sessionid={session_id}'})
                    data = response.json()
                    if data.get('message') == 'success':
                        return h
                except:
                    continue
            return None
        
        host = get_info()
        if host:
            response = requests.post(f'https://{host}/passport/auth/unbind/?aid=8311&platform=google',
                headers={'Host': host, 'Cookie': f'sessionid={session_id}'},
                data={'platform': "google", 'ac': 'wifi', 'is_sso': 'false', 'account_sdk_source': 'web', 
                      'language': 'en', 'region': 'US', 'did': '1234567890123456789'})
            
            if response.json().get('message') == 'success':
                bot.send_message(chat_id, f"✅ تم إلغاء الربط بنجاح\nالتاريخ: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}", parse_mode=None)
            else:
                bot.send_message(chat_id, f"❌ فشل في إلغاء الربط\n{response.text[:500]}", parse_mode=None)
        else:
            bot.send_message(chat_id, "❌ سيشن غير صالح", parse_mode=None)
            
    except Exception as e:
        bot.send_message(chat_id, f"❌ خطأ في التنفيذ:\n{str(e)}", parse_mode=None)

# 🔹 أمر البدء مع الفيديو والكليشة الجميلة
@bot.message_handler(commands=['start'])
def start(message):
    # إضافة المستخدم لقائمة جميع المستخدمين
    all_users.add(message.chat.id)
    
    # التحقق إذا كان محظوراً
    if message.chat.id in banned_users:
        bot.send_message(message.chat.id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    # إنشاء الكليشة الجميلة
    caption = """ * اللهم صلي على محمد وال محمد * 

━━━☆━━━َِ𝗔 𝗕 𝗦 𖤝━━━━━☆
1. اختر نوع الربط (فيسبوك أو جوجل)
2. أدخل التوكن (Access Token)
3. أدخل الـ Session ID
4. انتظر نتيجة الربط
☆━━━━☆━━━━☆٭━━━━━━━
⚠️ *ملاحظات مهمة:*
• تأكد من صحة التوكن والـ Session
• استخدم سيشن ويب وليس تطبيق
• التوكن يجب أن يكون حديث
☆━━━٭━━☆━━━━━━━━━٭━━
مبرمج البوت  - @I00EI

*اختارلك زر رحمة  الهلك*"""
    
    # إنشاء زر للدخول لقناة المطور
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(" مطور البوت ", url="https://t.me/I00EI"))
    markup.add(InlineKeyboardButton(" قناة ", url="https://t.me/UAAAUUU"))
    
    # إرسال الفيديو مع الكليشة
    video_url = "https://t.me/kkkkyeb/988"
    bot.send_video(
        message.chat.id, 
        video_url,
        caption=caption,
        parse_mode='Markdown',
        reply_markup=markup
    )
    
    # إرسال لوحة المفاتيح الرئيسية
    bot.send_message(
        message.chat.id,
        "👇 اختر نوع الربط الذي تريده:",
        parse_mode=None,
        reply_markup=main_keyboard()
    )

# 🔹 أمر للمطور للتحكم
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id == OWNER_ID:
        bot.send_message(
            message.chat.id,
            "👑 لوحة تحكم المطور\n\n🔹 اختر من الأزرار أدناه:",
            parse_mode=None,
            reply_markup=admin_keyboard()
        )
    else:
        bot.send_message(message.chat.id, "⛔ هذا الأمر للمطور فقط!", parse_mode=None)

# 🔹 زر ربط فيسبوك
@bot.message_handler(func=lambda message: message.text == "📱 ربط فيسبوك")
def facebook_button(message):
    # التحقق إذا كان محظوراً
    if message.chat.id in banned_users:
        bot.send_message(message.chat.id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    user_data[message.chat.id] = {'type': 'facebook'}
    msg = bot.send_message(
        message.chat.id,
        "🔵 ربط حساب فيسبوك\n\n🔑 أرسل التوكن (Access Token):\n\n💡 طريقة الحصول على التوكن:\n1. افتح الموقع في المتصفح\n2. افتح Inspect Element (F12)\n3. اذهب لـ Network\n4. ابحث عن requests تحتوي على access_token",
        parse_mode=None,
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, get_token_step)

# 🔹 زر ربط جوجل
@bot.message_handler(func=lambda message: message.text == "📱 ربط جوجل")
def google_button(message):
    # التحقق إذا كان محظوراً
    if message.chat.id in banned_users:
        bot.send_message(message.chat.id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    user_data[message.chat.id] = {'type': 'google'}
    msg = bot.send_message(
        message.chat.id,
        "🔵 ربط حساب جوجل\n\n🔑 أرسل التوكن (Access Token):\n\n💡 طريقة الحصول على التوكن:\n1. سجل دخول بحساب جوجل\n2. افتح Inspect Element (F12)\n3. اذهب لـ Network\n4. ابحث عن requests تحتوي على access_token",
        parse_mode=None,
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, get_token_step)

def get_token_step(message):
    chat_id = message.chat.id
    
    # التحقق إذا كان محظوراً
    if chat_id in banned_users:
        bot.send_message(chat_id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    # التحقق إذا كان المطور يريد إلغاء
    if message.text.lower() in ['/cancel', 'إلغاء', 'cancel']:
        bot.send_message(chat_id, "تم الإلغاء", reply_markup=main_keyboard(), parse_mode=None)
        return
    
    if chat_id in user_data:
        user_data[chat_id]['token'] = message.text.strip()
        msg = bot.send_message(
            chat_id,
            "📝 أرسل الـ Session ID:\n\n💡 طريقة الحصول على الـ Session:\n1. في نفس صفحة Inspect Element\n2. اذهب لـ Application أو Storage\n3. ابحث عن Cookies\n4. ابحث عن sessionid\n5. انسخ القيمة",
            parse_mode=None
        )
        bot.register_next_step_handler(msg, get_session_step)
    else:
        bot.send_message(chat_id, "❌ حدث خطأ، ابدأ من جديد", reply_markup=main_keyboard(), parse_mode=None)

def get_session_step(message):
    chat_id = message.chat.id
    
    # التحقق إذا كان محظوراً
    if chat_id in banned_users:
        bot.send_message(chat_id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    # التحقق إذا كان المطور يريد إلغاء
    if message.text.lower() in ['/cancel', 'إلغاء', 'cancel']:
        bot.send_message(chat_id, "تم الإلغاء", reply_markup=main_keyboard(), parse_mode=None)
        return
    
    if chat_id in user_data:
        session_id = message.text.strip()
        token = user_data[chat_id]['token']
        connection_type = user_data[chat_id].get('type', 'google')
        
        if connection_type == 'google':
            bot.send_message(chat_id, "🔍 جاري التحقق من السيشن...", parse_mode=None)
            session_data, host = check_session(session_id)
            if session_data:
                bot.send_message(chat_id, f"✅ السيشن صالح\n🔍 المضيف: {host}", parse_mode=None)
            else:
                bot.send_message(chat_id, "⚠️ لم يتم التحقق من السيشن، جاري المحاولة...", parse_mode=None)
        
        bot.send_message(chat_id, "⏳ جاري عملية الربط...", parse_mode=None)
        
        if connection_type == 'facebook':
            thread = threading.Thread(target=facebook_connect, args=(chat_id, token, session_id))
        else:
            thread = threading.Thread(target=google_connect, args=(chat_id, token, session_id))
        thread.start()
        
        # تنظيف البيانات المؤقتة
        if chat_id in user_data:
            del user_data[chat_id]
    else:
        bot.send_message(chat_id, "❌ حدث خطأ، ابدأ من جديد", reply_markup=main_keyboard(), parse_mode=None)

# 🔹 زر قائمة المستخدمين (للمالك فقط)
@bot.message_handler(func=lambda message: message.text == "👥 قائمة المستخدمين" and message.chat.id == OWNER_ID)
def users_list(message):
    if message.chat.id != OWNER_ID:
        return
    
    total_users = len(all_users)
    banned_count = len(banned_users)
    active_count = total_users - banned_count
    
    response = f"📊 إحصائيات المستخدمين:\n\n"
    response += f"• 👥 إجمالي المستخدمين: {total_users}\n"
    response += f"• ✅ المستخدمين النشطين: {active_count}\n"
    response += f"• 🚫 المستخدمين المحظورين: {banned_count}\n\n"
    
    if all_users:
        response += "📋 آخر 20 مستخدم:\n"
        for i, user_id in enumerate(list(all_users)[-20:], 1):
            status = "🚫" if user_id in banned_users else "✅"
            response += f"{i}. {status} {user_id}\n"
    else:
        response += "📭 لا يوجد مستخدمين بعد"
    
    bot.send_message(message.chat.id, response, parse_mode=None)

# 🔹 زر حظر مستخدم (للمالك فقط)
@bot.message_handler(func=lambda message: message.text == "🚫 حظر مستخدم" and message.chat.id == OWNER_ID)
def ban_user_command(message):
    if message.chat.id != OWNER_ID:
        return
    
    msg = bot.send_message(
        message.chat.id,
        "🚫 حظر مستخدم\n\nأرسل آيدي المستخدم الذي تريد حظره:",
        parse_mode=None,
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, process_ban_user)

def process_ban_user(message):
    if message.chat.id != OWNER_ID:
        return
    
    try:
        user_id = int(message.text.strip())
        if user_id == OWNER_ID:
            bot.send_message(message.chat.id, "❌ لا يمكنك حظر نفسك!", parse_mode=None)
            return
        
        banned_users.add(user_id)
        bot.send_message(
            message.chat.id,
            f"✅ تم حظر المستخدم:\n{user_id}",
            parse_mode=None
        )
        
        # إعلام المستخدم بأنه تم حظره
        try:
            bot.send_message(user_id, "🚫 لقد تم حظرك من استخدام البوت!", parse_mode=None)
        except:
            pass
            
        bot.send_message(message.chat.id, "🔙", reply_markup=admin_keyboard(), parse_mode=None)
    except:
        bot.send_message(message.chat.id, "❌ آيدي غير صالح!", parse_mode=None)
        bot.send_message(message.chat.id, "🔙", reply_markup=admin_keyboard(), parse_mode=None)

# 🔹 زر فك حظر مستخدم (للمالك فقط)
@bot.message_handler(func=lambda message: message.text == "✅ فك حظر مستخدم" and message.chat.id == OWNER_ID)
def unban_user_command(message):
    if message.chat.id != OWNER_ID:
        return
    
    msg = bot.send_message(
        message.chat.id,
        "✅ فك حظر مستخدم\n\nأرسل آيدي المستخدم الذي تريد فك حظره:",
        parse_mode=None,
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, process_unban_user)

def process_unban_user(message):
    if message.chat.id != OWNER_ID:
        return
    
    try:
        user_id = int(message.text.strip())
        if user_id in banned_users:
            banned_users.remove(user_id)
            bot.send_message(
                message.chat.id,
                f"✅ تم فك حظر المستخدم:\n{user_id}",
                parse_mode=None
            )
            
            # إعلام المستخدم بأنه تم فك حظره
            try:
                bot.send_message(user_id, "✅ تم فك حظرك من البوت!\nيمكنك استخدام البوت الآن.", parse_mode=None)
            except:
                pass
        else:
            bot.send_message(message.chat.id, f"⚠️ المستخدم {user_id} ليس محظوراً أصلاً", parse_mode=None)
        
        bot.send_message(message.chat.id, "🔙", reply_markup=admin_keyboard(), parse_mode=None)
    except:
        bot.send_message(message.chat.id, "❌ آيدي غير صالح!", parse_mode=None)
        bot.send_message(message.chat.id, "🔙", reply_markup=admin_keyboard(), parse_mode=None)

# 🔹 زر إحصائيات البوت (للمالك فقط)
@bot.message_handler(func=lambda message: message.text == "📊 إحصائيات البوت" and message.chat.id == OWNER_ID)
def bot_stats(message):
    if message.chat.id != OWNER_ID:
        return
    
    total_users = len(all_users)
    banned_count = len(banned_users)
    saved_tokens_count = sum(len(tokens) for tokens in saved_tokens.values())
    
    stats_text = f"""
📈 إحصائيات البوت الشاملة

👥 المستخدمين:
• إجمالي المستخدمين: {total_users}
• المستخدمين النشطين: {total_users - banned_count}
• المستخدمين المحظورين: {banned_count}

💾 التوكنات:
• إجمالي التوكنات المحفوظة: {saved_tokens_count}
• عدد المستخدمين الذين حفظوا توكنات: {len(saved_tokens)}

🔄 السيشنات:
• إجمالي السيشنات المستخدمة: {sum(len(sessions) for sessions in user_sessions.values())}

📊 عام:
• تاريخ التشغيل: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• حالة البوت: ✅ يعمل بشكل طبيعي
"""
    
    bot.send_message(message.chat.id, stats_text, parse_mode=None)

# 🔹 زر الرجوع
@bot.message_handler(func=lambda message: message.text == "🔙 رجوع")
def back_to_main(message):
    if message.chat.id == OWNER_ID:
        bot.send_message(message.chat.id, "🔙", reply_markup=admin_keyboard(), parse_mode=None)
    else:
        bot.send_message(message.chat.id, "🏠 الرئيسية", reply_markup=main_keyboard(), parse_mode=None)

# 🔹 أمر إلغاء ربط (للمستخدمين)
@bot.message_handler(commands=['unbind'])
def unbind_command(message):
    # التحقق إذا كان محظوراً
    if message.chat.id in banned_users:
        bot.send_message(message.chat.id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    msg = bot.send_message(
        message.chat.id,
        "❌ إلغاء ربط الحساب\n\nأرسل الـ Session ID للحساب الذي تريد إلغاء ربطه:",
        parse_mode=None,
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, process_unbind)

def process_unbind(message):
    chat_id = message.chat.id
    
    # التحقق إذا كان محظوراً
    if chat_id in banned_users:
        bot.send_message(chat_id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    # التحقق إذا كان المطور يريد إلغاء
    if message.text.lower() in ['/cancel', 'إلغاء', 'cancel']:
        bot.send_message(chat_id, "تم الإلغاء", reply_markup=main_keyboard(), parse_mode=None)
        return
    
    session_id = message.text.strip()
    bot.send_message(chat_id, "⏳ جاري إلغاء الربط...", parse_mode=None)
    
    thread = threading.Thread(target=fk_function, args=(chat_id, session_id))
    thread.start()
    bot.send_message(chat_id, "🔙", reply_markup=main_keyboard(), parse_mode=None)

# 🔹 أمر عرض التوكنات المحفوظة
@bot.message_handler(commands=['mytokens'])
def my_tokens_command(message):
    # التحقق إذا كان محظوراً
    if message.chat.id in banned_users:
        bot.send_message(message.chat.id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    chat_id = message.chat.id
    if chat_id in saved_tokens and saved_tokens[chat_id]:
        tokens = saved_tokens[chat_id]
        response = "💾 التوكنات المحفوظة:\n\n"
        
        for i, token in enumerate(tokens, 1):
            response += f"{i}. التوكن: {token['token']}\n"
            response += f"   السيشن: {token['session']}\n"
            response += f"   التاريخ: {token['date']}\n"
            response += f"   الحالة: {token['status']}\n"
            response += "   ───────────────\n"
        
        response += f"\n📊 العدد الإجمالي: {len(tokens)} توكن"
        bot.send_message(chat_id, response, parse_mode=None)
    else:
        bot.send_message(chat_id, "📭 لا توجد توكنات محفوظة\n\n🔹 قم بربط حساب أولاً ليتم حفظ التوكن", parse_mode=None)

# 🔹 أمر معرفة الآيدي
@bot.message_handler(commands=['id'])
def get_my_id(message):
    # التحقق إذا كان محظوراً
    if message.chat.id in banned_users:
        bot.send_message(message.chat.id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    status = "✅ نشط" if message.chat.id not in banned_users else "🚫 محظور"
    bot.send_message(
        message.chat.id, 
        f"🆔 معلومات حسابك:\n\n• آيدي: {message.chat.id}\n• الحالة: {status}\n• التاريخ: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        parse_mode=None
    )

# 🔹 أمر المساعدة
@bot.message_handler(commands=['help'])
def help_command(message):
    # التحقق إذا كان محظوراً
    if message.chat.id in banned_users:
        bot.send_message(message.chat.id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    help_text = """
📖 أوامر البوت المتاحة:

🔹 الأوامر الأساسية:
• /start - بدء استخدام البوت
• /help - عرض هذه الرسالة
• /id - عرض آيدي حسابك
• /mytokens - عرض التوكنات المحفوظة
• /unbind - إلغاء ربط حساب

🔹 أوامر المطور:
• /admin - لوحة تحكم المطور

🔹 الأزرار المتاحة:
• 📱 ربط فيسبوك - ربط حساب فيسبوك
• 📱 ربط جوجل - ربط حساب جوجل

💡 للتواصل مع المطور:
@I00EI
"""
    
    bot.send_message(message.chat.id, help_text, parse_mode=None)

# 🔹 معالجة الرسائل الأخرى
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    chat_id = message.chat.id
    
    # التحقق إذا كان محظوراً
    if chat_id in banned_users:
        bot.send_message(chat_id, "🚫 أنت محظور من استخدام البوت!", parse_mode=None)
        return
    
    # إضافة المستخدم لقائمة جميع المستخدمين إذا لم يكن موجوداً
    if chat_id not in all_users:
        all_users.add(chat_id)
    
    # عرض لوحة المفاتيح الرئيسية
    bot.send_message(
        chat_id,
        "👋 مرحباً بك في بوت ربط تيك توك\n\n👇 اختر نوع الربط الذي تريده:",
        parse_mode=None,
        reply_markup=main_keyboard()
    )

# 🔹 تشغيل البوت
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 بوت ربط تيك توك يعمل...")
    print(f"👑 المالك: {OWNER_ID}")
    print("⭐ المطور: عبس [@I00EI]")
    print("📅 تاريخ التشغيل:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 60)
    
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")
import subprocess
import sys
import telebot
from telebot import types
import requests
import json
import os
import time
from threading import Thread
import re
import random, binascii, uuid, secrets, string

# ===== دالة لتحميل المكاتب المفقودة تلقائياً =====
def install_missing_packages():
    """تثبيت المكاتب المفقودة تلقائياً"""
    required_packages = [
        'MedoSigner',
        'telebot',
        'requests'
    ]
    
    installed_packages = []
    missing_packages = []
    
    # فحص المكاتب المثبتة
    for package in required_packages:
        try:
            if package == 'telebot':
                __import__('telebot')
            elif package == 'MedoSigner':
                __import__('MedoSigner')
            elif package == 'requests':
                __import__('requests')
            installed_packages.append(package)
        except ImportError:
            missing_packages.append(package)
    
    # تثبيت المكاتب المفقودة
    if missing_packages:
        print("🔍 جاري تثبيت المكاتب المفقودة...")
        for package in missing_packages:
            try:
                print(f"📦 تثبيت {package}...")
                if package == 'MedoSigner':
                    # محاولة تثبيت MedoSigner من GitHub إذا لم يكن متوفراً في PyPI
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "MedoSigner"])
                    except:
                        print(f"⚠️ لم أستطع تثبيت {package} من PyPI")
                        continue
                else:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ تم تثبيت {package} بنجاح")
            except Exception as e:
                print(f"❌ فشل تثبيت {package}: {e}")
        
        print("🔄 إعادة تشغيل البرنامج...")
        os.execl(sys.executable, sys.executable, *sys.argv)

# ===== تشغيل دالة التحقق من المكاتب أولاً =====
install_missing_packages()

# ===== الآن يمكن استيراد MedoSigner بأمان =====
from MedoSigner import Argus, Gorgon, Ladon, md5

# ===== إعدادات البوت =====
token = "7813538454:AAEFyW_6j-JljPLgOWEzugNDH7u1ycgPTAc"
bot = telebot.TeleBot(token, parse_mode="HTML")

# ===== دالة فحص نوع السيشن =====
def check_app_type(session_id):
    """فحص نوع التطبيق بناءً على app_id"""
    api = 'https://api31-normal-alisg.tiktokv.com/2/user/info/'
    cookies = {'sessionid': session_id}
    
    try:
        response = requests.get(url=api, cookies=cookies, timeout=10)
        data = response.json().get('data', {})
        app_id = data.get('app_id')
        
        if app_id == 1233:
            return '🇻🇮 App '
        elif app_id == 1340:
            return '🔥 Lite'
        elif app_id == 567753:
            return '🍁 Studio'
        elif app_id == 1459:
            return '🌐 Web'
        elif app_id == 1180:
            return '📱 iOS'
        else:
            return '❓ Unknown'
    except Exception as e:
        return f'❌ Error: {str(e)[:30]}'

# ===== دالة فحص الروبط الخارجية =====
def get_external_links(session_id):
    """فحص الروبط الخارجية (Google/Apple/Facebook/Twitter/Instagram)"""
    try:
        # الرابط الصحيح لفحص الروبط الخارجية
        url = "https://www.tiktok.com/passport/web/account/info/"
        
        cookies = {"sessionid": session_id}
        headers = {
            "accept": "*/*",
            "accept-language": "ar,en-US;q=0.9,en;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            "sec-ch-ua-platform": '"Windows"'
        }
        
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                if data.get('message') == 'success':
                    geo = data.get('data', {})
                    connects = geo.get('connects', [])
                    
                    external_links = []
                    
                    # فحص كل ربط
                    for connect in connects:
                        platform = connect.get('platform', '').lower()
                        
                        if platform == 'google':
                            external_links.append('google')
                        elif platform == 'apple':
                            external_links.append('apple')
                        elif platform == 'facebook':
                            external_links.append('facebook')
                        elif platform == 'twitter':
                            external_links.append('twitter')
                        elif platform == 'instagram':
                            external_links.append('instagram')
                        elif platform == 'kakaotalk':
                            external_links.append('kakao')
                        elif platform == 'line':
                            external_links.append('line')
                        elif platform == 'linkedin':
                            external_links.append('linkedin')
                        elif platform == 'snapchat':
                            external_links.append('snapchat')
                    
                    return external_links
                else:
                    # محاولة API بديل
                    return get_external_links_alternative(session_id)
                    
            except json.JSONDecodeError:
                # إذا كان الرد ليس JSON، نجرب API بديل
                return get_external_links_alternative(session_id)
        else:
            # إذا فشل الطلب، نجرب API بديل
            return get_external_links_alternative(session_id)
            
    except Exception as e:
        print(f"خطأ في فحص الروبط الخارجية: {e}")
        return []

def get_external_links_alternative(session_id):
    """API بديل لفحص الروبط الخارجية"""
    try:
        cookies = {"sessionid": session_id}
        headers = {
            'User-Agent': 'com.zhiliaoapp.musically/2021306050 (Linux; U; Android 13; ar_IQ_#u-nu-latn; ANY-LX2; Build/HONORANY-L22CQ; Cronet/TTNetVersion:57844a4b 2019-10-16)',
            'X-Khronos': str(int(time.time())),
            'X-Gorgon': '0300100f040038a0761d2b67b399b05c32364fcc76f4faa0fb05',
        }
        
        # رابط API بديل
        url = "https://api2.musical.ly/2/user/setting/"
        
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data:
                user_data = data['data']
                external_links = []
                
                # فحص الحقول المختلفة
                if user_data.get('google_account') or user_data.get('google_connected') or user_data.get('google_bind'):
                    external_links.append('google')
                if user_data.get('apple_account') or user_data.get('apple_connected') or user_data.get('apple_bind'):
                    external_links.append('apple')
                if user_data.get('facebook_account') or user_data.get('facebook_connected') or user_data.get('facebook_bind'):
                    external_links.append('facebook')
                if user_data.get('twitter_account') or user_data.get('twitter_connected') or user_data.get('twitter_bind'):
                    external_links.append('twitter')
                
                return external_links
        
        return []
        
    except Exception as e:
        print(f"خطأ في API البديل: {e}")
        return []

# ===== دالة Level =====
def info(username):
    """الحصول على ID من username"""
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Android 10; Pixel 3 Build/QKQ1.200308.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6394.70 Mobile Safari/537.36 trill_350402 JsSdk/1.0 NetType/MOBILE Channel/googleplay AppName/trill app_version/35.3.1 ByteLocale/en ByteFullLocale/en Region/IN AppId/1180 Spark/1.5.9.1 AppVersion/35.3.1 BytedanceWebview/d8a21c6",
    }
    try:
        tikinfo = requests.get(f'https://www.tiktok.com/@{username}', headers=headers).text
        info = str(tikinfo.split('webapp.user-detail"')[1]).split('"RecommenUserList"')[0]
        id = str(info.split('id":"')[1]).split('",')[0]
        return id
    except:
        return None

def sign(params, payload: str = None, sec_device_id: str = "", cookie: str or None = None, 
         aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "2.3.1.i18n", 
         sdk_version: int = 2, platform: int = 19, unix: int = None):
    """دالة التوقيع"""
    x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None
    data = payload
    if not unix: 
        unix = int(time.time())
    return Gorgon(params, unix, payload, cookie).get_value() | {
        "x-ladon": Ladon.encrypt(unix, license_id, aid),
        "x-argus": Argus.get_sign(
            params, x_ss_stub, unix,
            platform=platform,
            aid=aid,
            license_id=license_id,
            sec_device_id=sec_device_id,
            sdk_version=sdk_version_str,
            sdk_version_int=sdk_version
        )
    }

def get_level(username):
    """الحصول على Level"""
    try:
        id = info(username)
        if not id:
            return "غير متوفر"
        
        url = "https://webcast16-normal-no1a.tiktokv.eu/webcast/user/?request_from=profile_card_v2&request_from_scene=1&target_uid=" + str(id) + "&iid=" + str(random.randint(1, 10**19)) + "&device_id=" + str(random.randint(1, 10**19)) + "&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=300102&version_name=30.1.2&device_platform=android&os=android&ab_version=30.1.2&ssmix=a&device_type=RMX3511&device_brand=realme&language=ar&os_api=33&os_version=13&openudid=" + str(binascii.hexlify(os.urandom(8)).decode()) + "&manifest_version_code=2023001020&resolution=1080*2236&dpi=360&update_version_code=2023001020&_rticket=" + str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632" + "&current_region=IQ&app_type=normal&sys_region=IQ&mcc_mnc=41805&timezone_name=Asia%2FBaghdad&carrier_region_v2=418&residence=IQ&app_language=ar&carrier_region=IQ&ac2=wifi&uoo=0&op_region=IQ&timezone_offset=10800&build_number=30.1.2&host_abi=arm64-v8a&locale=ar&region=IQ&content_language=gu%2C&ts=" + str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "&cdid=" + str(uuid.uuid4()) + "&webcast_sdk_version=2920&webcast_language=ar&webcast_locale=ar_IQ"
        
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2023001020 (Linux; U; Android 13; ar; RMX3511; Build/TP1A.220624.014; Cronet/TTNetVersion:06d6a583 2023-04-17 QuicVersion:d298137e 2023-02-13)"
        }
        
        headers.update(sign(
            url.split('?')[1], 
            '', 
            "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), 
            None, 
            1233
        ))
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            match = re.search(r'"default_pattern":"(.*?)"', response.text)
            if match:
                level_value = match.group(1)
                # استخراج الرقم من النص إذا كان النص يحتوي على كلمات
                numbers = re.findall(r'\d+', level_value)
                if numbers:
                    return numbers[0]  # إرجاع الرقم فقط
                else:
                    return level_value  # إرجاع النص كما هو إذا لم يكن هناك أرقام
    except Exception as e:
        print(f"خطأ في الحصول على Level: {e}")
    
    return "غير متوفر"

# ===== دالة لتحديد رمز الدولة =====
def get_country_flag(phone_number):
    """الحصول على رمز الدولة بناءً على رقم الهاتف"""
    if not phone_number:
        return "🌍"
    
    phone = str(phone_number).replace('+', '')
    
    country_codes = {
        '966': '🇸🇦', '20': '🇪🇬', '971': '🇦🇪', '962': '🇯🇴', '973': '🇧🇭',
        '974': '🇶🇦', '965': '🇰🇼', '968': '🇴🇲', '212': '🇲🇦', '213': '🇩🇿',
        '216': '🇹🇳', '218': '🇱🇾', '964': '🇮🇶', '961': '🇱🇧', '963': '🇸🇾',
        '967': '🇾🇪', '249': '🇸🇩', '252': '🇸🇴', '253': '🇩🇯', '254': '🇰🇪',
        '255': '🇹🇿', '256': '🇺🇬', '257': '🇧🇮', '258': '🇲🇿', '260': '🇿🇲',
        '261': '🇲🇬', '262': '🇷🇪', '263': '🇿🇼', '264': '🇳🇦', '265': '🇲🇼',
        '266': '🇱🇸', '267': '🇧🇼', '268': '🇸🇿', '269': '🇰🇲', '27': '🇿🇦',
        '90': '🇹🇷', '91': '🇮🇳', '92': '🇵🇰', '93': '🇦🇫', '94': '🇱🇰',
        '95': '🇲🇲', '98': '🇮🇷', '992': '🇹🇯', '993': '🇹🇲', '994': '🇦🇿',
        '995': '🇬🇪', '996': '🇰🇬', '998': '🇺🇿', '1': '🇺🇸', '7': '🇷🇺',
        '33': '🇫🇷', '34': '🇪🇸', '39': '🇮🇹', '44': '🇬🇧', '49': '🇩🇪',
        '55': '🇧🇷', '86': '🇨🇳', '81': '🇯🇵', '82': '🇰🇷'
    }
    
    for code_length in [3, 2, 1]:
        if phone[:code_length] in country_codes:
            return country_codes[phone[:code_length]]
    
    return "🌍"

# ===== دالة فحص السيشن =====
def get_user_info(session_id):
    """دالة فحص السيشن"""
    # فحص نوع التطبيق أولاً
    app_type = check_app_type(session_id)
    
    # ثم الاستمرار بالفحص العادي
    cookies = {"sessionid": session_id}
    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2021306050 (Linux; U; Android 13; ar_IQ_#u-nu-latn; ANY-LX2; Build/HONORANY-L22CQ; Cronet/TTNetVersion:57844a4b 2019-10-16)',
        'X-Khronos': str(int(time.time())),
        'X-Gorgon': '0300100f040038a0761d2b67b399b05c32364fcc76f4faa0fb05',
    }
    
    try:
        res = requests.get(
            'https://api2.musical.ly/2/user/info/',
            params={
                'manifest_version_code': '2021306050',
                '_rticket': str(int(time.time() * 1000)),
                'app_language': 'ar',
                'app_type': 'normal',
                'iid': '7377748478723802885',
                'channel': 'googleplay',
                'device_type': 'ANY-LX2',
                'language': 'ar',
                'locale': 'ar',
                'resolution': '1080*2298',
                'openudid': '39e9b96bb5c6e336',
                'content_language': 'ar',
                'update_version_code': '2021306050',
                'ac2': 'wifi',
                'sys_region': 'IQ',
                'os_api': '33',
                'uoo': '0',
                'is_my_cn': '0',
                'timezone_name': 'Asia/Baghdad',
                'dpi': '480',
                'carrier_region': 'IQ',
                'ac': 'wifi',
                'pass-route': '1',
                'mcc_mnc': '41805',
                'os_version': '13',
                'timezone_offset': '10800',
                'version_code': '130605',
                'carrier_region_v2': '418',
                'app_name': 'musical_ly',
                'ab_version': '13.6.5',
                'version_name': '13.6.5',
                'device_brand': 'HONOR',
                'ssmix': 'a',
                'pass-region': '1',
                'device_platform': 'android',
                'build_number': '13.6.5',
                'region': 'ar',
                'aid': '1233',
                'ts': str(int(time.time()))
            },
            cookies=cookies,
            headers=headers,
            timeout=15
        ).json()
        
        if 'data' in res:
            data = res['data']
            
            username = data.get('username', 'غير معروف')
            screen_name = data.get('screen_name', '')
            user_id = data.get('user_id', '')
            email = data.get('email', '')
            phone = data.get('mobile', '')
            
            # الحصول على Level
            level = get_level(username)
            
            followers, likes = get_tiktok_stats_accurate(username)
            
            formatted_phone = "لا يوجد"
            country_flag = "🌍"
            if phone:
                country_flag = get_country_flag(phone)
                if len(phone) > 6:
                    formatted_phone = f"{country_flag} +{phone[:3]}****{phone[-4:]}"
                else:
                    formatted_phone = f"{country_flag} ****"
            
            if email and not phone:
                status = "📨 الحالة: مرتبط بريد فقط"
            elif phone and not email:
                status = "❄ الحالة: مرتبط رقم فقط"
            elif email and phone:
                status = "🧞‍♂️ الحالة: مرتبط بريد ورقم"
            else:
                status = "🌍 الحالة: غير مرتبط"
            
            # فحص الروبط الخارجية
            external_links = get_external_links(session_id)
            
            return {
                'success': True,
                'username': username,
                'screen_name': screen_name,
                'user_id': user_id,
                'email': email,
                'phone': phone,
                'formatted_phone': formatted_phone,
                'followers': followers,
                'likes': likes,
                'level': level,
                'status': status,
                'app_type': app_type,  # إضافة نوع التطبيق
                'external_links': external_links,  # إضافة الروبط الخارجية
                'session': session_id
            }
        else:
            return {'success': False, 'error': '❌ السيشن غير شغال'}
            
    except Exception as e:
        return {'success': False, 'error': f'❌ خطأ في الاتصال: {str(e)[:50]}'}

# ===== دالة الحصول على المتابعين والإعجابات =====
def get_tiktok_stats_accurate(username):
    """الحصول على عدد المتابعين والإعجابات بشكل دقيق"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
            'Referer': 'https://www.tiktok.com/',
            'Connection': 'keep-alive',
        }
        
        profile_url = f"https://www.tiktok.com/@{username}"
        response = requests.get(profile_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            
            followers_patterns = [
                r'"followerCount":\s*"([\d,]+)"',
                r'"followerCount":\s*([\d,]+)',
                r'data-e2e="followers-count"[^>]*>([\d,]+)',
                r'followersCount["\']?\s*:\s*["\']?([\d,]+)',
                r'([\d,]+)\s*متابع',
                r'([\d,]+)\s*Followers'
            ]
            
            likes_patterns = [
                r'"heartCount":\s*"([\d,]+)"',
                r'"heartCount":\s*([\d,]+)',
                r'data-e2e="likes-count"[^>]*>([\d,]+)',
                r'heartCount["\']?\s*:\s*["\']?([\d,]+)',
                r'([\d,]+)\s*إعجاب',
                r'([\d,]+)\s*Likes'
            ]
            
            followers = 0
            likes = 0
            
            for pattern in followers_patterns:
                match = re.search(pattern, html_content)
                if match:
                    try:
                        followers = int(match.group(1).replace(',', ''))
                        break
                    except:
                        continue
            
            for pattern in likes_patterns:
                match = re.search(pattern, html_content)
                if match:
                    try:
                        likes = int(match.group(1).replace(',', ''))
                        break
                    except:
                        continue
            
            return followers, likes
            
    except:
        pass
    
    return 0, 0

# ===== دالة إرسال ملف النتائج الكاملة =====
def send_full_results_file(chat_id, valid_results):
    """إرسال ملف النتائج الكاملة بالكليشة المطلوبة"""
    try:
        if not valid_results:
            return None
        
        file_content = "🎯 نتائج فحص حسابات TikTok\n"
        file_content += "="*60 + "\n\n"
        file_content += f"📊 عدد الحسابات الشغالة: {len(valid_results)}\n"
        file_content += f"⏰ وقت الإنشاء: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n\n"
        file_content += "="*60 + "\n\n"
        
        for i, result in enumerate(valid_results, 1):
            file_content += f"followers:{result['followers']}||like:{result['likes']}\n\n"
            file_content += f"{result['username']}\n"
            file_content += f"📛 الاسم: {result['screen_name'] if result['screen_name'] else 'غير معروف'}\n\n"
            file_content += f"{result['session']}\n"
            file_content += f"🆔 ايدي الحساب: {result['user_id']}\n"
            file_content += f"📧 البريد: {result['email'] if result['email'] else 'لا يوجد'}\n"
            file_content += f"{result['formatted_phone']}\n"
            file_content += f"{result['status']}\n"
            file_content += f"الـ ـفـل | {result['level']}\n"
            file_content += f"السيشن: {result['app_type']}\n"
            file_content += f"🔰 الربط الخرجي: {', '.join(result['external_links']) if result['external_links'] else 'لا يوجد'}\n"
            file_content += "-"*40 + "\n\n"
        
        timestamp = int(time.time())
        file_path = f"full_results_{chat_id}_{timestamp}.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        return file_path
        
    except Exception as e:
        print(f"خطأ في إنشاء الملف: {str(e)}")
        return None

# ===== متغيرات التخزين =====
processing_files = {}
user_results = {}

# ===== دالة معالجة الملف =====
def process_file_thread(file_path, chat_id):
    """معالجة الملف في خيط منفصل"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sessions_list = [line.strip() for line in f if line.strip()]
        
        total_sessions = len(sessions_list)
        
        processing_files[chat_id] = {
            'total': total_sessions,
            'processed': 0,
            'valid': 0,
            'invalid': 0,
            'start_time': time.time()
        }
        
        user_results[chat_id] = []
        
        bot.send_message(chat_id, f"""
<b>🚀 بدأ فحص {total_sessions} سيشن...</b>

📁 <b>عدد السيشنات:</b> {total_sessions}
⏳ <b>الحالة:</b> جاري المعالجة...
        """)
        
        for i, session in enumerate(sessions_list):
            processing_files[chat_id]['processed'] = i + 1
            
            result = get_user_info(session)
            
            if result['success']:
                result['session'] = session
                user_results[chat_id].append(result)
                processing_files[chat_id]['valid'] += 1
            else:
                processing_files[chat_id]['invalid'] += 1
            
            if (i + 1) % 100 == 0 or (i + 1) == total_sessions:
                progress = processing_files[chat_id]
                elapsed = time.time() - progress['start_time']
                
                progress_msg = f"""
<b>📊 تقدم الفحص:</b>

✅ معالج: {i + 1}/{total_sessions}
✅ شغال: {progress['valid']}
❌ غير شغال: {progress['invalid']}
⏱️ الوقت: {int(elapsed)} ثانية
                """
                bot.send_message(chat_id, progress_msg)
        
        if user_results[chat_id]:
            summary = f"""
<b>🎉 تم الانتهاء من الفحص!</b>

📁 <b>الإجمالي:</b> {total_sessions} سيشن
✅ <b>شغال:</b> {len(user_results[chat_id])}
❌ <b>غير شغال:</b> {processing_files[chat_id]['invalid']}

📤 <b>اضغط على زر 'إرسال الملفات' أدناه للحصول على ملف النتائج</b>
            """
            
            markup = types.InlineKeyboardMarkup()
            send_files_btn = types.InlineKeyboardButton(text='📤 إرسال الملفات', callback_data='send_files')
            markup.add(send_files_btn)
            
            bot.send_message(chat_id, summary, reply_markup=markup)
            
            example_count = min(3, len(user_results[chat_id]))
            for i in range(example_count):
                result = user_results[chat_id][i]
                
                result_text = f"""
<code>followers:{result['followers']}||like:{result['likes']}</code>

{result['username']}
📛 الاسم: {result['screen_name'] if result['screen_name'] else 'غير معروف'}

{result['session']}
🆔 ايدي الحساب: {result['user_id']}
📧 البريد: {result['email'] if result['email'] else 'لا يوجد'}
{result['formatted_phone']}
{result['status']}
الـ ـفـل | {result['level']}
السيشن: {result['app_type']}
🔰 الربط الخرجي: {', '.join(result['external_links']) if result['external_links'] else 'لا يوجد'}
                """
                
                markup = types.InlineKeyboardMarkup()
                acc_btn = types.InlineKeyboardButton(
                    text='🚀 دخول للحساب', 
                    url=f'https://tiktok.com/@{result["username"]}'
                )
                markup.add(acc_btn)
                
                bot.send_message(chat_id, result_text, reply_markup=markup)
            
            if len(user_results[chat_id]) > 3:
                bot.send_message(chat_id, 
                    f"<b>و {len(user_results[chat_id]) - 3} حسابات أخرى...</b>\n"
                    f"📤 <b>اضغط على 'إرسال الملفات' للحصول على جميع النتائج</b>"
                )
        else:
            bot.send_message(chat_id, "❌ <b>لم يتم العثور على أي سيشن شغال</b>")
        
        try:
            os.remove(file_path)
        except:
            pass
        
        if chat_id in processing_files:
            del processing_files[chat_id]
        
    except Exception as e:
        bot.send_message(chat_id, f"❌ خطأ في المعالجة: {str(e)[:100]}")

# ===== واجهة البوت =====
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    
    check_btn = types.InlineKeyboardButton(text='🔍 فحص سيشن', callback_data='check_session')
    file_btn = types.InlineKeyboardButton(text='📁 فحص ملف', callback_data='check_file')
    
    markup.add(check_btn, file_btn)
    
    welcome_text = f"""
<b>🎊 أهلاً وسهلاً بك {name}!</b>

<b>🤖 بوت فحص TikTok المتقدم</b>
<b>✏️ المبرمج: @I00EI ﴿  عبس  ﴾</b>

<b>⚡ كيفية الاستخدام:</b>

<u>1️⃣ فحص سيشن واحد:</u>
• أرسل sessionid للفحص

<u>2️⃣ فحص ملف سيشنات:</u>
• أرسل ملف txt يحتوي على السيشنات
• سطر واحد لكل سيشن

<b>📤 بعد الفحص:</b>
• سيظهر زر "إرسال الملفات" تلقائياً
• اضغط عليه لتحميل ملف النتائج الكاملة

<b>🎯 تنسيق الناتج:</b>
<code>followers:XXX||like:YYY</code>
<code>الـ ـفـل | XXX</code>
<code>السيشن: Web/iOS/Android</code>

<b>👉 اختر من الأزرار أدناه:</b>
    """
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    
    if call.data == 'check_session':
        bot.send_message(chat_id, 
            "🔑 <b>أرسل sessionid للفحص</b>\n\n"
            "⚡ <b>مثال:</b>\n"
            "1e9ef0c46bbe6b5f16233218542665c1\n\n"
            " <b>يدعم جميع أنواع التطبيقات:</b>\n"
            "• Android App\n"
            "• iOS App\n"
            "• Web\n"
            "• Studio\n"
            "• Lite")
    
    elif call.data == 'check_file':
        bot.send_message(chat_id, 
            "📁 <b>أرسل ملف txt بالسيشنات</b>\n\n"
            "⚡ <b>محتوى الملف:</b>\n"
            "• كل سيشن في سطر منفصل\n"
            "• مثال:\n"
            "session1\n"
            "session2\n"
            "session3\n\n"
            " <b>سيتم فحص نوع كل تطبيق تلقائياً</b>")
    
    elif call.data == 'send_files':
        if chat_id in user_results and user_results[chat_id]:
            bot.send_message(chat_id, "🔄 <b>جاري تحضير ملف النتائج...</b>")
            
            file_path = send_full_results_file(chat_id, user_results[chat_id])
            
            if file_path and os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    bot.send_document(
                        chat_id, 
                        f, 
                        caption=f"<b>📄 ملف النتائج الكاملة</b>\n\n"
                               f"📊 عدد الحسابات: {len(user_results[chat_id])}\n"
                               f"✏️ المبرمج: @I00EI ﴿  عبس  ﴾\n\n"
                               f"✅ بنفس تنسيق الكليشة المطلوبة\n"
                               f" مع إضافة نوع السيشن لكل حساب"
                    )
                
                try:
                    os.remove(file_path)
                except:
                    pass
                
                bot.send_message(chat_id, 
                    f"<b>✅ تم إرسال الملف بنجاح</b>\n\n"
                    f"📊 عدد الحسابات: {len(user_results[chat_id])}\n"
                    f"✏️ المبرمج: @I00EI ﴿  عبس  ﴾\n\n"
                    f"📁 يمكنك فحص ملف جديد أو سيشن آخر"
                )
            else:
                bot.send_message(chat_id, "❌ <b>خطأ في إنشاء الملف</b>")
        else:
            bot.send_message(chat_id, 
                "📭 <b>لا توجد نتائج متاحة</b>\n\n"
                "📁 أرسل ملف سيشنات أولاً لبدء الفحص\n"
                "✏️ المبرمج: @I00EI ﴿  عبس  ﴾"
            )

@bot.message_handler(content_types=['document'])
def handle_document(message):
    """معالجة ملف السيشنات"""
    if message.document.mime_type == 'text/plain' or message.document.file_name.endswith('.txt'):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        timestamp = int(time.time())
        file_path = f"temp_{message.chat.id}_{timestamp}.txt"
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            count = len(lines)
        
        if count == 0:
            bot.reply_to(message, "❌ <b>الملف فارغ</b>")
            os.remove(file_path)
            return
        
        bot.reply_to(message, f"""
<b>🚀 بدأ فحص {count} سيشن...</b>

📁 <b>عدد السيشنات:</b> {count}
✏️ <b>المبرمج:</b> @I00EI ﴿  عبس  ﴾
⏳ <b>الحالة:</b> جاري المعالجة...

⏱️ <b>سيتم إعلامك عند اكتمال الفحص</b>
📤 <b>سيظهر زر 'إرسال الملفات' بعد الانتهاء</b>
 <b>مع فحص نوع كل تطبيق تلقائياً</b>
        """)
        
        thread = Thread(target=process_file_thread, args=(file_path, message.chat.id))
        thread.start()
    
    else:
        bot.reply_to(message, "❌ <b>أرسل ملف txt فقط</b>\n✏️ المبرمج: @I00EI ﴿  عبس  ﴾")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    """فحص سيشن فردي"""
    text = message.text.strip()
    
    if len(text) > 20:
        bot.reply_to(message, "🔄 <b>جاري فحص السيشن...</b>\n✏️ المبرمج: @I00EI ﴿  عبس  ﴾")
        
        result = get_user_info(text)
        
        if result['success']:
            response = f"""
<code>followers:{result['followers']}||like:{result['likes']}</code>

{result['username']}
📛 الاسم: {result['screen_name'] if result['screen_name'] else 'غير معروف'}

{result['session']}
🆔 ايدي الحساب: {result['user_id']}
📧 البريد: {result['email'] if result['email'] else 'لا يوجد'}
{result['formatted_phone']}
{result['status']}
الـ ـفـل | {result['level']}
السيشن: {result['app_type']}
🔰 الربط الخرجي: {', '.join(result['external_links']) if result['external_links'] else 'لا يوجد'}
            """
            
            markup = types.InlineKeyboardMarkup()
            acc_btn = types.InlineKeyboardButton(
                text='🚀 دخول للحساب', 
                url=f'https://tiktok.com/@{result["username"]}'
            )
            markup.add(acc_btn)
            
            bot.send_message(message.chat.id, response, reply_markup=markup)
            
            if message.chat.id not in user_results:
                user_results[message.chat.id] = []
            
            result['session'] = text
            user_results[message.chat.id].append(result)
            
            if len(user_results[message.chat.id]) > 0:
                markup = types.InlineKeyboardMarkup()
                send_files_btn = types.InlineKeyboardButton(text='📤 إرسال الملفات', callback_data='send_files')
                markup.add(send_files_btn)
                
                bot.send_message(message.chat.id, 
                    f"<b>✅ تم حفظ النتيجة</b>\n"
                    f"📊 لديك الآن {len(user_results[message.chat.id])} نتيجة\n"
                    f"✏️ المبرمج: @I00EI ﴿  عبس  ﴾\n\n"
                    f"<b>اضغط على 'إرسال الملفات' لتحميل جميع النتائج</b>",
                    reply_markup=markup
                )
        else:
            bot.reply_to(message, 
                f"❌ <b>السيشن غير شغال:</b>\n\n{result['error']}\n"
                f"✏️ المبرمج: @I00EI ﴿  عبس  ﴾"
            )
    
    else:
        markup = types.InlineKeyboardMarkup()
        send_files_btn = types.InlineKeyboardButton(text='📤 إرسال الملفات', callback_data='send_files')
        markup.add(send_files_btn)
        
        bot.reply_to(message, 
            "<b>🎊 أهلاً وسهلاً بك!</b>\n\n"
            "<b>✏️ المبرمج: @I00EI ﴿  عبس  ﴾</b>\n\n"
            "<b>⚡ كيفية الاستخدام:</b>\n\n"
            "1️⃣ <b>لفحص سيشن واحد:</b>\n"
            "• أرسل sessionid للفحص\n\n"
            "2️⃣ <b>لفحص ملف سيشنات:</b>\n"
            "• أرسل ملف txt بالسيشنات\n\n"
            "<b>📤 بعد الفحص:</b>\n"
            "• سيظهر زر 'إرسال الملفات' تلقائياً\n"
            "• اضغط عليه لتحميل ملف النتائج\n\n"
            "<b>🎯 تنسيق الناتج:</b>\n"
            "<code>followers:XXX||like:YYY</code>\n"
            "<code>الـ ـفـل | XXX</code>\n"
            "<code> الـسيشن: Web/iOS/Android</code>",
            reply_markup=markup)

# ===== تشغيل البوت =====
if __name__ == "__main__":
    print("="*50)
    print("🤖 بوت فحص TikTok يعمل...")
    print("✏️ المبرمج: @I00EI ﴿  عبس  ﴾")
    print("✅ تم تعديل تنسيق الكليشة بنجاح")
    print("✅ تنسيق Level الجديد: 'الـ ـفـل | رقم'")
    print("✅ تم إضافة فحص نوع السيشن (Web/iOS/Android/Studio/Lite)")
    print("✅ تم إضافة فحص الروبط الخارجية (Google/Apple/Facebook/Twitter/Instagram)")
    print("="*50)
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")
        print("🔄 إعادة المحاولة بعد 5 ثواني...")
        time.sleep(5)
        os.execl(sys.executable, sys.executable, *sys.argv)
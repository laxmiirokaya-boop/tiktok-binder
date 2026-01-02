import json
import requests
import time
import uuid
import secrets
import string
from urllib.parse import urlencode
from flask import Flask, request, jsonify
from SignerPy import sign, ttencrypt, get
from hsopyt import Argus, Ladon, Gorgon, md5

app = Flask(__name__)

class TikTokBinder:
    def __init__(self):
        self.device_id = None
        self.install_id = None
        
    def initialize_device(self, proxy=None):
        pro = None
        if proxy:
            pro = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
        
        params = {
            "aid": "1233",
            "app_name": "musical_ly",
            "app_type": "normal",
            "channel": "googleplay",
            "device_platform": "android",
            "device_brand": "sony",
            "device_type": "SO-51A",
            "ssmix": "a",
            "version_code": "360505",
            "version_name": "36.5.5",
            "manifest_version_code": "2023605050",
            "update_version_code": "2023605050",
            "build_number": "36.5.5",
            "ab_version": "36.5.5",
            "language": "ar",
            "region": "IQ"
        }
        
        params.update(get(params))
        
        session = requests.Session()
        secret = secrets.token_hex(16)
        session.cookies.update({
            "passport_csrf_token": secret,
            "passport_csrf_token_default": secret
        })
        
        sig = sign(params=params, payload="", cookie="", version=4404, sdk_version=2)
        
        payload = ttencrypt.Enc().encrypt(data=json.dumps({
            "magic_tag": "ss_app_log",
            "header": {
                "display_name": "TikTok",
                "aid": 1233,
                "channel": "googleplay",
                "package": "com.zhiliaoapp.musically",
                "app_version": params["version_name"],
                "version_code": int(params["version_code"]),
                "sdk_version": "3.10.3-tiktok.1",
                "os": "Android",
                "os_version": "12",
                "device_model": params["device_type"],
                "device_brand": params["device_brand"],
                "cpu_abi": "arm64-v8a",
                "language": "ar",
                "access": "wifi",
                "mcc_mnc": "41820",
                "cdid": params.get("cdid", ""),
                "openudid": params.get("openudid", ""),
                "google_aid": str(uuid.uuid4()),
                "req_id": str(uuid.uuid4()),
                "region": "IQ",
                "tz_name": "Asia/Baghdad",
                "device_platform": "android",
                "apk_first_install_time": int(time.time()),
                "custom": {
                    "web_ua": f"Dalvik/2.1.0 (Linux; U; Android 14; {params['device_type']} Build/UP1A.231005.007)",
                    "priority_region": "IQ",
                    "dark_mode_setting_value": 1
                }
            },
            "_gen_time": int(time.time())
        }, separators=(',', ':')))
        
        headers = {
            "User-Agent": f"com.zhiliaoapp.musically/2023605050 (Linux; U; Android 14; ar_IQ; {params['device_type']}; Build/UP1A.231005.007)",
            "x-tt-passport-csrf-token": secret,
            "content-type": "application/octet-stream;tt-data=a",
        }
        headers.update(sig)
        
        request_params = {
            "tt_data": "a",
            "ac": "WIFI",
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "360505",
            "version_name": "36.5.5",
            "device_platform": "android",
            "os": "android",
            "ab_version": "36.5.5",
            "ssmix": "a",
            "language": "ar",
            "is_pad": "0",
            "app_type": "normal",
            "carrier_region_v2": "418",
            "app_language": "ar",
            "timezone_offset": "10800",
            "build_number": "36.5.5",
            "locale": "ar",
            "region": "IQ",
        }
        request_params.update(params)
        
        url = "https://log-boot.tiktokv.com/service/2/device_register/"
        response = session.post(url, params=request_params, data=payload, headers=headers, proxies=pro)
        
        try:
            data = response.json()
            self.device_id = data.get("device_id")
            self.install_id = data.get("install_id")
            if self.device_id and int(self.device_id) > 6:
                return True
        except Exception as e:
            print(f"Error initializing device: {e}")
        
        return False
    
    def signn(self, params: str, payload: str or None = None, sec_device_id: str = '',
              cookie: str or None = None, aid: int = 1233, license_id: int = 1611921764,
              sdk_version_str: str = 'v05.00.06-ov-android', sdk_version: int = 167775296,
              platform: int = 0, unix: float = None):
        x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None
        if not unix:
            unix = time.time()

        return Gorgon(params, unix, payload, cookie).get_value() | {
            'content-length': str(len(payload)),
            'x-ss-stub': x_ss_stub.upper(),
            'x-ladon': Ladon.encrypt(int(unix), license_id, aid),
            'x-argus': Argus.get_sign(
                params, x_ss_stub, int(unix),
                platform=platform,
                aid=aid,
                license_id=license_id,
                sec_device_id=sec_device_id,
                sdk_version=sdk_version_str,
                sdk_version_int=sdk_version
            )
        }
    
    def bind_without_verify(self, sessionid, email, proxy=None):
        if not self.device_id or not self.install_id:
            if not self.initialize_device(proxy):
                return {"status": "error", "message": "Failed to initialize device"}
        
        pro = None
        if proxy:
            pro = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
        
        url = "https://api22-normal-c-alisg.tiktokv.com/passport/email/bind_without_verify/"

        params = {
            "passport-sdk-version": "19",
            "iid": self.install_id,
            "device_id": self.device_id,
            "ac": "mobile",
            "ac2": "mobile",
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "310503",
            "version_name": "31.5.3",
            "ab_version": "31.5.3",
            "build_number": "31.5.3",
            "app_version": "31.5.3",
            "manifest_version_code": "2023105030",
            "update_version_code": "2023105030",
            "device_platform": "android",
            "os": "android",
            "os_api": "28",
            "os_version": "9",
            "device_type": "NE2211",
            "device_brand": "OnePlus",
            "host_abi": "arm64-v8a",
            "resolution": "900*1600",
            "dpi": "240",
            "openudid": "7a59d727a58ee91e",
            "language": "en",
            "app_language": "en",
            "locale": "en-GB",
            "content_language": "en,",
            "region": "GB",
            "sys_region": "US",
            "current_region": "TW",
            "op_region": "TW",
            "carrier_region": "TW",
            "carrier_region_v2": "466",
            "residence": "TW",
            "mcc_mnc": "46692",
            "timezone_name": "Asia/Baghdad",
            "timezone_offset": "10800",
            "_rticket": int(time.time() * 1000),
            "ts": int(time.time()),
            "app_type": "normal",
            "is_pad": "0",
            "uoo": "0",
            "support_webview": "1",
            "cronet_version": "2fdb62f9_2023-09-06",
            "ttnet_version": "4.2.152.11-tiktok",
            "use_store_region_cookie": "1",
            "cdid": str(uuid.uuid4()),
        }

        payload = {
            'account_sdk_source': 'app',
            'multi_login': '1',
            'email_source': '9',
            'email': email,
            'mix_mode': '1'
        }

        x_log1 = self.signn(urlencode(params), urlencode(payload),
                   "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)),
                   None, 1233)

        headers = {
            "User-Agent": "com.zhiliaoapp.musically/2023105030 (Linux; U; Android 9; en; OnePlus NE2211; Build/PKQ1.180716.001; Cronet/2fdb62f9 2023-09-06)",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": f"sessionid={sessionid}",
            "sdk-version": "2",
            "passport-sdk-version": "19",
            "x-ss-dp": "1233",
        }

        headers.update(x_log1)

        res = requests.post(url, params=params, data=payload, headers=headers, proxies=pro)
        
        try:
            return res.json()
        except:
            return {"status": "success", "response": res.text}

@app.route('/tiktok-bind', methods=['POST'])
def tiktok_bind():
    try:
        data = request.json
        
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        required_fields = ['email', 'sessionid']
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400
        
        email = data['email']
        sessionid = data['sessionid']
        proxy = data.get('proxy', '')
        by = data.get('by', '@is71s')
        
        binder = TikTokBinder()
        
        result = binder.bind_without_verify(sessionid, email, proxy if proxy else None)
        
        result['email'] = email
        result['by'] = by
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "TikTok Email Binder"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

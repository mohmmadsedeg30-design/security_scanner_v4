#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗   ║
║   ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗  ║
║   ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝  ║
║   ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗  ║
║   ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║  ║
║   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ║
║                                                                  ║
║        [ ETHICAL SECURITY SCANNER v4.0 - 2026 ]                  ║
║        "فحص آمن ← تعلم ← احمي"                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import json
import time
import sys
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════
# الألوان
# ═══════════════════════════════════════════════════════════════════
G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
C = "\033[96m"
B = "\033[94m"
M = "\033[95m"
W = "\033[97m"
D = "\033[2m"
RST = "\033[0m"
BLD = "\033[1m"

# ═══════════════════════════════════════════════════════════════════
# اللوجو
# ═══════════════════════════════════════════════════════════════════
LOGO = f"""
{C}{BLD}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ ║
    ║   ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗║
    ║   ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝║
    ║   ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗║
    ║   ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║║
    ║   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝║
    ║                                                               ║
    ║        [ ETHICAL SECURITY SCANNER v4.0 - 2026 ]               ║
    ║        "فحص آمن ← تعلم ← احمي"                                ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
{RST}"""

# ═══════════════════════════════════════════════════════════════════
# دوال مساعدة
# ═══════════════════════════════════════════════════════════════════
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def sep(char="─", color=C):
    print(f"{color}{char * 65}{RST}")

def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{R}[✗] ملف config.json غير موجود!{RST}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{R}[✗] ملف config.json تالف!{RST}")
        sys.exit(1)

def save_config(config):
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print(f"{G}[✓] تم الحفظ!{RST}")

def get_url(config):
    mode = config["server_settings"]["mode"]
    if mode == "local":
        return config["server_settings"]["local_url"]
    return config["server_settings"]["custom_url"]

# ═══════════════════════════════════════════════════════════════════
# تشغيل الفحص
# ═══════════════════════════════════════════════════════════════════
def run_scan():
    try:
        import requests
    except ImportError:
        print(f"{R}[✗] ثبّت requests: pip install requests{RST}")
        input(f"\n{Y}اضغط Enter...{RST}")
        return

    config = load_config()
    url = get_url(config)

    if not url:
        print(f"{R}[✗] لم يتم تحديد رابط! اذهب لإعدادات السيرفر.{RST}")
        input(f"\n{Y}اضغط Enter...{RST}")
        return

    accounts = config["targets"]["emails"] + config["targets"]["phones"]
    passwords = config["passwords_to_test"]
    settings = config.get("scan_settings", {})

    clear()
    print(LOGO)
    print(f"\n{BLD}{W}📊 معلومات الفحص:{RST}")
    print(f"   {C}• السيرفر:{RST} {url}")
    print(f"   {C}• الحسابات:{RST} {len(accounts)}")
    print(f"   {C}• كلمات المرور:{RST} {len(passwords)}")
    print(f"   {C}• إجمالي المحاولات:{RST} {len(accounts) * len(passwords)}")
    print(f"   {C}• التأخير:{RST} {settings.get('delay_between_requests', 0.4)}s")
    sep()
    time.sleep(1)

    results = {"success": [], "failed": [], "total": 0}
    delay = settings.get("delay_between_requests", 0.4)
    show_full = settings.get("show_full_response", False)

    for password in passwords:
        print(f"\n{M}{BLD}🔐 اختبار: [{password}]{RST}")
        sep("─", D)

        for account in accounts:
            payload = {
                "username": account,
                "password": password
            }

            try:
                response = requests.post(f"{url}/login", json=payload, timeout=10)
                res_data = response.json()
                ts = datetime.now().strftime("%H:%M:%S")
                results["total"] += 1

                if response.status_code == 200:
                    results["success"].append({
                        "account": account,
                        "password": password,
                        "time": ts
                    })
                    print(f"{G}[{ts}] ✅ نجاح! {BLD}{account}{RST}{G} ← {password}{RST}")
                else:
                    results["failed"].append({
                        "account": account,
                        "password": password,
                        "status": response.status_code,
                        "response": res_data.get("message", "")
                    })
                    if show_full:
                        print(f"{Y}[{ts}] ⚠️ فشل: {account} | {res_data.get('message', '')}{RST}")
                    else:
                        print(f"{Y}[{ts}] ⚠️ فشل: {account}{RST}")

            except requests.exceptions.ConnectionError:
                print(f"{R}[✗] السيرفر غير متصل!{RST}")
                input(f"\n{Y}اضغط Enter...{RST}")
                return
            except requests.exceptions.Timeout:
                print(f"{R}[✗] انتهت المهلة{RST}")
            except Exception as e:
                print(f"{R}[✗] خطأ: {e}{RST}")

            time.sleep(delay)

    sep("═", C)
    print(f"\n{BLD}{W}📋 الملخص:{RST}")
    print(f"   {G}✅ نجاح: {len(results['success'])}{RST}")
    print(f"   {Y}⚠️ فشل: {len(results['failed'])}{RST}")
    print(f"   {C}📊 إجمالي: {results['total']}{RST}")
    sep("═", C)

    if results["success"]:
        print(f"\n{G}{BLD}🔓 الحسابات المكتشفة:{RST}")
        for r in results["success"]:
            print(f"   {G}✓ {r['account']} : {r['password']} ({r['time']}){RST}")

    report = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"\n{C}💾 التقرير: {report}{RST}")

# ═══════════════════════════════════════════════════════════════════
# عرض الإعدادات
# ═══════════════════════════════════════════════════════════════════
def show_config():
    config = load_config()
    clear()
    print(LOGO)
    print(f"\n{BLD}{W}⚙️ الإعدادات:{RST}\n")

    print(f"{C}🌐 وضع السيرفر:{RST} {config['server_settings']['mode']}")
    print(f"{C}🔗 الرابط:{RST} {get_url(config)}")

    print(f"\n{C}📧 البريدات:{RST}")
    for e in config["targets"]["emails"]:
        print(f"   {D}→{RST} {e}")

    print(f"\n{C}📱 الأرقام:{RST}")
    for p in config["targets"]["phones"]:
        print(f"   {D}→{RST} {p}")

    print(f"\n{C}🔑 كلمات المرور:{RST}")
    for pwd in config["passwords_to_test"]:
        print(f"   {D}→{RST} {Y}{pwd}{RST}")

    settings = config.get("scan_settings", {})
    print(f"\n{C}⚡ إعدادات الفحص:{RST}")
    print(f"   {D}→{RST} تأخير: {settings.get('delay_between_requests', 0.4)}s")
    print(f"   {D}→{RST} عرض الرد الكامل: {'نعم' if settings.get('show_full_response') else 'لا'}")

# ═══════════════════════════════════════════════════════════════════
# تعديل الإعدادات
# ═══════════════════════════════════════════════════════════════════
def edit_config():
    config = load_config()

    while True:
        clear()
        print(LOGO)
        print(f"\n{BLD}{W}✏️ تعديل الإعدادات:{RST}\n")
        print(f"   {C}[1]{RST} تعديل البريدات الإلكترونية")
        print(f"   {C}[2]{RST} تعديل أرقام الهواتف")
        print(f"   {C}[3]{RST} تعديل كلمات المرور")
        print(f"   {C}[4]{RST} إعدادات السيرفر (محلي/مخصص)")
        print(f"   {C}[5]{RST} إعدادات الفحص (تأخير، عرض الرد)")
        print(f"   {C}[6]{RST} حفظ والعودة")

        sep("─", D)
        ch = input(f"\n{BLD}{Y}➤ اختيارك: {RST}").strip()

        if ch == "1":
            print(f"\n{Y}البريدات الحالية:{RST}")
            for i, e in enumerate(config["targets"]["emails"]):
                print(f"   [{i+1}] {e}")
            print(f"\n{G}أدخل البريدات الجديدة مفصولة بفواصل:{RST}")
            new = input("   > ").strip()
            if new:
                config["targets"]["emails"] = [x.strip() for x in new.split(",") if x.strip()]
                print(f"{G}✓ تم التحديث!{RST}")
                time.sleep(0.5)

        elif ch == "2":
            print(f"\n{Y}الأرقام الحالية:{RST}")
            for i, p in enumerate(config["targets"]["phones"]):
                print(f"   [{i+1}] {p}")
            print(f"\n{G}أدخل الأرقام الجديدة مفصولة بفواصل:{RST}")
            new = input("   > ").strip()
            if new:
                config["targets"]["phones"] = [x.strip() for x in new.split(",") if x.strip()]
                print(f"{G}✓ تم التحديث!{RST}")
                time.sleep(0.5)

        elif ch == "3":
            print(f"\n{Y}كلمات المرور الحالية:{RST}")
            for i, p in enumerate(config["passwords_to_test"]):
                print(f"   [{i+1}] {p}")
            print(f"\n{G}أدخل كلمات المرور الجديدة مفصولة بفواصل:{RST}")
            new = input("   > ").strip()
            if new:
                config["passwords_to_test"] = [x.strip() for x in new.split(",") if x.strip()]
                print(f"{G}✓ تم التحديث!{RST}")
                time.sleep(0.5)

        elif ch == "4":
            print(f"\n{Y}وضع السيرفر:{RST} {config['server_settings']['mode']}")
            print(f"{C}[1]{RST} محلي ({config['server_settings']['local_url']})")
            print(f"{C}[2]{RST} مخصص (رابط خارجي)")
            sm = input(f"\n{BLD}{Y}➤ اختيارك: {RST}").strip()
            if sm == "1":
                config["server_settings"]["mode"] = "local"
                print(f"{G}✓ تم التبديل للوضع المحلي{RST}")
            elif sm == "2":
                config["server_settings"]["mode"] = "custom"
                new_url = input(f"{G}أدخل الرابط الكامل (مثال: http://site.com:5000): {RST}").strip()
                if new_url:
                    config["server_settings"]["custom_url"] = new_url
                    print(f"{G}✓ تم التعيين: {new_url}{RST}")
            time.sleep(0.5)

        elif ch == "5":
            settings = config.get("scan_settings", {})
            print(f"\n{Y}الإعدادات الحالية:{RST}")
            print(f"   تأخير: {settings.get('delay_between_requests', 0.4)}s")
            print(f"   عرض الرد الكامل: {'نعم' if settings.get('show_full_response') else 'لا'}")

            try:
                d = input(f"\n{G}تأخير جديد (ثواني): {RST}").strip()
                if d: settings["delay_between_requests"] = float(d)

                f = input(f"{G}عرض الرد الكامل؟ (y/n): {RST}").strip().lower()
                if f: settings["show_full_response"] = (f == 'y')

                config["scan_settings"] = settings
                print(f"{G}✓ تم التحديث!{RST}")
            except:
                print(f"{R}✗ قيمة غير صالحة{RST}")
            time.sleep(0.5)

        elif ch == "6":
            save_config(config)
            time.sleep(1)
            break

        else:
            print(f"{R}✗ اختيار غير صالح{RST}")
            time.sleep(0.5)

# ═══════════════════════════════════════════════════════════════════
# فحص اتصال السيرفر
# ═══════════════════════════════════════════════════════════════════
def test_connection():
    try:
        import requests
    except ImportError:
        print(f"{R}[✗] ثبّت requests{RST}")
        input(f"\n{Y}اضغط Enter...{RST}")
        return

    config = load_config()
    url = get_url(config)

    if not url:
        print(f"{R}[✗] لم يتم تحديد رابط!{RST}")
        input(f"\n{Y}اضغط Enter...{RST}")
        return

    clear()
    print(LOGO)
    print(f"\n{BLD}{W}🔗 فحص الاتصال:{RST}\n")
    print(f"{D}الرابط: {url}{RST}\n")

    try:
        resp = requests.get(f"{url}/", timeout=10)
        data = resp.json()
        print(f"{G}✅ السيرفر متصل!{RST}")
        print(f"   {C}الحالة:{RST} {data.get('status', 'N/A')}")
        print(f"   {C}الإصدار:{RST} {data.get('version', 'N/A')}")
        print(f"   {C}الرسالة:{RST} {data.get('message', 'N/A')}")
    except requests.exceptions.ConnectionError:
        print(f"{R}[✗] السيرفر غير متصل!{RST}")
        print(f"{Y}   تأكد من تشغيل السيرفر أو صحة الرابط.{RST}")
    except Exception as e:
        print(f"{R}[✗] خطأ: {e}{RST}")

# ═══════════════════════════════════════════════════════════════════
# القائمة الرئيسية
# ═══════════════════════════════════════════════════════════════════
def main_menu():
    while True:
        clear()
        print(LOGO)

        config = load_config()
        url = get_url(config)
        mode_icon = "🏠" if config["server_settings"]["mode"] == "local" else "🌐"

        print(f"\n{BLD}{W}🎯 القائمة الرئيسية ({mode_icon} {config['server_settings']['mode']}){RST}")
        print(f"{D}   الرابط: {url}{RST}\n")

        print(f"   {C}[1]{RST} 🚀 تشغيل الفحص")
        print(f"   {C}[2]{RST} 📋 عرض الإعدادات")
        print(f"   {C}[3]{RST} ✏️ تعديل الإعدادات")
        print(f"   {C}[4]{RST} 🔗 فحص اتصال السيرفر")
        print(f"   {C}[5]{RST} 📖 دليل الاستخدام")
        print(f"   {C}[6]{RST} 🚪 الخروج")

        sep("─", D)
        choice = input(f"\n{BLD}{Y}➤ اختيارك (1-6): {RST}").strip()

        if choice == "1":
            run_scan()
            input(f"\n{Y}اضغط Enter للعودة...{RST}")
        elif choice == "2":
            show_config()
            input(f"\n{Y}اضغط Enter للعودة...{RST}")
        elif choice == "3":
            edit_config()
        elif choice == "4":
            test_connection()
            input(f"\n{Y}اضغط Enter للعودة...{RST}")
        elif choice == "5":
            clear()
            print(LOGO)
            guide = f"""
{BLD}{W}📖 دليل الاستخدام:{RST}

{C}1. التشغيل:{RST}
   Terminal 1: python3 server.py  (للسيرفر المحلي فقط)
   Terminal 2: python3 scanner.py

{C}2. تبديل السيرفر:{RST}
   [3] تعديل الإعدادات → [4] إعدادات السيرفر
   اختر [2] مخصص وأدخل رابط موقعك الآمن

{C}3. تعديل الأهداف:{RST}
   [3] تعديل الإعدادات → اختر البريدات/الأرقام/كلمات المرور
   أدخل القيم الجديدة مفصولة بفواصل

{C}4. إعدادات الفحص:{RST}
   [3] → [5] لتعديل التأخير بين الطلبات
   وعرض/إخفاء الردود الكاملة

{M}{BLD}⚠️ تنبيه أخلاقي:{RST}
   استخدم هذا السكربت فقط على مواقعك الخاصة
   أو مواقع لديك إذن صريح باختبارها.
"""
            print(guide)
            input(f"\n{Y}اضغط Enter للعودة...{RST}")
        elif choice == "6":
            print(f"\n{G}{BLD}✨ شكراً لاستخدامك السكربت! في أمان الله.{RST}\n")
            sys.exit(0)
        else:
            print(f"{R}[✗] اختيار غير صالح!{RST}")
            time.sleep(0.8)

# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Y}👋 تم الإيقاف.{RST}")
        sys.exit(0)

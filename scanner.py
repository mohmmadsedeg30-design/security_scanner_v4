import json
import time
import requests
import os
import sys
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

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "lab_info": {"name": "Nexus Security Suite", "version": "5.0", "author": "Nexus Team"},
            "server_settings": {"mode": "local", "local_url": "http://127.0.0.1:5000", "custom_url": "", "timeout": 5},
            "targets": {"emails": [], "phones": []},
            "passwords_to_test": ["123456", "password123"],
            "scan_settings": {"delay_between_requests": 0.5, "max_attempts": 10, "show_full_response": False, "verbose": True}
        }

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
{Colors.PURPLE}Professional Ethical Security Suite v5.0{Colors.END}
{Colors.DIM}--------------------------------------------------{Colors.END}
    """
    print(banner)

def main_menu():
    clear_screen()
    show_banner()
    print(f"{Colors.YELLOW}[ Main Menu ]{Colors.END}")
    print(f"{Colors.GREEN}[1]{Colors.END} Run Security Scan")
    print(f"{Colors.GREEN}[2]{Colors.END} Target Configuration")
    print(f"{Colors.GREEN}[3]{Colors.END} Server Settings")
    print(f"{Colors.GREEN}[4]{Colors.END} Scan Parameters")
    print(f"{Colors.RED}[0]{Colors.END} Exit")
    
    choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus > {Colors.END}")
    return choice

def run_scan():
    config = load_config()
    clear_screen()
    show_banner()
    
    url = config['server_settings']['local_url'] if config['server_settings']['mode'] == "local" else config['server_settings']['custom_url']
    
    if not url:
        print(f"{Colors.RED}[!] Error: No URL configured!{Colors.END}")
        time.sleep(2)
        return

    print(f"{Colors.YELLOW}Target URL: {Colors.CYAN}{url}{Colors.END}")
    print(f"{Colors.YELLOW}Starting Scan Sequence...{Colors.END}\n")
    
    emails = config['targets']['emails']
    phones = config['targets']['phones']
    all_targets = emails + phones
    passwords = config['passwords_to_test']
    
    if not all_targets:
        print(f"{Colors.RED}[!] No targets configured!{Colors.END}")
        time.sleep(2)
        return

    for target in all_targets:
        print(f"{Colors.BLUE}[*] Target: {Colors.WHITE}{target}{Colors.END}")
        for pwd in passwords:
            sys.stdout.write(f"    {Colors.DIM}Testing: {pwd}{Colors.END}\r")
            sys.stdout.flush()
            try:
                # Simulation of scanning logic
                time.sleep(config['scan_settings']['delay_between_requests'])
                # status = requests.post(f"{url}/login", json={"u": target, "p": pwd}, timeout=2).status_code
                # if status == 200: print(f"\n{Colors.GREEN}[+] FOUND: {target}:{pwd}{Colors.END}")
            except Exception as e:
                print(f"\n{Colors.RED}[!] Connection Error: {e}{Colors.END}")
                break
        print(f"\n{Colors.GREEN}[✓] Scan complete for {target}{Colors.END}\n")
    
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
        print(f"1. Mode: {Colors.CYAN}{config['server_settings']['mode']}{Colors.END}")
        print(f"2. Local URL: {Colors.CYAN}{config['server_settings']['local_url']}{Colors.END}")
        print(f"3. Custom URL: {Colors.CYAN}{config['server_settings']['custom_url']}{Colors.END}")
        print(f"0. Back")
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Nexus/Server > {Colors.END}")
        
        if choice == '1':
            config['server_settings']['mode'] = "local" if config['server_settings']['mode'] == "custom" else "custom"
        elif choice == '2':
            config['server_settings']['local_url'] = input("Enter Local URL: ")
        elif choice == '3':
            config['server_settings']['custom_url'] = input("Enter Custom URL: ")
        elif choice == '0':
            break
        save_config(config)

def start():
    while True:
        choice = main_menu()
        if choice == '1':
            run_scan()
        elif choice == '2':
            target_config()
        elif choice == '3':
            server_config()
        elif choice == '4':
            config = load_config()
            clear_screen()
            show_banner()
            print(f"{Colors.YELLOW}[ Scan Parameters ]{Colors.END}")
            delay = input(f"Current Delay ({config['scan_settings']['delay_between_requests']}s). New delay: ")
            if delay: config['scan_settings']['delay_between_requests'] = float(delay)
            save_config(config)
        elif choice == '0':
            print(f"{Colors.GREEN}Exiting Nexus...{Colors.END}")
            sys.exit()

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Session Terminated.{Colors.END}")
        sys.exit()

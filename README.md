# 🛡️ Nexus Password Spraying Lab v5.0

A professional, interactive, and highly customizable **Password Spraying** educational tool designed for security researchers and students.

## 📖 What is Password Spraying?
Password Spraying is a type of brute-force attack where a malicious actor attempts a small number of commonly used passwords against a large number of user accounts. Unlike traditional brute-force (which tries many passwords against one account), spraying avoids account lockouts by staying under the threshold of failed login attempts.

**This tool is built to simulate this technique in a controlled, ethical environment.**

## ✨ Features
- **Interactive UI**: Clean and colorful terminal interface (ANSI Colors).
- **Spray Engine**: Specifically designed to test common passwords across multiple targets.
- **ASCII Art**: Professional "NEXUS" startup banner.
- **Full Customization**: Modify target lists (emails, phones), password lists, and server settings directly from the menu.
- **Config Persistence**: All settings are saved in `config.json`.

## 📁 File Structure
| File | Description |
|-------|-------|
| `config.json` | Persistent configuration for targets and settings |
| `scanner.py` | Main Password Spraying engine |
| `server.py` | Local training server (Flask) to test your spray attacks |

## 🚀 Quick Start (Educational Lab)

### 1. Clone the repository
```bash
git clone https://github.com/mohmmadsedeg30-design/security_scanner_v4.git
cd security_scanner_v4
pip install flask requests
```

### 2. Run the Local Lab Server (Terminal 1)
```bash
python server.py
```

### 3. Run the Spraying Engine (Terminal 2)
```bash
python scanner.py
```
*Go to `Server Settings` -> `Switch to LOCAL Server`, then `Run Security Scan`.*

## ⚠️ Ethical Warning
This tool is for **educational purposes only**. Password spraying without explicit written permission is illegal and unethical. Use this only in labs, CTFs, or authorized penetration tests.

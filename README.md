# 🛡️ Nexus Password Spraying Lab v5.0

A professional, interactive, and highly customizable **Password Spraying** educational tool designed for security researchers and students.

## 📖 What is Password Spraying?
Password Spraying is a type of brute-force attack where a malicious actor attempts a small number of commonly used passwords against a large number of user accounts. Unlike traditional brute-force (which tries many passwords against one account), spraying avoids account lockouts by staying under the threshold of failed login attempts.

**This tool is built to simulate this technique in a controlled, ethical environment.**

## ✨ Features
- **High-Efficiency Engine**: Uses **Multi-threading** to test multiple targets simultaneously.
- **Stealth Mode**: Features **Random User-Agents** and **Smart Delays** to simulate human-like behavior and bypass simple rate limiting.
- **Interactive UI**: Clean and colorful terminal interface (ANSI Colors) with professional ASCII art.
- **Full Customization**: Easily manage targets, passwords, and server settings via the interactive menu.
- **Advanced Configuration**: Fine-tune threads, delays, and more directly from the app.

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

# 🛡️ Nexus Security Suite v5.0

A professional, interactive, and highly customizable ethical security scanner for educational and training purposes.

## ✨ Features
- **Interactive UI**: Clean and colorful terminal interface (ANSI Colors).
- **ASCII Art**: Professional startup banner.
- **Full Customization**: Modify targets (emails, phones), passwords, and server settings directly from the menu.
- **Flexible Modes**: Switch between local lab testing and custom remote targets.
- **Config Driven**: All settings are saved in `config.json` for persistence.

## 📁 File Structure
| File | Description |
|-------|-------|
| `config.json` | Persistent configuration for targets and settings |
| `scanner.py` | Main interactive scanner engine |
| `server.py` | Local training server (Flask) |

## 🚀 Installation & Usage

### 📱 Termux
```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/mohmmadsedeg30-design/security_scanner_v4.git
cd security_scanner_v4
pip install flask requests
python scanner.py
```

### 💻 Ubuntu
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
git clone https://github.com/mohmmadsedeg30-design/security_scanner_v4.git
cd security_scanner_v4
pip3 install flask requests
python3 scanner.py
```

## ⚙️ Customization
You can easily customize the tool via:
1. **Target Configuration**: Add/Remove emails, phones, and passwords.
2. **Server Settings**: Change target URLs and modes.
3. **Scan Parameters**: Adjust delays and verbose settings.

## ⚠️ Ethical Warning
This tool is for **educational purposes only**. Never use it on targets without explicit written permission.

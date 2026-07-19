#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     ETHICAL SECURITY SCANNER - TARGET SERVER v4.0              ║
║     سيرفر هدف بسيط للتدريب الأخلاقي                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# قاعدة بيانات وهمية
VALID_ACCOUNTS = {
    "admin@example.com": "Welcome@2026",
    "user1@test.com": "password123",
    "+966500000002": "admin2026"
}

@app.route('/')
def home():
    return jsonify({
        "status": "ONLINE",
        "version": "4.0",
        "message": "🎯 Target Server - Ethical Scanner Lab"
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if username in VALID_ACCOUNTS and VALID_ACCOUNTS[username] == password:
        return jsonify({
            "status": "SUCCESS",
            "message": f"✅ Access Granted: {username}",
            "timestamp": time.strftime("%H:%M:%S")
        }), 200
    else:
        return jsonify({
            "status": "FAILED",
            "message": "❌ Invalid Credentials"
        }), 401

if __name__ == '__main__':
    print("\n" + "="*55)
    print("  🎯 TARGET SERVER - Ethical Scanner Lab v4.0")
    print("  🚀 http://127.0.0.1:5000")
    print("="*55 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=False)

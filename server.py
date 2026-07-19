from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Mock Database for testing (Matches default config.json)
VALID_CREDENTIALS = {
    "admin@example.com": "password123",
    "security@internal.net": "admin@2024",
    "test-user@nexus.io": "nexus_secure",
    "+1234567890": "123456"
}

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Nexus Local Training Server is running!",
        "version": "5.0"
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    
    # Simulate processing delay
    time.sleep(0.1)
    
    if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
        return jsonify({
            "status": "success",
            "message": f"Welcome back, {username}!",
            "token": "mock-session-token-12345"
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid credentials. Access Denied."
        }), 401

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  NEXUS LOCAL TRAINING SERVER v5.0")
    print("  Running on: http://127.0.0.1:5000")
    print("  Endpoints: /login [POST]")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000)

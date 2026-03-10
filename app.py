from flask import Flask, jsonify
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Hello from CI/CD Pipeline!",
        "app": "n8n Demo App",
        "version": "1.0.0",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "environment": os.getenv("ENVIRONMENT", "development")
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

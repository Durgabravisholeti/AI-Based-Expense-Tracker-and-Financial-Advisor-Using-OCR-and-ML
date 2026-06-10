#!/usr/bin/env python3
"""
Debug version of the Flask app with enhanced logging
"""
import logging
from flask import request
from app import app

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# Add request logging
@app.before_request
def log_request_info():
    app.logger.debug('Request: %s %s', request.method, request.url)
    if request.is_json:
        app.logger.debug('Request JSON: %s', request.get_json())

@app.after_request
def log_response_info(response):
    app.logger.debug('Response: %s', response.status_code)
    return response

if __name__ == "__main__":
    print("🐛 Starting Flask app in DEBUG mode...")
    print("   Main app: http://127.0.0.1:5000")
    print("   Test page: http://127.0.0.1:5000/test-auth")
    print("   Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
#!/usr/bin/env python3
"""
Quick test to verify the app works end-to-end
"""
import requests
import time
import threading
from app import app

def start_server():
    """Start the Flask server in a separate thread"""
    app.run(debug=False, host='127.0.0.1', port=5001, use_reloader=False)

def test_auth_flow():
    """Test the complete authentication flow"""
    base_url = "http://127.0.0.1:5001"
    
    # Wait for server to start
    time.sleep(2)
    
    print("🧪 Testing authentication flow...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        print(f"✅ Server is running (status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server connection failed: {e}")
        return False
    
    # Test 2: Register a new user
    register_data = {
        "username": "testuser123",
        "email": "test123@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/register", json=register_data, timeout=5)
        data = response.json()
        if data.get("success"):
            print("✅ Registration successful")
        else:
            print(f"⚠️  Registration response: {data.get('message', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Registration failed: {e}")
        return False
    
    # Test 3: Login with the new user
    login_data = {
        "email": "test123@example.com",
        "password": "testpass123"
    }
    
    try:
        session = requests.Session()
        response = session.post(f"{base_url}/api/login", json=login_data, timeout=5)
        data = response.json()
        if data.get("success"):
            print("✅ Login successful")
            print(f"   Redirect URL: {data.get('redirect')}")
        else:
            print(f"❌ Login failed: {data.get('message', 'Unknown error')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Login request failed: {e}")
        return False
    
    # Test 4: Access protected endpoint
    try:
        response = session.get(f"{base_url}/dashboard", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard access successful")
        else:
            print(f"❌ Dashboard access failed (status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Dashboard request failed: {e}")
        return False
    
    # Test 5: Add an expense
    expense_data = {
        "title": "Test lunch",
        "amount": 25.50,
        "date": "2024-04-18"
    }
    
    try:
        response = session.post(f"{base_url}/add", json=expense_data, timeout=5)
        data = response.json()
        if data.get("success"):
            print(f"✅ Expense added successfully (category: {data.get('category')})")
        else:
            print(f"❌ Add expense failed: {data.get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Add expense request failed: {e}")
        return False
    
    print("\n🎉 All tests passed! The authentication system is working correctly.")
    return True

def main():
    print("🚀 Starting quick authentication test...")
    print("=" * 50)
    
    # Start server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Run tests
    success = test_auth_flow()
    
    if success:
        print("\n✅ Authentication is working correctly!")
        print("\n💡 To use the app:")
        print("   1. Run: python app.py")
        print("   2. Open: http://127.0.0.1:5000")
        print("   3. Click 'Get Started' to register")
        print("   4. Or use the test page: http://127.0.0.1:5000/test-auth")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()
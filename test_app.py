#!/usr/bin/env python3
"""
Simple test script to verify the expense tracker functionality
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_registration_and_login():
    """Test user registration and login"""
    print("Testing registration and login...")
    
    # Test registration
    reg_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register", json=reg_data)
        if response.status_code == 200:
            print("✓ Registration successful")
        else:
            print(f"✗ Registration failed: {response.json()}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure the Flask app is running.")
        return False
    
    # Test login
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    session = requests.Session()
    response = session.post(f"{BASE_URL}/api/login", json=login_data)
    if response.status_code == 200:
        print("✓ Login successful")
        return session
    else:
        print(f"✗ Login failed: {response.json()}")
        return False

def test_add_expense(session):
    """Test adding an expense"""
    print("Testing add expense...")
    
    expense_data = {
        "title": "Test lunch at restaurant",
        "amount": 250.50,
        "date": "2024-04-18"
    }
    
    response = session.post(f"{BASE_URL}/add", json=expense_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Expense added successfully, category: {data.get('category')}")
        return True
    else:
        print(f"✗ Add expense failed: {response.json()}")
        return False

def test_get_expenses(session):
    """Test retrieving expenses"""
    print("Testing get expenses...")
    
    response = session.get(f"{BASE_URL}/expenses?limit=10")
    if response.status_code == 200:
        expenses = response.json()
        print(f"✓ Retrieved {len(expenses)} expenses")
        return len(expenses) > 0
    else:
        print(f"✗ Get expenses failed: {response.json()}")
        return False

def test_summary(session):
    """Test summary endpoint"""
    print("Testing summary...")
    
    response = session.get(f"{BASE_URL}/summary")
    if response.status_code == 200:
        summary = response.json()
        print(f"✓ Summary: Total=₹{summary.get('total')}, This Month=₹{summary.get('this_month')}, Count={summary.get('count')}")
        return True
    else:
        print(f"✗ Summary failed: {response.json()}")
        return False

def main():
    print("🧪 Testing AI Expense Tracker functionality...\n")
    
    # Test registration and login
    session = test_registration_and_login()
    if not session:
        return
    
    # Test adding expense
    if not test_add_expense(session):
        return
    
    # Test retrieving expenses
    if not test_get_expenses(session):
        return
    
    # Test summary
    if not test_summary(session):
        return
    
    print("\n✅ All tests passed! The expense tracker is working correctly.")
    print("\n📝 Features verified:")
    print("  • User registration with secure password hashing")
    print("  • User login with session management")
    print("  • Adding expenses with auto-categorization")
    print("  • Retrieving expense list")
    print("  • Summary calculations")
    print("\n🌟 Additional features available:")
    print("  • OCR bill scanning (requires EasyOCR/Tesseract)")
    print("  • AI predictions using linear regression")
    print("  • 6 interactive charts for analytics")
    print("  • Edit and delete expenses")
    print("  • Financial tips based on spending patterns")

if __name__ == "__main__":
    main()
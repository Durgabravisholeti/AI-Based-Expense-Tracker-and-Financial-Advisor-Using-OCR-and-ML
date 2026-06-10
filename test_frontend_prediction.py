#!/usr/bin/env python3
"""
Frontend Prediction Test - Complete Test Suite
This script will test the prediction functionality end-to-end
"""

import sqlite3
import subprocess
import sys
import time
import webbrowser
from datetime import datetime, timedelta

def setup_test_data():
    """Add comprehensive test data across multiple months"""
    print("🗄️ Setting up test data...")
    
    conn = sqlite3.connect('expenses.db')
    
    # Clear existing test data
    conn.execute('DELETE FROM expenses WHERE user_id IN (SELECT id FROM users WHERE email LIKE "%test%")')
    conn.execute('DELETE FROM users WHERE email LIKE "%test%"')
    
    # Create test user
    from werkzeug.security import generate_password_hash
    test_email = "test@prediction.com"
    test_password = generate_password_hash("test123")
    
    conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', 
                (test_email, test_password))
    
    user_id = conn.lastrowid
    
    # Add expenses across 4 months with realistic data
    base_date = datetime(2024, 1, 1)
    expenses = []
    
    # January 2024
    expenses.extend([
        ("Groceries", 1500, "Food", "2024-01-05"),
        ("Restaurant", 800, "Food", "2024-01-12"),
        ("Bills", 2000, "Bills", "2024-01-15"),
        ("Shopping", 1200, "Shopping", "2024-01-20"),
        ("Coffee", 300, "Food", "2024-01-25"),
    ])
    
    # February 2024
    expenses.extend([
        ("Groceries", 1600, "Food", "2024-02-03"),
        ("Utilities", 1800, "Bills", "2024-02-10"),
        ("Movie", 500, "Entertainment", "2024-02-14"),
        ("Gas", 700, "Transport", "2024-02-18"),
        ("Dinner", 900, "Food", "2024-02-22"),
    ])
    
    # March 2024
    expenses.extend([
        ("Groceries", 1700, "Food", "2024-03-02"),
        ("Internet", 1000, "Bills", "2024-03-08"),
        ("Clothes", 2500, "Shopping", "2024-03-15"),
        ("Taxi", 400, "Transport", "2024-03-20"),
        ("Lunch", 600, "Food", "2024-03-28"),
    ])
    
    # April 2024
    expenses.extend([
        ("Groceries", 1800, "Food", "2024-04-05"),
        ("Phone Bill", 800, "Bills", "2024-04-10"),
        ("Books", 1200, "Education", "2024-04-15"),
        ("Coffee", 350, "Food", "2024-04-22"),
    ])
    
    # Insert all expenses
    for title, amount, category, date in expenses:
        conn.execute('''INSERT INTO expenses (user_id, title, amount, category, date) 
                       VALUES (?, ?, ?, ?, ?)''', 
                    (user_id, title, amount, category, date))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Added {len(expenses)} expenses across 4 months")
    print(f"📧 Test user: {test_email}")
    print(f"🔑 Password: test123")
    
    return test_email

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Flask server...")
    try:
        # Start server in background
        process = subprocess.Popen([sys.executable, 'app.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server is running
        if process.poll() is None:
            print("✅ Server started successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return None

def main():
    print("🔮 Frontend Prediction Test Suite")
    print("=" * 50)
    
    # Setup test data
    test_email = setup_test_data()
    
    # Start server
    server_process = start_server()
    
    if server_process:
        print("\n🌐 Opening browser...")
        print("📋 Test Instructions:")
        print("1. Login with:")
        print(f"   📧 Email: {test_email}")
        print(f"   🔑 Password: test123")
        print("2. Go to 'AI Advisor' section (robot icon)")
        print("3. Click 'Predict Next Month' button")
        print("4. You should see a prediction result")
        print("\n🔍 If it doesn't work:")
        print("• Press F12 and check Console tab for errors")
        print("• Check Network tab for failed requests")
        print("• Make sure you're logged in")
        
        # Open browser
        webbrowser.open('http://127.0.0.1:5000')
        
        print("\n⏳ Server is running... Press Ctrl+C to stop")
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            server_process.terminate()
            server_process.wait()
            print("✅ Server stopped")
    else:
        print("❌ Could not start server. Please run manually:")
        print("   python app.py")

if __name__ == "__main__":
    main()
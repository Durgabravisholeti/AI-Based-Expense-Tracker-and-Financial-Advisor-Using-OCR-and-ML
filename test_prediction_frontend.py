#!/usr/bin/env python3
"""
Test the prediction functionality from frontend perspective
"""
import webbrowser
import threading
import time
import sqlite3
import datetime
from app import app

def add_sample_expenses():
    """Add sample expenses to test prediction"""
    print("📊 Adding sample expenses for testing...")
    
    try:
        conn = sqlite3.connect("expenses.db")
        
        # Check if we have a test user
        user = conn.execute("SELECT id FROM users WHERE email = 'test@example.com'").fetchone()
        
        if not user:
            print("⚠️  No test user found. Please register first.")
            conn.close()
            return False
        
        user_id = user[0]
        
        # Add sample expenses across multiple months
        sample_expenses = [
            # January 2024
            ("Grocery shopping", 1500.0, "Food", "2024-01-15"),
            ("Restaurant dinner", 800.0, "Food", "2024-01-20"),
            ("Gas bill", 2200.0, "Bills", "2024-01-25"),
            
            # February 2024
            ("Coffee shop", 300.0, "Food", "2024-02-10"),
            ("Electricity bill", 1800.0, "Bills", "2024-02-15"),
            ("Grocery shopping", 1200.0, "Food", "2024-02-28"),
            
            # March 2024
            ("Restaurant lunch", 450.0, "Food", "2024-03-05"),
            ("Internet bill", 1100.0, "Bills", "2024-03-15"),
            ("Grocery shopping", 1400.0, "Food", "2024-03-22"),
            
            # April 2024
            ("Coffee and snacks", 250.0, "Food", "2024-04-08"),
            ("Utility bills", 2500.0, "Bills", "2024-04-18"),
            ("Grocery shopping", 1300.0, "Food", "2024-04-25"),
        ]
        
        # Insert sample expenses
        for title, amount, category, date in sample_expenses:
            conn.execute(
                "INSERT INTO expenses (user_id, title, amount, category, date) VALUES (?, ?, ?, ?, ?)",
                (user_id, title, amount, category, date)
            )
        
        conn.commit()
        conn.close()
        
        print(f"✅ Added {len(sample_expenses)} sample expenses")
        return True
        
    except Exception as e:
        print(f"❌ Error adding sample expenses: {e}")
        return False

def start_server():
    """Start the Flask server"""
    app.run(debug=False, host='127.0.0.1', port=5003, use_reloader=False)

def main():
    print("🔮 Testing Prediction Frontend")
    print("=" * 50)
    
    # Add sample expenses
    add_sample_expenses()
    
    # Start server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    print("✅ Server started successfully")
    print("🌐 Opening browser...")
    
    # Open browser to the app
    webbrowser.open("http://127.0.0.1:5003")
    
    print("\n🧪 Testing Steps:")
    print("1. ✅ Register/Login with email: test@example.com")
    print("2. ✅ Go to AI Advisor section (robot icon in sidebar)")
    print("3. ✅ Click 'Predict Next Month' button")
    print("4. ✅ You should see a prediction like: ₹2,500.00")
    print("5. ✅ Check the trend (increasing/decreasing/stable)")
    
    print("\n🔍 What to check if it's not working:")
    print("• Open browser console (F12) and check for JavaScript errors")
    print("• Make sure you're logged in")
    print("• Check if the AI Advisor section is visible")
    print("• Verify the 'Predict Next Month' button exists")
    print("• Look for network errors in the Network tab")
    
    print("\n📊 Expected Result:")
    print("• Predicted amount: Around ₹2,000-3,000")
    print("• Trend: Should show increasing/decreasing/stable")
    print("• Message: 'Based on X months of data'")
    
    print(f"\n🌍 URL: http://127.0.0.1:5003")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Keep the server running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    main()
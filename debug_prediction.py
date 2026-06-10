#!/usr/bin/env python3
"""
Debug script to test the prediction functionality
"""
import sqlite3
import datetime
from model import predict_next_month

def test_prediction_with_sample_data():
    """Test prediction with sample expense data"""
    print("🧪 Testing Prediction Functionality")
    print("=" * 50)
    
    # Sample expense data spanning multiple months
    sample_expenses = [
        {"amount": 1500.0, "date": "2024-01-15"},
        {"amount": 800.0, "date": "2024-01-20"},
        {"amount": 2200.0, "date": "2024-01-25"},
        
        {"amount": 1800.0, "date": "2024-02-10"},
        {"amount": 950.0, "date": "2024-02-18"},
        {"amount": 1200.0, "date": "2024-02-28"},
        
        {"amount": 2100.0, "date": "2024-03-05"},
        {"amount": 1100.0, "date": "2024-03-15"},
        {"amount": 1400.0, "date": "2024-03-22"},
        
        {"amount": 2500.0, "date": "2024-04-08"},
        {"amount": 1300.0, "date": "2024-04-18"},
    ]
    
    print(f"📊 Sample data: {len(sample_expenses)} expenses across 4 months")
    
    # Test prediction
    result = predict_next_month(sample_expenses)
    
    print("\n🔮 Prediction Result:")
    print(f"   Predicted amount: ₹{result.get('predicted', 0)}")
    print(f"   Trend: {result.get('trend', 'unknown')}")
    print(f"   Months used: {result.get('months_used', 0)}")
    print(f"   Message: {result.get('message', 'No message')}")
    
    return result

def test_prediction_with_user_data():
    """Test prediction with actual user data from database"""
    print("\n🗄️ Testing with actual database data...")
    
    try:
        conn = sqlite3.connect("expenses.db")
        conn.row_factory = sqlite3.Row
        
        # Get all expenses from database
        rows = conn.execute("SELECT amount, date FROM expenses").fetchall()
        expenses = [dict(r) for r in rows]
        
        print(f"📊 Found {len(expenses)} expenses in database")
        
        if not expenses:
            print("⚠️  No expenses found in database")
            return None
        
        # Show sample of data
        print("\n📋 Sample expenses:")
        for i, exp in enumerate(expenses[:5]):
            print(f"   {i+1}. ₹{exp['amount']} on {exp['date']}")
        if len(expenses) > 5:
            print(f"   ... and {len(expenses) - 5} more")
        
        # Test prediction
        result = predict_next_month(expenses)
        
        print("\n🔮 Prediction Result:")
        print(f"   Predicted amount: ₹{result.get('predicted', 0)}")
        print(f"   Trend: {result.get('trend', 'unknown')}")
        print(f"   Months used: {result.get('months_used', 0)}")
        print(f"   Message: {result.get('message', 'No message')}")
        
        conn.close()
        return result
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None

def test_edge_cases():
    """Test prediction with edge cases"""
    print("\n🧪 Testing edge cases...")
    
    # Test 1: No data
    result1 = predict_next_month([])
    print(f"✅ No data: {result1.get('message', 'No message')}")
    
    # Test 2: Single month data
    single_month = [
        {"amount": 1000.0, "date": "2024-04-15"},
        {"amount": 500.0, "date": "2024-04-20"},
    ]
    result2 = predict_next_month(single_month)
    print(f"✅ Single month: {result2.get('message', 'No message')}")
    
    # Test 3: Invalid date format
    invalid_data = [
        {"amount": 1000.0, "date": "invalid-date"},
        {"amount": 500.0, "date": "2024-04-20"},
    ]
    result3 = predict_next_month(invalid_data)
    print(f"✅ Invalid date: {result3.get('message', 'No message')}")

def test_api_endpoint():
    """Test the actual API endpoint"""
    print("\n🌐 Testing API endpoint...")
    
    try:
        import requests
        
        # This would require authentication, so we'll just test if server is running
        response = requests.get("http://127.0.0.1:5000/", timeout=2)
        if response.status_code == 200:
            print("✅ Server is running")
            print("💡 To test prediction API:")
            print("   1. Start the app: python app.py")
            print("   2. Login to the app")
            print("   3. Go to AI Advisor section")
            print("   4. Click 'Predict Next Month'")
        else:
            print("⚠️  Server responded but may have issues")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server not running")
        print("💡 Start the server with: python app.py")
    except ImportError:
        print("⚠️  Requests library not available")
        print("💡 Install with: pip install requests")

def main():
    print("🔮 AI Prediction Debug Tool")
    print("=" * 50)
    
    # Test with sample data
    sample_result = test_prediction_with_sample_data()
    
    # Test with actual database data
    db_result = test_prediction_with_user_data()
    
    # Test edge cases
    test_edge_cases()
    
    # Test API endpoint
    test_api_endpoint()
    
    print("\n" + "=" * 50)
    print("🎯 Summary:")
    
    if sample_result and sample_result.get('predicted', 0) > 0:
        print("✅ Prediction algorithm works correctly")
    else:
        print("❌ Prediction algorithm may have issues")
    
    if db_result:
        if db_result.get('predicted', 0) > 0:
            print("✅ Database integration works")
        else:
            print("⚠️  Database has insufficient data for prediction")
    else:
        print("❌ Database integration failed")
    
    print("\n💡 Troubleshooting tips:")
    print("   • Make sure you have at least 2 months of expense data")
    print("   • Check that expenses have valid dates")
    print("   • Ensure you're logged in when testing the web interface")
    print("   • Check browser console for JavaScript errors")

if __name__ == "__main__":
    main()
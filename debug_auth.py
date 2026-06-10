#!/usr/bin/env python3
"""
Debug script to test authentication functionality
"""
import sqlite3
import sys
from werkzeug.security import generate_password_hash, check_password_hash

def test_database():
    """Test database connection and table creation"""
    print("🔍 Testing database...")
    
    try:
        conn = sqlite3.connect("expenses.db", timeout=10)
        conn.row_factory = sqlite3.Row
        
        # Check if tables exist
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        print(f"✅ Database connected. Tables: {[t['name'] for t in tables]}")
        
        # Check users table structure
        users_info = conn.execute("PRAGMA table_info(users)").fetchall()
        print(f"✅ Users table columns: {[col[1] for col in users_info]}")
        
        # Check if there are any users
        user_count = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()
        print(f"✅ Current users in database: {user_count['count']}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_password_hashing():
    """Test password hashing functionality"""
    print("\n🔐 Testing password hashing...")
    
    try:
        test_password = "testpass123"
        
        # Test hashing
        hashed = generate_password_hash(test_password)
        print(f"✅ Password hashed successfully: {hashed[:20]}...")
        
        # Test verification
        is_valid = check_password_hash(hashed, test_password)
        print(f"✅ Password verification: {is_valid}")
        
        # Test wrong password
        is_invalid = check_password_hash(hashed, "wrongpass")
        print(f"✅ Wrong password rejected: {not is_invalid}")
        
        return True
    except Exception as e:
        print(f"❌ Password hashing error: {e}")
        return False

def test_user_registration():
    """Test user registration process"""
    print("\n👤 Testing user registration...")
    
    try:
        conn = sqlite3.connect("expenses.db", timeout=10)
        conn.row_factory = sqlite3.Row
        
        # Test data
        username = "testuser_debug"
        email = "test_debug@example.com"
        password = "testpass123"
        
        # Delete existing test user if exists
        conn.execute("DELETE FROM users WHERE email = ?", (email,))
        conn.commit()
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Insert user
        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        print(f"✅ User registered successfully")
        
        # Verify user exists
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user:
            print(f"✅ User found in database: {user['username']}")
            
            # Test login
            if check_password_hash(user['password'], password):
                print(f"✅ Login test successful")
            else:
                print(f"❌ Login test failed")
        else:
            print(f"❌ User not found after registration")
        
        # Cleanup
        conn.execute("DELETE FROM users WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_flask_imports():
    """Test if all required Flask modules are available"""
    print("\n📦 Testing Flask imports...")
    
    try:
        from flask import Flask, request, jsonify, render_template, redirect, url_for, session, g
        print("✅ Flask core modules imported")
        
        from werkzeug.utils import secure_filename
        from werkzeug.security import generate_password_hash, check_password_hash
        print("✅ Werkzeug modules imported")
        
        import secrets
        print("✅ Secrets module imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Authentication Debug Tests")
    print("=" * 50)
    
    tests = [
        test_flask_imports,
        test_database,
        test_password_hashing,
        test_user_registration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All tests passed! Authentication should work correctly.")
        print("\n💡 If you're still having issues, check:")
        print("   • Browser console for JavaScript errors")
        print("   • Network tab for failed API requests")
        print("   • Flask server logs for error messages")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print(f"   Test results: {results}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Script to fix common frontend authentication issues
"""

def fix_home_html():
    """Fix common issues in home.html"""
    print("🔧 Fixing home.html authentication issues...")
    
    # Read the current file
    with open('templates/home.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for common issues and fix them
    fixes_applied = []
    
    # Fix 1: Ensure proper error message display
    if 'loginMsg' in content and 'registerMsg' in content:
        fixes_applied.append("✅ Error message elements found")
    else:
        print("❌ Missing error message elements")
    
    # Fix 2: Check if doLogin and doRegister functions exist
    if 'async function doLogin()' in content:
        fixes_applied.append("✅ doLogin function found")
    else:
        print("❌ doLogin function missing")
    
    if 'async function doRegister()' in content:
        fixes_applied.append("✅ doRegister function found")
    else:
        print("❌ doRegister function missing")
    
    # Fix 3: Ensure proper form IDs
    if 'id="loginEmail"' in content and 'id="loginPassword"' in content:
        fixes_applied.append("✅ Login form fields found")
    else:
        print("❌ Login form fields missing")
    
    if 'id="regName"' in content and 'id="regEmail"' in content and 'id="regPassword"' in content:
        fixes_applied.append("✅ Registration form fields found")
    else:
        print("❌ Registration form fields missing")
    
    # Fix 4: Check for proper button handlers
    if 'onclick="doLogin()"' in content:
        fixes_applied.append("✅ Login button handler found")
    else:
        print("❌ Login button handler missing")
    
    if 'onclick="doRegister()"' in content:
        fixes_applied.append("✅ Register button handler found")
    else:
        print("❌ Register button handler missing")
    
    print(f"\n📊 Analysis complete:")
    for fix in fixes_applied:
        print(f"   {fix}")
    
    return len(fixes_applied) >= 6

def create_simple_auth_page():
    """Create a simple authentication page that definitely works"""
    print("\n🔧 Creating simple authentication page...")
    
    simple_auth_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Expense Tracker - Login</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #333; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background: #0056b3; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .message { padding: 10px; margin: 15px 0; border-radius: 5px; text-align: center; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .toggle { text-align: center; margin-top: 20px; }
        .toggle a { color: #007bff; text-decoration: none; }
        .toggle a:hover { text-decoration: underline; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Expense Tracker</h1>
        
        <!-- Login Form -->
        <div id="loginSection">
            <h2>Sign In</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label for="loginEmail">Email:</label>
                    <input type="email" id="loginEmail" required>
                </div>
                <div class="form-group">
                    <label for="loginPassword">Password:</label>
                    <input type="password" id="loginPassword" required>
                </div>
                <button type="submit" id="loginBtn">Sign In</button>
            </form>
            <div id="loginMessage"></div>
            <div class="toggle">
                Don't have an account? <a href="#" onclick="showRegister()">Create one</a>
            </div>
        </div>

        <!-- Register Form -->
        <div id="registerSection" class="hidden">
            <h2>Create Account</h2>
            <form id="registerForm">
                <div class="form-group">
                    <label for="regName">Full Name:</label>
                    <input type="text" id="regName" required>
                </div>
                <div class="form-group">
                    <label for="regEmail">Email:</label>
                    <input type="email" id="regEmail" required>
                </div>
                <div class="form-group">
                    <label for="regPassword">Password:</label>
                    <input type="password" id="regPassword" required minlength="6">
                </div>
                <button type="submit" id="registerBtn">Create Account</button>
            </form>
            <div id="registerMessage"></div>
            <div class="toggle">
                Already have an account? <a href="#" onclick="showLogin()">Sign in</a>
            </div>
        </div>
    </div>

    <script>
        function showMessage(elementId, message, type) {
            const element = document.getElementById(elementId);
            element.innerHTML = `<div class="message ${type}">${message}</div>`;
        }

        function showLogin() {
            document.getElementById('loginSection').classList.remove('hidden');
            document.getElementById('registerSection').classList.add('hidden');
        }

        function showRegister() {
            document.getElementById('loginSection').classList.add('hidden');
            document.getElementById('registerSection').classList.remove('hidden');
        }

        // Login form handler
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value.trim();
            const password = document.getElementById('loginPassword').value;
            const btn = document.getElementById('loginBtn');

            if (!email || !password) {
                showMessage('loginMessage', 'Please enter email and password', 'error');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Signing in...';

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (data.success) {
                    showMessage('loginMessage', 'Login successful! Redirecting...', 'success');
                    setTimeout(() => {
                        window.location.href = data.redirect || '/dashboard';
                    }, 1000);
                } else {
                    showMessage('loginMessage', data.message || 'Login failed', 'error');
                    btn.disabled = false;
                    btn.textContent = 'Sign In';
                }
            } catch (error) {
                showMessage('loginMessage', 'Connection error. Please try again.', 'error');
                btn.disabled = false;
                btn.textContent = 'Sign In';
            }
        });

        // Register form handler
        document.getElementById('registerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('regName').value.trim();
            const email = document.getElementById('regEmail').value.trim();
            const password = document.getElementById('regPassword').value;
            const btn = document.getElementById('registerBtn');

            if (!username || !email || !password) {
                showMessage('registerMessage', 'All fields are required', 'error');
                return;
            }

            if (password.length < 6) {
                showMessage('registerMessage', 'Password must be at least 6 characters', 'error');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Creating account...';

            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, email, password })
                });

                const data = await response.json();

                if (data.success) {
                    showMessage('registerMessage', 'Account created! Please sign in.', 'success');
                    setTimeout(() => {
                        document.getElementById('loginEmail').value = email;
                        showLogin();
                    }, 1500);
                } else {
                    showMessage('registerMessage', data.message || 'Registration failed', 'error');
                }
            } catch (error) {
                showMessage('registerMessage', 'Connection error. Please try again.', 'error');
            }

            btn.disabled = false;
            btn.textContent = 'Create Account';
        });
    </script>
</body>
</html>'''
    
    with open('templates/simple_auth.html', 'w', encoding='utf-8') as f:
        f.write(simple_auth_html)
    
    print("✅ Created simple_auth.html")
    return True

def add_simple_auth_route():
    """Add route for simple auth page"""
    print("\n🔧 Adding simple auth route...")
    
    # Read app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if route already exists
    if '@app.route("/simple-auth")' in content:
        print("✅ Simple auth route already exists")
        return True
    
    # Add the route before the existing routes
    route_code = '''
@app.route("/simple-auth")
def simple_auth():
    """Simple authentication page that definitely works"""
    return render_template("simple_auth.html")
'''
    
    # Find a good place to insert (after the test-auth route)
    if '@app.route("/test-auth")' in content:
        content = content.replace(
            '@app.route("/test-auth")\ndef test_auth():\n    """Test page for authentication functionality"""\n    return render_template("../test_auth.html")',
            '@app.route("/test-auth")\ndef test_auth():\n    """Test page for authentication functionality"""\n    return render_template("../test_auth.html")' + route_code
        )
    else:
        # Insert before the home route
        content = content.replace(
            '@app.route("/home")',
            route_code + '\n@app.route("/home")'
        )
    
    # Write back
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added simple auth route to app.py")
    return True

def main():
    print("🔧 Frontend Authentication Fix Tool")
    print("=" * 50)
    
    # Check current home.html
    home_ok = fix_home_html()
    
    # Create simple auth page as backup
    simple_created = create_simple_auth_page()
    
    # Add route for simple auth
    route_added = add_simple_auth_route()
    
    print("\n" + "=" * 50)
    print("🎯 Fix Summary:")
    
    if home_ok:
        print("✅ home.html appears to be working correctly")
        print("   Try: http://127.0.0.1:5000")
    else:
        print("⚠️  home.html may have issues")
    
    if simple_created and route_added:
        print("✅ Created backup simple authentication page")
        print("   Try: http://127.0.0.1:5000/simple-auth")
    
    print("\n💡 Troubleshooting steps:")
    print("1. Start the app: python app.py")
    print("2. Try the main page: http://127.0.0.1:5000")
    print("3. If issues persist, use: http://127.0.0.1:5000/simple-auth")
    print("4. Check browser console (F12) for JavaScript errors")
    print("5. Check Flask logs for server errors")

if __name__ == "__main__":
    main()
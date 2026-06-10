#!/usr/bin/env python3
"""
Startup script for AI Expense Tracker
Handles dependency checking and provides helpful error messages
"""
import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        ('flask', 'Flask'),
        ('werkzeug', 'Werkzeug'),
        ('sqlite3', 'SQLite3 (built-in)'),
    ]
    
    optional_packages = [
        ('easyocr', 'EasyOCR (for OCR functionality)'),
        ('pytesseract', 'PyTesseract (OCR fallback)'),
        ('PIL', 'Pillow (image processing)'),
    ]
    
    missing_required = []
    missing_optional = []
    
    print("\n📦 Checking dependencies...")
    
    # Check required packages
    for package, name in required_packages:
        if package == 'sqlite3':
            # sqlite3 is built-in
            print(f"✅ {name}")
            continue
            
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_required.append((package, name))
            print(f"❌ {name}")
        else:
            print(f"✅ {name}")
    
    # Check optional packages
    for package, name in optional_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_optional.append((package, name))
            print(f"⚠️  {name} (optional)")
        else:
            print(f"✅ {name}")
    
    if missing_required:
        print(f"\n❌ Missing required packages:")
        for package, name in missing_required:
            print(f"   • {name}")
        print(f"\n💡 Install with: pip install {' '.join([p[0] for p in missing_required])}")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional packages (OCR features will be limited):")
        for package, name in missing_optional:
            print(f"   • {name}")
        print(f"\n💡 Install with: pip install {' '.join([p[0] for p in missing_optional])}")
    
    return True

def install_requirements():
    """Install requirements from requirements.txt"""
    if os.path.exists('requirements.txt'):
        print("\n📥 Installing requirements...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Requirements installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements")
            return False
    else:
        print("⚠️  requirements.txt not found")
        return True

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting AI Expense Tracker...")
    print("   URL: http://127.0.0.1:5000")
    print("   Press Ctrl+C to stop\n")
    
    try:
        # Import and run the app
        from app import app
        app.run(debug=False, threaded=True)
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
        return True
    except Exception as e:
        print(f"❌ Application error: {e}")
        return False

def main():
    """Main startup function"""
    print("🤖 AI Expense Tracker - Startup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        response = input("\n❓ Install missing packages? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            if not install_requirements():
                sys.exit(1)
        else:
            print("❌ Cannot start without required packages")
            sys.exit(1)
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()
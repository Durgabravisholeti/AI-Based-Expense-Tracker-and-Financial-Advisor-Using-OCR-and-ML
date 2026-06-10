@echo off
echo 🔮 Testing AI Prediction Functionality
echo =====================================
echo.
echo This will:
echo 1. Add test data across 4 months
echo 2. Start the server
echo 3. Open your browser
echo.
echo Press any key to continue...
pause >nul

cd /d "%~dp0"
python test_frontend_prediction.py
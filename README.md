# 🤖 AI Expense Tracker

A comprehensive Flask-based expense tracking application with AI-powered predictions, OCR bill scanning, and advanced analytics.

## ✨ Features

### 🔐 **Secure Authentication**
- User registration and login with secure password hashing (Werkzeug)
- Session management with CSRF protection
- Input validation and sanitization

### 💰 **Expense Management**
- Add, edit, and delete expenses
- Auto-categorization into 7 categories (Food, Travel, Shopping, Bills, Health, Education, General)
- Date validation and amount limits
- Real-time category preview

### 📸 **OCR Bill Scanning**
- Upload receipt images (PNG, JPG, JPEG, GIF, BMP, WEBP)
- Automatic amount extraction using EasyOCR + Tesseract fallback
- Drag-and-drop file upload
- Smart amount detection with multiple regex patterns

### 🧠 **AI-Powered Insights**
- Linear regression model for next month expense prediction
- Trend analysis (increasing/decreasing/stable)
- Personalized financial tips based on spending patterns
- Category-wise spending breakdown

### 📊 **Advanced Analytics (6 Charts)**
1. **Monthly Spending** - Bar chart showing spending trends
2. **Category Breakdown** - Doughnut chart of expense categories
3. **Daily Spending** - Line chart of last 30 days
4. **Top 5 Expenses** - Horizontal bar chart of highest expenses
5. **Weekday Patterns** - Radar chart showing spending by day of week
6. **Cumulative Spending** - Area chart of monthly cumulative total

### 🎨 **Modern UI/UX**
- Responsive design with dark theme
- Interactive dashboard with real-time updates
- Mobile-friendly sidebar navigation
- Toast notifications and loading states
- Smooth animations and transitions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd expense-tracker
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://127.0.0.1:5000`

### Optional: OCR Setup

For bill scanning functionality, you can install either:

**Option 1: EasyOCR (Recommended)**
```bash
pip install easyocr
```
- Downloads models automatically on first use (~500MB)
- Works out of the box, no additional setup needed

**Option 2: Tesseract OCR**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install and add to system PATH
- The app will auto-detect Tesseract installation

## 🧪 Testing

Run the test script to verify functionality:
```bash
python test_app.py
```

This will test:
- User registration and login
- Adding expenses
- Retrieving expense data
- Summary calculations

## 📁 Project Structure

```
expense-tracker/
├── app.py              # Main Flask application
├── model.py            # Linear regression prediction model
├── ocr.py              # OCR processing (EasyOCR + Tesseract)
├── utils.py            # Categorization and tips generation
├── requirements.txt    # Python dependencies
├── expenses.db         # SQLite database (auto-created)
├── static/
│   ├── app.js         # Frontend JavaScript
│   ├── style.css      # Main stylesheet
│   ├── home.css       # Landing page styles
│   └── auth.css       # Authentication modal styles
├── templates/
│   ├── home.html      # Landing page
│   ├── index.html     # Dashboard
│   ├── login.html     # Login page
│   └── register.html  # Registration page
└── uploads/           # Temporary OCR file storage
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key (auto-generated if not set)

### Database
- Uses SQLite by default (`expenses.db`)
- Automatic table creation and indexing
- WAL mode enabled for better concurrency

### File Uploads
- Maximum file size: 10MB
- Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP
- Files are automatically cleaned up after OCR processing

## 🛡️ Security Features

- **Password Security**: Werkzeug password hashing (PBKDF2)
- **Input Validation**: Server-side validation for all inputs
- **File Upload Security**: File type validation and size limits
- **SQL Injection Protection**: Parameterized queries
- **XSS Protection**: HTML escaping in templates and JavaScript
- **Session Security**: Secure session configuration

## 🎯 Usage Guide

### 1. **Registration & Login**
- Create an account with username, email, and password
- Login to access the dashboard

### 2. **Adding Expenses**
- Use "Add Expense" section
- Enter title, amount, and date
- Category is auto-detected from title keywords
- Or use "Scan Bill" to extract amount from receipt images

### 3. **Viewing Analytics**
- Dashboard shows summary cards and 2 main charts
- "Reports" section has 6 detailed charts
- All charts update in real-time as you add expenses

### 4. **AI Insights**
- "AI Advisor" section provides predictions and tips
- Prediction model requires at least 2 months of data
- Tips are personalized based on your spending patterns

### 5. **Managing Expenses**
- Edit expenses by clicking the edit button in tables
- Delete expenses with confirmation dialog
- All changes update charts and summaries immediately

## 🔍 Troubleshooting

### Common Issues

**OCR not working:**
- Install EasyOCR: `pip install easyocr`
- Or install Tesseract from the official website
- Check console logs for specific error messages

**Database locked errors:**
- Restart the application
- Check if multiple instances are running

**Charts not loading:**
- Ensure Chart.js CDN is accessible
- Check browser console for JavaScript errors

**Login/Registration issues:**
- Verify all required fields are filled
- Check password meets minimum requirements (6+ characters)
- Ensure email format is valid

## 🚀 Production Deployment

For production use:

1. **Set environment variables:**
   ```bash
   export SECRET_KEY="your-secure-secret-key"
   export FLASK_ENV="production"
   ```

2. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Consider using PostgreSQL instead of SQLite**
4. **Set up proper logging and monitoring**
5. **Use HTTPS with SSL certificates**

## 📊 Technical Details

### Backend (Flask)
- **Framework**: Flask 2.3+
- **Database**: SQLite with WAL mode
- **Authentication**: Werkzeug password hashing
- **File Handling**: Secure filename generation
- **API**: RESTful endpoints with JSON responses

### Frontend
- **Charts**: Chart.js 4.x with custom themes
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **JavaScript**: Vanilla ES6+ with async/await
- **Responsive**: Mobile-first design approach

### AI/ML Components
- **Prediction**: Linear regression (built from scratch)
- **OCR**: EasyOCR (primary) + Tesseract (fallback)
- **Categorization**: Keyword-based classification
- **Tips**: Rule-based financial advice system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **EasyOCR** for OCR functionality
- **Chart.js** for beautiful charts
- **Font Awesome** for icons
- **Flask** for the web framework

---

**Made with ❤️ for better financial management**
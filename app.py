try:
    from flask import Flask, request, jsonify, render_template, redirect, url_for, session, g
except ImportError as exc:
    raise ImportError("Flask is required to run this application. Install it with `pip install flask`.") from exc
import sqlite3, os, datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

# Disable static file caching during development
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}

DB = "expenses.db"

# ── DB Helpers ────────────────────────────────────────────────────────────────

def get_db():
    """Return a per-request cached DB connection."""
    if "db" not in g:
        g.db = sqlite3.connect(DB, timeout=10)
        g.db.row_factory = sqlite3.Row
        # Enable WAL mode for better concurrency
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA synchronous=NORMAL")
        g.db.execute("PRAGMA cache_size=1000")
        g.db.execute("PRAGMA temp_store=memory")
    return g.db

@app.teardown_appcontext
def close_db(exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def hash_pw(pw):
    return generate_password_hash(pw)

def verify_pw(pw, hash):
    return check_password_hash(hash, pw)

def init_db():
    # Run once at startup using a direct connection (not g, which needs app context)
    conn = sqlite3.connect(DB, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email    TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created  TEXT DEFAULT (DATE('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  INTEGER NOT NULL,
            title    TEXT NOT NULL,
            amount   REAL NOT NULL,
            category TEXT DEFAULT 'General',
            date     TEXT DEFAULT (DATE('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    # Add indexes for faster lookups
    conn.execute("CREATE INDEX IF NOT EXISTS idx_expenses_user ON expenses(user_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(user_id, date)")
    conn.commit()
    conn.close()

init_db()

def current_user():
    return session.get("user_id")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ── Pages ─────────────────────────────────────────────────────────────────────

@app.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/test-auth")
def test_auth():
    """Test page for authentication functionality"""
    return render_template("test_auth.html")
@app.route("/about")
def about_page():
    """About page with information about the AI Expense Tracker"""
    return render_template("about.html",
        logged_in=bool(current_user()),
        username=session.get("username", ""))

@app.route("/simple-auth")
def simple_auth():
    """Simple authentication page that definitely works"""
    return render_template("simple_auth.html")


@app.route("/home")
def home_page():
    return render_template("home.html",
        logged_in=bool(current_user()),
        username=session.get("username", ""))

@app.route("/")
def index():
    return render_template("home.html",
        logged_in=bool(current_user()),
        username=session.get("username", ""))

@app.route("/dashboard")
def dashboard():
    if not current_user():
        return redirect(url_for("index"))
    return render_template("index.html", username=session.get("username", "User"))

@app.route("/login")
def login_page():
    if current_user():
        return redirect(url_for("index"))
    return render_template("login.html", next=request.args.get("next", ""))

@app.route("/register")
def register_page():
    if current_user():
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ── Auth APIs ─────────────────────────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def login():
    try:
        data     = request.get_json(silent=True) or {}
        email    = data.get("email", "").strip().lower()
        password = data.get("password", "")
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400
            
        print(f"[LOGIN] email={repr(email)}")
        db   = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=?", (email,)
        ).fetchone()
        
        if user and verify_pw(password, user["password"]):
            session["user_id"]  = user["id"]
            session["username"] = user["username"]
            session["email"]    = user["email"]
            next_section = data.get("next", "")
            redirect_url = "/dashboard"
            if next_section:
                redirect_url = f"/dashboard#{next_section}"
            return jsonify({"success": True, "next": next_section, "redirect": redirect_url})
        return jsonify({"success": False, "message": "Invalid email or password"}), 401
    except Exception as e:
        print(f"[LOGIN ERROR] {e}")
        return jsonify({"success": False, "message": "Login failed"}), 500

@app.route("/api/register", methods=["POST"])
def register():
    try:
        data     = request.get_json(silent=True) or {}
        username = data.get("username", "").strip()
        email    = data.get("email", "").strip().lower()
        raw_pw   = data.get("password", "")
        
        if not username or not email or not raw_pw:
            return jsonify({"success": False, "message": "All fields are required"}), 400
        if len(raw_pw) < 6:
            return jsonify({"success": False, "message": "Password must be at least 6 characters"}), 400
        if len(username) < 2:
            return jsonify({"success": False, "message": "Username must be at least 2 characters"}), 400
        if "@" not in email or "." not in email:
            return jsonify({"success": False, "message": "Please enter a valid email address"}), 400
            
        password = hash_pw(raw_pw)
        db = get_db()
        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?,?,?)",
            (username, email, password)
        )
        db.commit()
        return jsonify({"success": True})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Email or username already exists"}), 400
    except Exception as e:
        print(f"[REGISTER ERROR] {e}")
        return jsonify({"success": False, "message": "Registration failed"}), 500

# ── Expense APIs ──────────────────────────────────────────────────────────────

@app.route("/add", methods=["POST"])
def add_expense():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        from utils import categorize_expense
        data     = request.get_json(silent=True) or {}
        title    = data.get("title", "").strip()
        amount   = data.get("amount")
        date     = data.get("date") or datetime.date.today().isoformat()
        
        # Validation
        if not title:
            return jsonify({"error": "Title is required"}), 400
        if len(title) > 200:
            return jsonify({"error": "Title too long (max 200 characters)"}), 400
        
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid amount"}), 400
            
        if amount <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
        if amount > 1000000:
            return jsonify({"error": "Amount cannot exceed ₹10,00,000"}), 400
            
        # Validate date
        try:
            datetime.datetime.fromisoformat(date)
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
        
        category = categorize_expense(title)
        db = get_db()
        db.execute(
            "INSERT INTO expenses (user_id, title, amount, category, date) VALUES (?,?,?,?,?)",
            (current_user(), title, amount, category, date)
        )
        db.commit()
        return jsonify({"success": True, "category": category})
    except Exception as e:
        print(f"[ADD EXPENSE ERROR] {e}")
        return jsonify({"error": "Failed to add expense"}), 500

@app.route("/expenses", methods=["GET"])
def get_expenses():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    limit = request.args.get("limit", 50, type=int)
    limit = min(limit, 1000)  # Cap at 1000 for performance
    rows = get_db().execute(
        "SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC, id DESC LIMIT ?",
        (current_user(), limit)
    ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        from utils import categorize_expense
        data = request.get_json(silent=True) or {}
        title = data.get("title", "").strip()
        amount = data.get("amount")
        date = data.get("date")
        
        # Validation
        if not title:
            return jsonify({"error": "Title is required"}), 400
        if len(title) > 200:
            return jsonify({"error": "Title too long (max 200 characters)"}), 400
        
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid amount"}), 400
            
        if amount <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
        if amount > 1000000:
            return jsonify({"error": "Amount cannot exceed ₹10,00,000"}), 400
            
        # Validate date
        try:
            datetime.datetime.fromisoformat(date)
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
        
        category = categorize_expense(title)
        db = get_db()
        
        # Check if expense belongs to current user
        existing = db.execute(
            "SELECT id FROM expenses WHERE id=? AND user_id=?", 
            (expense_id, current_user())
        ).fetchone()
        
        if not existing:
            return jsonify({"error": "Expense not found"}), 404
        
        db.execute(
            "UPDATE expenses SET title=?, amount=?, category=?, date=? WHERE id=? AND user_id=?",
            (title, amount, category, date, expense_id, current_user())
        )
        db.commit()
        return jsonify({"success": True, "category": category})
    except Exception as e:
        print(f"[UPDATE EXPENSE ERROR] {e}")
        return jsonify({"error": "Failed to update expense"}), 500

@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        db = get_db()
        
        # Check if expense belongs to current user
        existing = db.execute(
            "SELECT id FROM expenses WHERE id=? AND user_id=?", 
            (expense_id, current_user())
        ).fetchone()
        
        if not existing:
            return jsonify({"error": "Expense not found"}), 404
        
        db.execute(
            "DELETE FROM expenses WHERE id=? AND user_id=?",
            (expense_id, current_user())
        )
        db.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(f"[DELETE EXPENSE ERROR] {e}")
        return jsonify({"error": "Failed to delete expense"}), 500

@app.route("/upload", methods=["POST"])
def upload_bill():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Please upload PNG, JPG, JPEG, GIF, BMP, or WEBP"}), 400
    
    # Check file size (max 10MB)
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset to beginning
    if size > 10 * 1024 * 1024:
        return jsonify({"error": "File too large. Maximum size is 10MB"}), 400
    
    try:
        from ocr import extract_amount_from_image
        filename = secure_filename(file.filename)
        # Add timestamp to prevent filename conflicts
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        amount, raw_text = extract_amount_from_image(filepath)
        
        # Clean up uploaded file after processing
        try:
            os.remove(filepath)
        except:
            pass
            
        return jsonify({"amount": amount, "raw_text": raw_text})
    except Exception as e:
        print(f"[OCR ERROR] {e}")
        return jsonify({"error": "OCR processing failed. Please try again with a clearer image."}), 500

@app.route("/predict", methods=["GET"])
def predict():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    from model import predict_next_month
    rows = get_db().execute(
        "SELECT amount, date FROM expenses WHERE user_id=?", (current_user(),)
    ).fetchall()
    return jsonify(predict_next_month([dict(r) for r in rows]))

@app.route("/tips", methods=["GET"])
def tips():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    from utils import get_tips
    rows = get_db().execute(
        "SELECT amount, category FROM expenses WHERE user_id=?", (current_user(),)
    ).fetchall()
    return jsonify(get_tips([dict(r) for r in rows]))

# ── Chart Data APIs ───────────────────────────────────────────────────────────

@app.route("/data", methods=["GET"])
@app.route("/chart-data", methods=["GET"])
def chart_data():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    rows = get_db().execute(
        """SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
           FROM expenses WHERE user_id=?
           GROUP BY month ORDER BY month DESC LIMIT 6""",
        (current_user(),)
    ).fetchall()
    rows = list(reversed(rows))
    return jsonify({
        "labels": [r["month"] for r in rows],
        "values": [round(r["total"], 2) for r in rows]
    })

@app.route("/category-data", methods=["GET"])
def category_data():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    rows = get_db().execute(
        """SELECT category, SUM(amount) as total
           FROM expenses WHERE user_id=?
           GROUP BY category ORDER BY total DESC""",
        (current_user(),)
    ).fetchall()
    return jsonify({
        "labels": [r["category"] for r in rows],
        "values": [round(r["total"], 2) for r in rows]
    })

@app.route("/daily-data", methods=["GET"])
def daily_data():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    rows = get_db().execute(
        """SELECT date, SUM(amount) as total
           FROM expenses WHERE user_id=? AND date >= DATE('now', '-30 days')
           GROUP BY date ORDER BY date ASC""",
        (current_user(),)
    ).fetchall()
    return jsonify({
        "labels": [r["date"] for r in rows],
        "values": [round(r["total"], 2) for r in rows]
    })

@app.route("/top-expenses", methods=["GET"])
def top_expenses():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    rows = get_db().execute(
        """SELECT title, amount, category FROM expenses WHERE user_id=?
           ORDER BY amount DESC LIMIT 5""",
        (current_user(),)
    ).fetchall()
    return jsonify({
        "labels": [r["title"] for r in rows],
        "values": [round(r["amount"], 2) for r in rows],
        "categories": [r["category"] for r in rows]
    })

@app.route("/weekday-data", methods=["GET"])
def weekday_data():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    rows = get_db().execute(
        """SELECT strftime('%w', date) as dow, SUM(amount) as total
           FROM expenses WHERE user_id=?
           GROUP BY dow ORDER BY dow ASC""",
        (current_user(),)
    ).fetchall()
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    totals = {str(i): 0 for i in range(7)}
    for r in rows:
        totals[r["dow"]] = round(r["total"], 2)
    return jsonify({
        "labels": days,
        "values": [totals[str(i)] for i in range(7)]
    })

@app.route("/summary", methods=["GET"])
def summary():
    if not current_user():
        return jsonify({"error": "Unauthorized"}), 401
    uid         = current_user()
    month_start = datetime.date.today().replace(day=1).isoformat()
    db          = get_db()
    total      = db.execute("SELECT COALESCE(SUM(amount),0) as t FROM expenses WHERE user_id=?", (uid,)).fetchone()["t"]
    this_month = db.execute("SELECT COALESCE(SUM(amount),0) as t FROM expenses WHERE user_id=? AND date>=?", (uid, month_start)).fetchone()["t"]
    count      = db.execute("SELECT COUNT(*) as c FROM expenses WHERE user_id=?", (uid,)).fetchone()["c"]
    return jsonify({"total": round(total, 2), "this_month": round(this_month, 2), "count": count})

if __name__ == "__main__":
    import threading, webbrowser
    print("\n  AI Expense Tracker running at: http://127.0.0.1:5000\n")
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=False, threaded=True)

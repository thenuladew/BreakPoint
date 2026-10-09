from flask import Flask, request, render_template, redirect, url_for, session, g
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "kavach_sys_secret_2048_!@#"
DB_PATH = "database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    
    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        return redirect(url_for("dashboard"))
    
    return render_template("login.html", error="Invalid credentials.")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))
    
    db = get_db()
    # Fetch documents for the logged in user ONLY (Secure)
    cur = db.execute("SELECT id, title, date FROM documents WHERE user_id = ?", (session["user_id"],))
    documents = cur.fetchall()
    
    return render_template("dashboard.html", user=session["username"], documents=documents)

@app.route("/portal/document")
def document():
    if "user_id" not in session:
        return redirect(url_for("index"))
    
    doc_id = request.args.get("id")
    if not doc_id:
        return "Missing document ID.", 400
    
    db = get_db()
    # VULNERABILITY: IDOR (Insecure Direct Object Reference)
    # The application fetches the document by ID without checking if the user owns it!
    cur = db.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    doc = cur.fetchone()
    
    if not doc:
        return render_template("document.html", error="Document not found or has been removed.")
    
    return render_template("document.html", doc=doc, user=session["username"])

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        import init_db
        init_db.init_db()
    app.run(host="0.0.0.0", port=5000)

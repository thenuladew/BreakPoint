import sqlite3
import os

DB_PATH = "database.db"

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    
    cur.execute("""
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Insert users
    users = [
        ("admin", "c0mpl3x_adm1n_p@ss", "admin"),
        ("dperera_ext", "h1dd3n_c0ntr@ct0r_p@ss", "contractor"),
        ("guest", "guest2048", "guest"),
        ("j.smith", "smith123", "contractor")
    ]
    cur.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", users)
    
    # Get user IDs
    cur.execute("SELECT id, username FROM users")
    user_map = {row[1]: row[0] for row in cur.fetchall()}
    
    flag_stage2 = os.environ.get("FLAG_STAGE2", "BP{idor_unlocked_portal_access}")
    
    # Insert explicitly to control IDs
    cur.execute("INSERT INTO documents (id, user_id, title, content, date) VALUES (?, ?, ?, ?, ?)", (1000, user_map["admin"], "System Architecture v2", "Confidential system architecture. Do not distribute.", "2048-09-12"))
    cur.execute("INSERT INTO documents (id, user_id, title, content, date) VALUES (?, ?, ?, ?, ?)", (1001, user_map["guest"], "Guest Onboarding Guide", "Welcome to the Kavach Systems Contractor Portal. As a guest, you have restricted access. Use this portal to review your assigned documents.", "2048-09-15"))
    cur.execute("INSERT INTO documents (id, user_id, title, content, date) VALUES (?, ?, ?, ?, ?)", (1002, user_map["j.smith"], "Q3 Invoice", "Total hours: 160. Amount due: $8,000.", "2048-10-01"))
    
    # Insert Devinda's classified document at ID 1042
    dperera_doc = f"""
    CLASSIFIED INCIDENT TRANSMISSION
    
    Warning: This document contains restricted payload parameters.
    
    FLAG: {flag_stage2}
    
    Transmission Log Intercept:
    The transmission log you requested has been encrypted for security.
    You can access the encrypted payload using the link below:
    
    <a href='/static/downloads/transmission_log_48.txt' target='_blank' style='color:#00ff88; text-decoration:underline;'>Download transmission_log_48.txt</a>
    
    Note: The encryption key is derived from standard security protocol phase 3.
    """
    cur.execute("INSERT INTO documents (id, user_id, title, content, date) VALUES (?, ?, ?, ?, ?)", (1042, user_map["dperera_ext"], "RESTRICTED: Incident Transmission", dperera_doc, "2048-10-07"))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()


"""
BREAKPOINT CTF – Control Platform
Flask application: team auth, flag validation, scoring, timer, Stage 6 gating.
"""

import hashlib
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

from flask import (Flask, abort, g, jsonify, redirect,
                   render_template, request, session, url_for)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ── Config ────────────────────────────────────────────────────
DB_PATH      = os.environ.get("DB_PATH",        "/app/database/breakpoint.db")
SCHEMA_PATH  = Path(__file__).parent / "database" / "schema.sql"
SEED_PATH    = Path(__file__).parent / "database" / "seed.py"
FLAG_SALT    = os.environ.get("FLAG_SALT",      "")
SECRET_KEY   = os.environ.get("SECRET_KEY",     "dev-secret-change-me")
ADMIN_PASS   = os.environ.get("ADMIN_PASSWORD",  "admin")
TIMER_SECS   = int(os.environ.get("TIMER_SECS", 3600))   # 60 minutes

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ── Rate limiting ─────────────────────────────────────────────
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

# ─────────────────────────────────────────────────────────────
# Database helpers
# ─────────────────────────────────────────────────────────────

def get_db() -> sqlite3.Connection:
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA journal_mode=WAL")
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create schema and seed data on first run."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())
    conn.commit()
    conn.close()
    # Run seed
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location("seed", SEED_PATH)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    conn2 = sqlite3.connect(DB_PATH)
    mod.seed(conn2)
    conn2.close()


# ─────────────────────────────────────────────────────────────
# Auth helpers
# ─────────────────────────────────────────────────────────────

def hash_flag(plaintext: str) -> str:
    return hashlib.sha256(f"{FLAG_SALT}{plaintext}".encode()).hexdigest()


def get_team_from_token(token: str):
    db = get_db()
    return db.execute(
        "SELECT * FROM teams WHERE token=?", (token,)
    ).fetchone()


def require_team(f):
    """Decorator: resolve team from session OR X-Team-Token header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get("team_token") or request.headers.get("X-Team-Token")
        if not token:
            abort(401)
        team = get_team_from_token(token)
        if not team:
            abort(401)
        g.team = team
        return f(*args, **kwargs)
    return decorated


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            abort(403)
        return f(*args, **kwargs)
    return decorated


# ─────────────────────────────────────────────────────────────
# Timer helpers
# ─────────────────────────────────────────────────────────────

def get_timer(team_id: int) -> dict:
    db = get_db()
    row = db.execute(
        "SELECT * FROM timers WHERE team_id=?", (team_id,)
    ).fetchone()
    if not row:
        return {"started": False, "remaining_s": TIMER_SECS, "expired": False, "stopped": False}

    if row["stopped_at"]:
        return {"started": True, "remaining_s": 0, "expired": False, "stopped": True}

    if row["is_expired"]:
        return {"started": True, "remaining_s": 0, "expired": True, "stopped": False}

    if row["started_at"] is None:
        return {"started": False, "remaining_s": TIMER_SECS, "expired": False, "stopped": False}

    started = datetime.fromisoformat(row["started_at"])
    elapsed = (datetime.now(timezone.utc) - started).total_seconds()
    remaining = max(0, TIMER_SECS - int(elapsed))

    if remaining == 0:
        # Mark as expired in DB
        db.execute(
            "UPDATE timers SET is_expired=1 WHERE team_id=?", (team_id,)
        )
        db.commit()
        return {"started": True, "remaining_s": 0, "expired": True, "stopped": False}

    return {"started": True, "remaining_s": remaining, "expired": False, "stopped": False}


def start_timer(team_id: int):
    db = get_db()
    existing = db.execute(
        "SELECT started_at FROM timers WHERE team_id=?", (team_id,)
    ).fetchone()
    if existing and existing["started_at"]:
        return  # Already running
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        """INSERT INTO timers (team_id, started_at, duration_s)
           VALUES (?, ?, ?)
           ON CONFLICT(team_id) DO UPDATE SET started_at=excluded.started_at""",
        (team_id, now, TIMER_SECS),
    )
    db.commit()


def stop_timer(team_id: int):
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "UPDATE timers SET stopped_at=? WHERE team_id=?", (now, team_id)
    )
    db.commit()


# ─────────────────────────────────────────────────────────────
# Stage helpers
# ─────────────────────────────────────────────────────────────

def get_solved_stages(team_id: int) -> set:
    db = get_db()
    rows = db.execute(
        "SELECT DISTINCT stage_id FROM submissions WHERE team_id=? AND correct=1",
        (team_id,),
    ).fetchall()
    return {r["stage_id"] for r in rows}


def get_all_stages() -> list:
    return get_db().execute("SELECT * FROM stages ORDER BY id").fetchall()


# ─────────────────────────────────────────────────────────────
# Routes – Public / Team UI
# ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    token = session.get("team_token")
    team  = get_team_from_token(token) if token else None
    if team:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def register():
    if request.method == "GET":
        return render_template("register.html")

    team_name = request.form.get("team_name", "").strip()
    if not team_name or len(team_name) > 40:
        return render_template("register.html", error="Team name must be 1–40 characters.")

    token = str(uuid.uuid4())
    db = get_db()
    try:
        db.execute(
            "INSERT INTO teams (name, token) VALUES (?, ?)", (team_name, token)
        )
        # Create a timer row (not started yet)
        team_id = db.execute(
            "SELECT id FROM teams WHERE token=?", (token,)
        ).fetchone()["id"]
        db.execute(
            "INSERT OR IGNORE INTO timers (team_id, duration_s) VALUES (?, ?)",
            (team_id, TIMER_SECS),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return render_template("register.html", error="Team name already taken.")

    session["team_token"] = token
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    token = request.form.get("token", "").strip()
    team  = get_team_from_token(token)
    if not team:
        return render_template("login.html", error="Invalid team token.")
    session["team_token"] = token
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
@require_team
def dashboard():
    team   = g.team
    stages = get_all_stages()
    solved = get_solved_stages(team["id"])
    timer  = get_timer(team["id"])
    return render_template(
        "dashboard.html",
        team=team,
        stages=stages,
        solved=solved,
        timer=timer,
    )


@app.route("/scoreboard")
def scoreboard():
    db = get_db()
    teams = db.execute(
        "SELECT name, score FROM teams ORDER BY score DESC, created_at ASC"
    ).fetchall()
    return render_template("scoreboard.html", teams=teams)


# ─────────────────────────────────────────────────────────────
# API – Flag Submission
# ─────────────────────────────────────────────────────────────

@app.route("/api/submit", methods=["POST"])
@require_team
@limiter.limit("5 per minute")
def submit_flag():
    team    = g.team
    data    = request.get_json(silent=True) or request.form
    stage_id = int(data.get("stage_id", 0))
    answer   = str(data.get("flag", "")).strip()

    if stage_id < 1 or stage_id > 6:
        return jsonify({"success": False, "message": "Invalid stage."}), 400

    db = get_db()

    # Already solved?
    already = db.execute(
        "SELECT 1 FROM submissions WHERE team_id=? AND stage_id=? AND correct=1",
        (team["id"], stage_id),
    ).fetchone()
    if already:
        return jsonify({"success": False, "message": "Stage already solved!", "already_solved": True})

    answer_hash = hash_flag(answer)
    flag_row    = db.execute(
        "SELECT flag_hash FROM flags WHERE stage_id=?", (stage_id,)
    ).fetchone()

    correct = flag_row and (flag_row["flag_hash"] == answer_hash)

    # Log submission
    db.execute(
        "INSERT INTO submissions (team_id, stage_id, answer_hash, correct) VALUES (?,?,?,?)",
        (team["id"], stage_id, answer_hash, 1 if correct else 0),
    )

    if correct:
        stage_row = db.execute(
            "SELECT points FROM stages WHERE id=?", (stage_id,)
        ).fetchone()
        # Subtract hint penalties
        hints_used = db.execute(
            "SELECT hint_number FROM hint_usage WHERE team_id=? AND stage_id=?",
            (team["id"], stage_id),
        ).fetchall()
        penalty = sum(5 if h["hint_number"] == 1 else 10 for h in hints_used)
        awarded = max(0, stage_row["points"] - int(stage_row["points"] * penalty / 100))

        db.execute(
            "UPDATE teams SET score = score + ? WHERE id=?", (awarded, team["id"])
        )

        # Stage 6 correct → stop countdown timer
        if stage_id == 6:
            stop_timer(team["id"])

        db.commit()
        return jsonify({
            "success": True,
            "message": f"🎉 Correct! +{awarded} points awarded.",
            "points_awarded": awarded,
            "stage_id": stage_id,
        })

    db.commit()
    return jsonify({"success": False, "message": "Incorrect flag. Keep trying."})


# ─────────────────────────────────────────────────────────────
# API – Hints
# ─────────────────────────────────────────────────────────────

@app.route("/api/hint", methods=["POST"])
@require_team
@limiter.limit("20 per minute")
def get_hint():
    team      = g.team
    data      = request.get_json(silent=True) or request.form
    stage_id  = int(data.get("stage_id", 0))
    hint_num  = int(data.get("hint_number", 1))

    if stage_id < 1 or stage_id > 6 or hint_num not in (1, 2):
        return jsonify({"success": False, "message": "Invalid request."}), 400

    db = get_db()
    stage = db.execute("SELECT * FROM stages WHERE id=?", (stage_id,)).fetchone()
    hint_text = stage["hint1_text"] if hint_num == 1 else stage["hint2_text"]
    penalty   = 5 if hint_num == 1 else 10

    try:
        db.execute(
            "INSERT INTO hint_usage (team_id, stage_id, hint_number) VALUES (?,?,?)",
            (team["id"], stage_id, hint_num),
        )
        db.commit()
        new_usage = True
    except sqlite3.IntegrityError:
        new_usage = False  # Already used this hint

    return jsonify({
        "success": True,
        "hint": hint_text,
        "penalty_pct": penalty,
        "first_use": new_usage,
    })


# ─────────────────────────────────────────────────────────────
# API – Timer
# ─────────────────────────────────────────────────────────────

@app.route("/api/timer")
@require_team
def api_timer():
    timer = get_timer(g.team["id"])
    return jsonify(timer)


@app.route("/api/start_timer", methods=["POST"])
@require_team
def api_start_timer():
    """Team manually clicks 'Start Challenge' — begins the 60-minute countdown."""
    team_id = g.team["id"]
    timer = get_timer(team_id)
    if timer["started"]:
        return jsonify({"success": False, "message": "Timer already started."})
    start_timer(team_id)
    return jsonify({"success": True, "message": "Challenge timer started! You have 60 minutes."})


# ─────────────────────────────────────────────────────────────
# API – Team Status (used by dashboard JS polling)
# ─────────────────────────────────────────────────────────────

@app.route("/api/status")
@require_team
def api_status():
    team   = g.team
    solved = get_solved_stages(team["id"])
    timer  = get_timer(team["id"])
    return jsonify({
        "team_name": team["name"],
        "score":     team["score"],
        "solved":    sorted(solved),
        "timer":     timer,
    })


# ─────────────────────────────────────────────────────────────
# API – Stage 6 Gate (called by Nginx auth_request)
# ─────────────────────────────────────────────────────────────

@app.route("/api/check_stage6_access")
def check_stage6_access():
    """
    Nginx auth_request endpoint.
    Returns 200 if team has solved Stage 5 AND timer is active.
    Returns 403 otherwise.
    Token comes from X-Team-Token header forwarded by Nginx.
    """
    token = request.headers.get("X-Team-Token")
    if not token:
        abort(403)
    team = get_team_from_token(token)
    if not team:
        abort(403)

    solved = get_solved_stages(team["id"])
    if 5 not in solved:
        abort(403)

    timer = get_timer(team["id"])
    if timer["expired"]:
        abort(403)

    return "", 200


# ─────────────────────────────────────────────────────────────
# Admin routes
# ─────────────────────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASS:
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
        return render_template("admin_login.html", error="Wrong password.")
    return render_template("admin_login.html")


@app.route("/admin")
@require_admin
def admin_dashboard():
    db = get_db()
    teams = db.execute(
        "SELECT t.id, t.name, t.score, t.token, "
        "(SELECT COUNT(*) FROM submissions s WHERE s.team_id=t.id AND s.correct=1) as stages_solved "
        "FROM teams t ORDER BY t.score DESC"
    ).fetchall()
    return render_template("admin.html", teams=teams)


@app.route("/admin/reset_team/<int:team_id>", methods=["POST"])
@require_admin
def admin_reset_team(team_id: int):
    db = get_db()
    db.execute("DELETE FROM submissions WHERE team_id=?", (team_id,))
    db.execute("DELETE FROM hint_usage WHERE team_id=?", (team_id,))
    db.execute("DELETE FROM timers WHERE team_id=?", (team_id,))
    db.execute("UPDATE teams SET score=0 WHERE id=?", (team_id,))
    db.commit()
    return redirect(url_for("admin_dashboard"))


# ─────────────────────────────────────────────────────────────
# Startup
# ─────────────────────────────────────────────────────────────

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

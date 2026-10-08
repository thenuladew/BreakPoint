#!/usr/bin/env python3
"""
Seed script – populates stages and hashed flags.
Run once at container startup (called by app.py init_db).
Environment variables required:
    FLAG_SALT      – random salt string
    FLAG_STAGE1..6 – plaintext flags
"""

import hashlib
import os
import sqlite3

DB_PATH = os.environ.get("DB_PATH", "/app/database/breakpoint.db")
SALT    = os.environ.get("FLAG_SALT", "")

STAGES = [
    {
        "id": 1,
        "title": "Ghost in the Footprint",
        "points": 100,
        "hint1": "Publicly visible staff directories often reveal more than intended.",
        "hint2": "Check the personal blog linked from the employee directory.",
    },
    {
        "id": 2,
        "title": "The Contractor Portal",
        "points": 100,
        "hint1": "You have guest credentials. Try accessing other users' resources.",
        "hint2": "The invoice endpoint at /portal/invoice takes a numeric id parameter.",
    },
    {
        "id": 3,
        "title": "Silent Signals",
        "points": 150,
        "hint1": "The encrypted note uses a classical cipher. The key is something you already know.",
        "hint2": "The Vigenère key is derived from the contractor's job title (lowercase, no spaces).",
    },
    {
        "id": 4,
        "title": "Buried Warning",
        "points": 150,
        "hint1": "Not all images are what they appear. Some carry hidden passengers.",
        "hint2": "Try steghide on each image using the passphrase from Stage 3.",
    },
    {
        "id": 5,
        "title": "The Injection Tool",
        "points": 200,
        "hint1": "Strip away the noise — many strings in this binary are decoys.",
        "hint2": "The real credential is XOR-encoded in the binary data section. Check Ghidra's decompiler output.",
    },
    {
        "id": 6,
        "title": "Last Authorization",
        "points": 300,
        "hint1": "Cross-reference the PCAP sessions with the audit log. One session has no operator approval.",
        "hint2": "Filter PCAP by the client identifier from Stage 5. Compare timestamps with the audit log.",
    },
]

FLAGS = {
    1: os.environ.get("FLAG_STAGE1", ""),
    2: os.environ.get("FLAG_STAGE2", ""),
    3: os.environ.get("FLAG_STAGE3", ""),
    4: os.environ.get("FLAG_STAGE4", ""),
    5: os.environ.get("FLAG_STAGE5", ""),
    6: os.environ.get("FLAG_STAGE6", ""),
}


def hash_flag(plaintext: str) -> str:
    """SHA-256( salt + plaintext )"""
    return hashlib.sha256(f"{SALT}{plaintext}".encode()).hexdigest()


def seed(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    # Seed stages (INSERT OR IGNORE – safe to run multiple times)
    for s in STAGES:
        cur.execute(
            """INSERT OR IGNORE INTO stages
               (id, title, points, hint1_text, hint2_text)
               VALUES (?, ?, ?, ?, ?)""",
            (s["id"], s["title"], s["points"], s["hint1"], s["hint2"]),
        )

    # Seed flags
    for stage_id, plaintext in FLAGS.items():
        if not plaintext:
            print(f"[WARN] FLAG_STAGE{stage_id} is not set – skipping hash.")
            continue
        flag_hash = hash_flag(plaintext)
        cur.execute(
            "INSERT OR REPLACE INTO flags (stage_id, flag_hash) VALUES (?, ?)",
            (stage_id, flag_hash),
        )
        print(f"[SEED] Stage {stage_id} flag hashed: {flag_hash[:12]}…")

    conn.commit()
    print("[SEED] Database seeded successfully.")


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    seed(conn)
    conn.close()

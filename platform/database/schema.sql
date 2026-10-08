-- ============================================================
-- BREAKPOINT CTF – Database Schema
-- ============================================================
-- Apply with:  sqlite3 breakpoint.db < schema.sql
-- ============================================================

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ── Teams ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS teams (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL UNIQUE,
    token        TEXT    NOT NULL UNIQUE,   -- UUID used as Bearer token
    score        INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- ── Stages metadata ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS stages (
    id           INTEGER PRIMARY KEY,       -- 1..6
    title        TEXT    NOT NULL,
    points       INTEGER NOT NULL,
    hint1_text   TEXT    NOT NULL DEFAULT '',
    hint1_used   INTEGER NOT NULL DEFAULT 0,  -- bitmask per team stored in stage_hints
    hint2_text   TEXT    NOT NULL DEFAULT ''
);

-- ── Flags (hashed, never stored plaintext) ───────────────────
CREATE TABLE IF NOT EXISTS flags (
    stage_id     INTEGER PRIMARY KEY REFERENCES stages(id),
    flag_hash    TEXT    NOT NULL    -- SHA-256( FLAG_SALT + plaintext_flag )
);

-- ── Submissions ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS submissions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id      INTEGER NOT NULL REFERENCES teams(id),
    stage_id     INTEGER NOT NULL,
    answer_hash  TEXT    NOT NULL,
    correct      INTEGER NOT NULL DEFAULT 0,  -- 1 = correct
    submitted_at TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_submissions_team ON submissions(team_id, stage_id);

-- ── Per-team hint usage (penalty tracking) ───────────────────
CREATE TABLE IF NOT EXISTS hint_usage (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id      INTEGER NOT NULL REFERENCES teams(id),
    stage_id     INTEGER NOT NULL,
    hint_number  INTEGER NOT NULL,   -- 1 or 2
    used_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(team_id, stage_id, hint_number)
);

-- ── Countdown Timer (one row per team) ───────────────────────
CREATE TABLE IF NOT EXISTS timers (
    team_id      INTEGER PRIMARY KEY REFERENCES teams(id),
    started_at   TEXT    DEFAULT NULL,     -- ISO-8601 UTC when Stage 5 flag was accepted
    duration_s   INTEGER NOT NULL DEFAULT 3600,  -- 60 minutes in seconds
    stopped_at   TEXT    DEFAULT NULL,     -- set when final flag submitted correctly
    is_expired   INTEGER NOT NULL DEFAULT 0   -- set to 1 if time ran out
);

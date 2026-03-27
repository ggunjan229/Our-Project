import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "../ids.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS alerts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp       TEXT    NOT NULL,
            is_attack       INTEGER NOT NULL,
            attack_type     TEXT    NOT NULL,
            severity        TEXT    NOT NULL,
            confidence      REAL    NOT NULL,
            rf_score        REAL,
            xgb_score       REAL,
            ae_score        REAL,
            recon_error     REAL,
            raw_input       TEXT,
            created_at      TEXT    DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS stats (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            date            TEXT    NOT NULL,
            total_analyzed  INTEGER DEFAULT 0,
            total_attacks   INTEGER DEFAULT 0,
            total_benign    INTEGER DEFAULT 0,
            top_attack_type TEXT,
            updated_at      TEXT    DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized")


def save_alert(prediction: dict, raw_input: str = ""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts
        (timestamp, is_attack, attack_type, severity, confidence,
         rf_score, xgb_score, ae_score, recon_error, raw_input)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        int(prediction["is_attack"]),
        prediction["attack_type"],
        prediction["severity"],
        prediction["hybrid_confidence"],
        prediction["model_breakdown"]["random_forest"],
        prediction["model_breakdown"]["xgboost"],
        prediction["model_breakdown"]["autoencoder"],
        prediction["reconstruction_error"],
        raw_input
    ))

    conn.commit()
    conn.close()


def get_recent_alerts(limit: int = 50) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM alerts
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_stats() -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM alerts")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as attacks FROM alerts WHERE is_attack=1")
    attacks = cursor.fetchone()["attacks"]

    cursor.execute("""
        SELECT attack_type, COUNT(*) as cnt
        FROM alerts WHERE is_attack=1
        GROUP BY attack_type
        ORDER BY cnt DESC LIMIT 1
    """)
    row = cursor.fetchone()
    top_attack = row["attack_type"] if row else "None"

    cursor.execute("""
        SELECT severity, COUNT(*) as cnt
        FROM alerts WHERE is_attack=1
        GROUP BY severity
    """)
    severity_dist = {r["severity"]: r["cnt"] for r in cursor.fetchall()}

    cursor.execute("""
        SELECT attack_type, COUNT(*) as cnt
        FROM alerts WHERE is_attack=1
        GROUP BY attack_type
        ORDER BY cnt DESC
    """)
    attack_dist = {r["attack_type"]: r["cnt"] for r in cursor.fetchall()}

    conn.close()

    return {
        "total_analyzed" : total,
        "total_attacks"  : attacks,
        "total_benign"   : total - attacks,
        "attack_rate"    : round(attacks / total * 100, 2) if total > 0 else 0,
        "top_attack"     : top_attack,
        "severity_dist"  : severity_dist,
        "attack_dist"    : attack_dist,
    }
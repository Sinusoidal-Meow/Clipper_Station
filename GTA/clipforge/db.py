"""SQLite database for ClipForge."""

import sqlite3
from pathlib import Path
from clipforge.config import settings

def get_db():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            source_url TEXT,
            brand TEXT,
            status TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            meta TEXT
        );

        CREATE TABLE IF NOT EXISTS clips (
            id TEXT PRIMARY KEY,
            job_id TEXT,
            brand TEXT,
            start_time REAL,
            end_time REAL,
            duration REAL,
            score REAL,
            title TEXT,
            description TEXT,
            tags TEXT,
            status TEXT DEFAULT 'pending_review',
            file_path TEXT,
            created_at TIMESTAMP,
            meta TEXT,
            FOREIGN KEY(job_id) REFERENCES jobs(id)
        );
        """)
    conn.close()

init_db()
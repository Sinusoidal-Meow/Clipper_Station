"""SQLite database module for clipops."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from clipops.config import settings

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

        CREATE TABLE IF NOT EXISTS connected_accounts (
            id TEXT PRIMARY KEY,
            platform TEXT,
            brand TEXT,
            label TEXT,
            encrypted_token TEXT,
            created_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS analytics (
            id TEXT PRIMARY KEY,
            clip_id TEXT,
            platform TEXT,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            retention_rate REAL DEFAULT 0.0,
            synced_at TIMESTAMP,
            FOREIGN KEY(clip_id) REFERENCES clips(id)
        );

        CREATE TABLE IF NOT EXISTS rolling_buffer (
            id TEXT PRIMARY KEY,
            stream_name TEXT,
            chunk_path TEXT,
            duration REAL,
            recorded_at TIMESTAMP
        );
        """)
    conn.close()

init_db()

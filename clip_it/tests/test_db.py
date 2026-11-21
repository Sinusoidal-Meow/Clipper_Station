"""Tests for clipops.db module."""

import pytest
import sqlite3
from pathlib import Path
from clipops import db
from clipops.config import settings


class TestDatabase:
    def test_get_db_returns_connection(self):
        conn = db.get_db()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)
        conn.close()

    def test_database_file_created(self):
        conn = db.get_db()
        conn.close()
        if settings.DATABASE_PATH.exists():
            assert settings.DATABASE_PATH.stat().st_size > 0

    def test_init_db_tables(self):
        tables = ["jobs", "clips", "connected_accounts", "analytics", "rolling_buffer"]
        conn = db.get_db()
        for t in tables:
            row = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{t}'").fetchone()
            assert row is not None, f"Table {t} not created"
        conn.close()

    def test_insert_job(self):
        conn = db.get_db()
        conn.execute(
            "INSERT INTO jobs (id, source_url, brand, status, created_at) VALUES (?, ?, ?, ?, ?)",
            ("job_test", "https://youtube.com/watch?v=123", "gta", "processing", "2024-01-01 00:00:00")
        )
        row = conn.execute("SELECT * FROM jobs WHERE id='job_test'").fetchone()
        assert row is not None
        conn.execute("DELETE FROM jobs WHERE id='job_test'")
        conn.close()

    def test_insert_clip(self):
        conn = db.get_db()
        conn.execute(
            "INSERT INTO clips (id, job_id, brand, start_time, end_time, duration, score, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("clip_test", "job_test", "gta", 0.0, 5.0, 5.0, 0.85, "review")
        )
        row = conn.execute("SELECT * FROM clips WHERE id='clip_test'").fetchone()
        assert row is not None
        conn.execute("DELETE FROM clips WHERE id='clip_test'")
        conn.close()

    def test_joins(self):
        conn = db.get_db()
        conn.execute("INSERT INTO jobs (id, source_url, brand, status, created_at) VALUES ('join_test', 'url', 'gta', 'done', '2024-01-01')")
        conn.execute("INSERT INTO clips (id, job_id, brand, start_time, end_time, duration, score, status) VALUES ('join_clip', 'join_test', 'gta', 0, 3, 3, 0.9, 'done')")
        row = conn.execute("SELECT j.id as job_id, c.id as clip_id FROM jobs j JOIN clips c ON j.id = c.job_id WHERE j.id='join_test'").fetchone()
        assert row is not None
        conn.execute("DELETE FROM clips WHERE id='join_clip'")
        conn.execute("DELETE FROM jobs WHERE id='join_test'")
        conn.close()
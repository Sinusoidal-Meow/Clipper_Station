"""Tests for clipforge.db module."""

import pytest
import sqlite3
from clipforge import db
from clipforge.config import settings


class TestDatabase:
    def test_get_db_returns_connection(self):
        conn = db.get_db()
        assert hasattr(conn, "execute")
        assert conn is not None
        conn.close()

    def test_database_file_created(self):
        assert settings.DATABASE_PATH.exists()

    def test_init_db_tables(self):
        conn = db.get_db()
        tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        assert "jobs" in tables
        assert "clips" in tables
        conn.close()

    def test_insert_job(self):
        conn = db.get_db()
        conn.execute("DELETE FROM jobs WHERE id='test_insert'")
        conn.execute(
            "INSERT INTO jobs (id, source_url, brand, status, created_at) VALUES (?, ?, ?, ?, ?)",
            ("test_insert", "https://test.com", "gta", "done", "2024-01-01")
        )
        row = conn.execute("SELECT * FROM jobs WHERE id='test_insert'").fetchone()
        assert row is not None
        assert row["source_url"] == "https://test.com"
        conn.execute("DELETE FROM jobs WHERE id='test_insert'")
        conn.close()
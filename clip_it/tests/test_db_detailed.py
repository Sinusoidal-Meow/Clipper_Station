"""Detailed database tests."""

import pytest
import sqlite3
from clipops import db
from clipops.config import settings


class TestDatabaseConnection:
    def test_get_db_returns_dbapi_connection(self):
        conn = db.get_db()
        assert hasattr(conn, "execute")
        row = conn.execute("SELECT 1").fetchone()
        assert row is not None
        conn.close()

    def test_get_db_row_factory(self):
        conn = db.get_db()
        assert conn.row_factory is not None
        conn.close()

    def test_get_db_reusable(self):
        conn1 = db.get_db()
        conn2 = db.get_db()
        assert conn1 is not conn2
        conn1.close()
        conn2.close()


class TestDatabaseSchema:
    def test_jobs_table_columns(self):
        conn = db.get_db()
        cols = [d[1] for d in conn.execute("PRAGMA table_info(jobs)").fetchall()]
        assert "id" in cols
        assert "source_url" in cols
        assert "brand" in cols
        assert "status" in cols
        conn.close()

    def test_clips_table_columns(self):
        conn = db.get_db()
        cols = [d[1] for d in conn.execute("PRAGMA table_info(clips)").fetchall()]
        assert "id" in cols
        assert "job_id" in cols
        assert "score" in cols
        assert "status" in cols
        conn.close()

    def test_connected_accounts_columns(self):
        conn = db.get_db()
        cols = [d[1] for d in conn.execute("PRAGMA table_info(connected_accounts)").fetchall()]
        assert "platform" in cols
        assert "brand" in cols
        assert "encrypted_token" in cols
        conn.close()

    def test_analytics_table_columns(self):
        conn = db.get_db()
        cols = [d[1] for d in conn.execute("PRAGMA table_info(analytics)").fetchall()]
        assert "clip_id" in cols
        assert "views" in cols
        assert "likes" in cols
        conn.close()

    def test_rolling_buffer_columns(self):
        conn = db.get_db()
        cols = [d[1] for d in conn.execute("PRAGMA table_info(rolling_buffer)").fetchall()]
        assert "stream_name" in cols
        assert "chunk_path" in cols
        conn.close()


class TestDatabaseInsert:
    def test_insert_and_select_job(self):
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

    def test_insert_returns_none_on_missing(self):
        conn = db.get_db()
        row = conn.execute("SELECT * FROM jobs WHERE id='nonexistent_xyz'").fetchone()
        assert row is None
        conn.close()

    def test_insert_with_meta_json(self):
        conn = db.get_db()
        import json
        meta = json.dumps({"key": "value"})
        conn.execute(
            "INSERT INTO jobs (id, source_url, brand, status, created_at, meta) VALUES (?, ?, ?, ?, ?, ?)",
            ("test_meta", "url", "gta", "pending", "now", meta)
        )
        row = conn.execute("SELECT meta FROM jobs WHERE id='test_meta'").fetchone()
        assert json.loads(row["meta"]) == {"key": "value"}
        conn.execute("DELETE FROM jobs WHERE id='test_meta'")
        conn.close()


class TestDatabaseForeignKeys:
    def test_jobs_to_clips_fk(self):
        conn = db.get_db()
        conn.execute("DELETE FROM clips WHERE id='fk_test'")
        conn.execute("DELETE FROM jobs WHERE id='fk_test'")
        conn.execute("INSERT INTO jobs (id, source_url, brand, status, created_at) VALUES ('fk_test', 'url', 'gta', 'done', 'now')")
        conn.execute("INSERT INTO clips (id, job_id, brand, start_time, end_time, duration, score, status) VALUES ('fk_test_clip', 'fk_test', 'gta', 0, 5, 5, 0.8, 'done')")
        row = conn.execute("SELECT c.job_id, j.source_url FROM clips c JOIN jobs j ON c.job_id = j.id WHERE c.id='fk_test_clip'").fetchone()
        assert row is not None
        conn.execute("DELETE FROM clips WHERE id='fk_test_clip'")
        conn.execute("DELETE FROM jobs WHERE id='fk_test'")
        conn.close()


class TestDatabaseCleanup:
    def test_connection_cleanup(self):
        conn = db.get_db()
        conn.close()
        with pytest.raises(sqlite3.ProgrammingError):
            conn.execute("SELECT 1")
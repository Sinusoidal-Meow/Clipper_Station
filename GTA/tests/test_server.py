"""Tests for clipforge.server module."""

import pytest
from fastapi.testclient import TestClient
from clipforge.server import app


class TestServerHealth:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_health_200_status(self, client):
        r = client.get("/health")
        assert r.status_code == 200

    def test_health_json_content_type(self, client):
        r = client.get("/health")
        assert "application/json" in r.headers.get("content-type", "")

    def test_health_status_healthy(self, client):
        r = client.get("/health")
        assert r.json()["status"] == "healthy"


class TestServerEndpoints:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_process_endpoint_exists(self, client):
        r = client.post("/process", data={"source_url": "https://test.com", "brand": "gta"})
        assert r.status_code == 200

    def test_process_returns_clips(self, client):
        r = client.post("/process", data={"source_url": "https://test.com", "brand": "gta"})
        data = r.json()
        assert "clips" in data
        assert "job_id" in data

    def test_clips_endpoint_exists(self, client):
        r = client.get("/clips/gta")
        assert r.status_code == 200

    def test_dashboard_returns_html(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert "GTA ClipForge" in r.text


class TestStaticFiles:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_static_mount_exists(self, client):
        mount_paths = [route.path for route in app.routes if hasattr(route, 'path')]
        assert "/static" in mount_paths
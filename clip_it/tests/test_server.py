"""Tests for clipops.server module."""

import pytest
from fastapi.testclient import TestClient
from clipops.server import app


class TestServerHealth:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_dashboard_homepage(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "Clip Operations Center" in response.text or "dashboard" in response.text.lower()

    def test_docs_endpoint(self, client):
        response = client.get("/docs")
        assert response.status_code == 200


class TestServerEndpoints:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_list_clips_empty(self, client):
        response = client.get("/clips/gta")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_clips_podcast(self, client):
        response = client.get("/clips/podcast")
        assert response.status_code == 200

    def test_list_clips_invalid_brand(self, client):
        response = client.get("/clips/invalid_brand_12345")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_process_clip_returns_json(self, client):
        response = client.post("/process", data={
            "source_url": "https://youtube.com/watch?v=1",
            "brand": "gta",
            "max_clips": 1
        })
        assert response.status_code == 200
        data = response.json()
        assert "source_url" in data
        assert "clips" in data

    def test_clip_review(self, client):
        response = client.post("/clip", data={
            "clip_id": "test_clip_1",
            "action": "approve",
            "note": "Good clip"
        })
        assert response.status_code == 200


class TestServerMiddleware:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_cors_headers(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_content_type_json(self, client):
        response = client.get("/health")
        assert "application/json" in response.headers.get("content-type", "")
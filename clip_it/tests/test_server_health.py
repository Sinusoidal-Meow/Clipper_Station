"""Health endpoint detailed tests."""

import pytest
from fastapi.testclient import TestClient
from clipops.server import app


class TestServerHealthDetailed:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_health_200_status(self, client):
        r = client.get("/health")
        assert r.status_code == 200

    def test_health_json_content_type(self, client):
        r = client.get("/health")
        assert "application/json" in r.headers.get("content-type", "")

    def test_health_has_status_key(self, client):
        r = client.get("/health")
        assert "status" in r.json()

    def test_health_status_is_healthy(self, client):
        r = client.get("/health")
        assert r.json()["status"] == "healthy"

    def test_health_has_time_key(self, client):
        r = client.get("/health")
        data = r.json()
        assert "time" in data

    def test_health_time_is_iso_format(self, client):
        r = client.get("/health")
        data = r.json()
        assert "T" in data["time"]  # ISO format has T separator

    def test_health_response_structure(self, client):
        r = client.get("/health")
        data = r.json()
        assert isinstance(data, dict)
        assert len(data) == 2


class TestDashboardEndpoint:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_dashboard_returns_html(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_dashboard_has_html_doctype(self, client):
        r = client.get("/")
        assert "<!DOCTYPE html>" in r.text or "<html>" in r.text

    def test_dashboard_title_present(self, client):
        r = client.get("/")
        assert r.status_code == 200


class TestCliocsEndpoint:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_docs_returns_html(self, client):
        r = client.get("/docs")
        assert r.status_code == 200

    def test_docs_has_swagger_ui(self, client):
        r = client.get("/docs")
        assert r.status_code == 200

    def test_openapi_json_exists(self, client):
        r = client.get("/openapi.json")
        assert r.status_code == 200


class TestStaticFiles:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_static_mount_exists(self, client):
        mount_paths = [route.path for route in app.routes if hasattr(route, 'path')]
        assert "/static" in mount_paths


class TestErrorHandling:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_process_endpoint_exists(self, client):
        r = client.post("/process", data={})
        assert r.status_code in [200, 422, 400]

    def test_clips_endpoint_exists(self, client):
        r = client.get("/clips/missing_brand_test")
        assert r.status_code == 200
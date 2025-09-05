"""Tests for the main application module."""

import pytest
from fastapi.testclient import TestClient
from src import __version__


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == __version__
    assert "Claude Code Sample API" in data["message"]


def test_api_docs_accessible(client: TestClient):
    """Test that API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_redoc_accessible(client: TestClient):
    """Test that ReDoc documentation is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
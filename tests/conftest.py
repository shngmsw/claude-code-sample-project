"""Test configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.utils import items_db, next_id


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the in-memory database before each test."""
    global next_id
    items_db.clear()
    next_id = 1
    yield
    items_db.clear()
    next_id = 1


@pytest.fixture
def sample_item_data():
    """Sample item data for testing."""
    return {
        "title": "Test Item",
        "description": "A test item",
        "price": 29.99,
        "is_active": True
    }
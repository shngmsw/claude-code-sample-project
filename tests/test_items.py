"""Tests for item-related functionality."""

import pytest
from fastapi.testclient import TestClient
from src.utils import create_item


def test_create_item(client: TestClient, sample_item_data):
    """Test creating a new item."""
    response = client.post("/items/", json=sample_item_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == sample_item_data["title"]
    assert data["description"] == sample_item_data["description"]
    assert data["price"] == sample_item_data["price"]
    assert data["is_active"] == sample_item_data["is_active"]
    assert "id" in data


def test_get_item(client: TestClient, sample_item_data):
    """Test retrieving a specific item."""
    # Create an item first
    created_item = create_item(sample_item_data)
    item_id = created_item["id"]
    
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == sample_item_data["title"]


def test_get_nonexistent_item(client: TestClient):
    """Test retrieving a nonexistent item."""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_get_all_items(client: TestClient, sample_item_data):
    """Test retrieving all items."""
    # Create a few items
    for i in range(3):
        item_data = sample_item_data.copy()
        item_data["title"] = f"Test Item {i+1}"
        create_item(item_data)
    
    response = client.get("/items/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3
    assert all(item["title"].startswith("Test Item") for item in data)


def test_get_items_with_pagination(client: TestClient, sample_item_data):
    """Test retrieving items with pagination."""
    # Create 5 items
    for i in range(5):
        item_data = sample_item_data.copy()
        item_data["title"] = f"Test Item {i+1}"
        create_item(item_data)
    
    # Get first 2 items
    response = client.get("/items/?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Get next 2 items
    response = client.get("/items/?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_update_item(client: TestClient, sample_item_data):
    """Test updating an existing item."""
    # Create an item first
    created_item = create_item(sample_item_data)
    item_id = created_item["id"]
    
    # Update the item
    update_data = {
        "title": "Updated Title",
        "price": 39.99
    }
    
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["price"] == 39.99
    assert data["description"] == sample_item_data["description"]  # Unchanged


def test_update_nonexistent_item(client: TestClient):
    """Test updating a nonexistent item."""
    update_data = {"title": "Updated Title"}
    response = client.put("/items/999", json=update_data)
    assert response.status_code == 404


def test_delete_item(client: TestClient, sample_item_data):
    """Test deleting an item."""
    # Create an item first
    created_item = create_item(sample_item_data)
    item_id = created_item["id"]
    
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
    
    # Verify item is deleted
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404


def test_delete_nonexistent_item(client: TestClient):
    """Test deleting a nonexistent item."""
    response = client.delete("/items/999")
    assert response.status_code == 404


def test_create_item_validation(client: TestClient):
    """Test item creation with invalid data."""
    invalid_data = {
        "title": "",  # Empty title should fail
        "price": -10  # Negative price should fail
    }
    
    response = client.post("/items/", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_create_item_missing_required_fields(client: TestClient):
    """Test item creation with missing required fields."""
    incomplete_data = {
        "description": "Missing title and price"
    }
    
    response = client.post("/items/", json=incomplete_data)
    assert response.status_code == 422
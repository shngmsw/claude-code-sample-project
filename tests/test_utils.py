"""Tests for utility functions."""

import pytest
from src.utils import (
    create_item,
    get_item,
    get_all_items,
    update_item,
    delete_item,
    get_next_id,
    items_db
)


def test_create_item(sample_item_data):
    """Test item creation."""
    item = create_item(sample_item_data)
    
    assert "id" in item
    assert item["title"] == sample_item_data["title"]
    assert item["description"] == sample_item_data["description"]
    assert item["price"] == sample_item_data["price"]
    assert item["is_active"] == sample_item_data["is_active"]


def test_get_next_id():
    """Test ID generation."""
    id1 = get_next_id()
    id2 = get_next_id()
    
    assert isinstance(id1, int)
    assert isinstance(id2, int)
    assert id2 == id1 + 1


def test_get_item(sample_item_data):
    """Test item retrieval."""
    created_item = create_item(sample_item_data)
    item_id = created_item["id"]
    
    retrieved_item = get_item(item_id)
    assert retrieved_item is not None
    assert retrieved_item["id"] == item_id
    assert retrieved_item["title"] == sample_item_data["title"]


def test_get_nonexistent_item():
    """Test retrieving a nonexistent item."""
    item = get_item(999)
    assert item is None


def test_get_all_items(sample_item_data):
    """Test retrieving all items."""
    # Create multiple items
    items = []
    for i in range(3):
        item_data = sample_item_data.copy()
        item_data["title"] = f"Item {i+1}"
        items.append(create_item(item_data))
    
    all_items = get_all_items()
    assert len(all_items) == 3
    assert all(item["title"].startswith("Item") for item in all_items)


def test_get_all_items_pagination(sample_item_data):
    """Test item retrieval with pagination."""
    # Create 5 items
    for i in range(5):
        item_data = sample_item_data.copy()
        item_data["title"] = f"Item {i+1}"
        create_item(item_data)
    
    # Test pagination
    page1 = get_all_items(skip=0, limit=2)
    assert len(page1) == 2
    
    page2 = get_all_items(skip=2, limit=2)
    assert len(page2) == 2
    
    page3 = get_all_items(skip=4, limit=2)
    assert len(page3) == 1


def test_update_item(sample_item_data):
    """Test item update."""
    created_item = create_item(sample_item_data)
    item_id = created_item["id"]
    
    update_data = {
        "title": "Updated Title",
        "price": 39.99
    }
    
    updated_item = update_item(item_id, update_data)
    assert updated_item is not None
    assert updated_item["title"] == "Updated Title"
    assert updated_item["price"] == 39.99
    assert updated_item["description"] == sample_item_data["description"]  # Unchanged


def test_update_nonexistent_item():
    """Test updating a nonexistent item."""
    result = update_item(999, {"title": "Updated"})
    assert result is None


def test_delete_item(sample_item_data):
    """Test item deletion."""
    created_item = create_item(sample_item_data)
    item_id = created_item["id"]
    
    # Item should exist
    assert get_item(item_id) is not None
    
    # Delete the item
    success = delete_item(item_id)
    assert success is True
    
    # Item should no longer exist
    assert get_item(item_id) is None


def test_delete_nonexistent_item():
    """Test deleting a nonexistent item."""
    success = delete_item(999)
    assert success is False
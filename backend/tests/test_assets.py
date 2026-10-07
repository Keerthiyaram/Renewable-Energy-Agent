import pytest
from datetime import datetime


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_create_asset(client):
    """Test creating a renewable asset."""
    asset_data = {
        "asset_id": "TEST-SOLAR-001",
        "name": "Test Solar Plant",
        "asset_type": "solar",
        "installed_capacity_mw": 5.0,
        "location": "Test Location",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "operational_status": "operational"
    }
    response = client.post("/assets/", json=asset_data)
    assert response.status_code == 201
    data = response.json()
    assert data["asset_id"] == "TEST-SOLAR-001"
    assert data["name"] == "Test Solar Plant"
    assert data["installed_capacity_mw"] == 5.0
    assert "id" in data


def test_create_duplicate_asset(client):
    """Test that duplicate asset_id is rejected."""
    asset_data = {
        "asset_id": "TEST-DUP-001",
        "name": "Test Duplicate",
        "asset_type": "solar",
        "installed_capacity_mw": 5.0,
        "operational_status": "operational"
    }
    # Create first asset
    response1 = client.post("/assets/", json=asset_data)
    assert response1.status_code == 201
    
    # Try to create duplicate
    response2 = client.post("/assets/", json=asset_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]


def test_get_assets(client):
    """Test getting all assets."""
    # Create multiple assets
    for i in range(3):
        asset_data = {
            "asset_id": f"TEST-GET-{i}",
            "name": f"Test Asset {i}",
            "asset_type": "solar",
            "installed_capacity_mw": 5.0,
            "operational_status": "operational"
        }
        client.post("/assets/", json=asset_data)
    
    response = client.get("/assets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_get_asset_by_id(client):
    """Test getting a specific asset."""
    asset_data = {
        "asset_id": "TEST-GET-BY-ID",
        "name": "Test Get By ID",
        "asset_type": "wind",
        "installed_capacity_mw": 6.0,
        "operational_status": "operational"
    }
    create_response = client.post("/assets/", json=asset_data)
    asset_id = create_response.json()["asset_id"]
    
    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["asset_id"] == asset_id
    assert data["name"] == "Test Get By ID"


def test_get_nonexistent_asset(client):
    """Test getting a non-existent asset."""
    response = client.get("/assets/NONEXISTENT")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_asset(client):
    """Test updating an asset."""
    asset_data = {
        "asset_id": "TEST-UPDATE",
        "name": "Test Update",
        "asset_type": "solar",
        "installed_capacity_mw": 5.0,
        "operational_status": "operational"
    }
    create_response = client.post("/assets/", json=asset_data)
    asset_id = create_response.json()["asset_id"]
    
    update_data = {
        "name": "Updated Name",
        "installed_capacity_mw": 7.0
    }
    response = client.put(f"/assets/{asset_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["installed_capacity_mw"] == 7.0


def test_delete_asset(client):
    """Test deleting an asset."""
    asset_data = {
        "asset_id": "TEST-DELETE",
        "name": "Test Delete",
        "asset_type": "solar",
        "installed_capacity_mw": 5.0,
        "operational_status": "operational"
    }
    client.post("/assets/", json=asset_data)
    
    response = client.delete("/assets/TEST-DELETE")
    assert response.status_code == 204
    
    # Verify deletion
    get_response = client.get("/assets/TEST-DELETE")
    assert get_response.status_code == 404


def test_invalid_asset_type(client):
    """Test that invalid asset type is rejected."""
    asset_data = {
        "asset_id": "TEST-INVALID-TYPE",
        "name": "Test Invalid Type",
        "asset_type": "nuclear",  # Invalid type
        "installed_capacity_mw": 5.0,
        "operational_status": "operational"
    }
    response = client.post("/assets/", json=asset_data)
    assert response.status_code == 422


def test_invalid_capacity(client):
    """Test that negative capacity is rejected."""
    asset_data = {
        "asset_id": "TEST-INVALID-CAP",
        "name": "Test Invalid Capacity",
        "asset_type": "solar",
        "installed_capacity_mw": -5.0,  # Invalid
        "operational_status": "operational"
    }
    response = client.post("/assets/", json=asset_data)
    assert response.status_code == 422

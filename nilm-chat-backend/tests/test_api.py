import sys
import os
import pytest
from fastapi.testclient import TestClient
import uuid

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data

def test_metrics_summary():
    response = client.get("/api/metrics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_devices" in data
    assert "total_power" in data
    assert "avg_power_factor" in data
    assert "avg_thd" in data
    assert "timestamp" in data

def test_devices_endpoint():
    response = client.get("/api/devices/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # If we have devices, check their structure
    if len(response.json()) > 0:
        device = response.json()[0]
        assert "id" in device
        assert "name" in device
        assert "cluster" in device
        assert "typical_power" in device

def test_chat_endpoint():
    # Create a simple chat request
    session_id = str(uuid.uuid4())
    request_data = {
        "message": "What's my current power usage?",
        "session_id": session_id
    }
    
    response = client.post("/api/chat/", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "session_id" in data
    assert data["session_id"] == session_id

    # Test getting chat history
    history_response = client.get(f"/api/chat/history/{session_id}")
    assert history_response.status_code == 200
    history = history_response.json()
    
    # Should have at least two messages (user and assistant)
    assert len(history) >= 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"
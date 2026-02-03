import json
import pytest
from pathlib import Path
from httpx import AsyncClient, ASGITransport

from app.main import app
import app.api.log_query as log_query

TEST_LOGS = [
    {
        "timestamp": "2026-01-01T00:00:00Z",
        "level": "INFO",
        "service": "auth",
        "event": "login",
        "message": "User login",
    },
    {
        "timestamp": "2026-01-01T00:01:00Z",
        "level": "ERROR",
        "service": "payment",
        "event": "charge_failed",
        "message": "Payment failed",
    },
]

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def temp_log_file(tmp_path, monkeypatch):
    log_file = tmp_path / "test.log.jsonl"

    with open(log_file, "w", encoding="utf-8") as f:
        for log in TEST_LOGS:
            f.write(json.dumps(log) + "\n")
    

    monkeypatch.setattr(log_query, "LOG_FILE_PATH", str(log_file))

    return log_file

@pytest.mark.asyncio
async def test_get_all_logs(temp_log_file, async_client):

    response = await async_client.get("/logs/")
    
    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 2
    assert len(data["data"]) == 2


@pytest.mark.asyncio
async def test_get_filter_by_levels(temp_log_file, async_client):

    response = await async_client.get("/logs/?level=ERROR")

    data = response.json()
    assert data["total"] == 1
    assert data["data"][0]["service"] == "payment"

@pytest.mark.asyncio
async def test_pagination(temp_log_file, async_client):

    response = await async_client.get("/logs/?limit=1")

    data = response.json()

    assert len(data["data"]) == 1
    assert data["total"] == 2

@pytest.mark.asyncio
async def test_get_levels(temp_log_file, async_client):
    response = await async_client.get("/logs/levels")

    levels = response.json()["levels"]

    assert "INFO" in levels
    assert "ERROR" in levels

@pytest.mark.asyncio
async def test_get_services(temp_log_file, async_client):
    response = await async_client.get("/logs/services")

    services = response.json()["services"]

    assert "auth" in services
    assert "payment" in services


@pytest.mark.asyncio
async def test_clear_logs(temp_log_file, async_client):
    await async_client.delete("/logs/")

    assert not temp_log_file.exists()

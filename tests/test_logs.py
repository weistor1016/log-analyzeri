import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_ingest_log_success():
    payload = {
        "timestamp": "2026-01-22T10:15:30Z",
        "level": "INFO",
        "service": "auth",
        "event": "login",
        "message": "User logged in",
    }

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post("/logs/", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "accepted"}


@pytest.mark.asyncio
async def test_ingest_log_invalid_level():
    payload = {
        "timestamp": "2026-01-22T10:15:30Z",
        "level": "INVALID",
        "service": "auth",
        "event": "login",
        "message": "User logged in",
    }

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post("/logs/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid log level"

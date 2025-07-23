"""Integration tests for wallet API endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI

from app.models.wallet_request import Base
from app.main import app
from app.db.database import get_db

# Set up in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override dependency to use testing database."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the default dependency in the app
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def client():
    """Create asynchronous test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


class TestWalletAPI:
    """Integration tests for wallet API endpoints."""

    @pytest.mark.asyncio
    async def test_post_wallet_info_success(self, client):
        """Test POST /api/v1/wallet/info with valid address returns status 200."""
        # Arrange - Mock address
        payload = {
            "address": "TTestAddress123456789012345678901234567890"
        }

        # Act
        response = await client.post("/api/v1/wallet/info", json=payload)

        # Assert
        assert response.status_code == 200
        assert "address" in response.json()

    @pytest.mark.asyncio
    async def test_post_wallet_info_invalid_address(self, client):
        """Test POST /api/v1/wallet/info with invalid address returns 400."""
        # Arrange - Invalid address
        payload = {
            "address": "InvalidAddress!"
        }

        # Act
        response = await client.post("/api/v1/wallet/info", json=payload)

        # Assert
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_get_wallet_requests(self, client):
        """Test GET /api/v1/wallet/requests returns paginated records."""

        # Act
        response = await client.get("/api/v1/wallet/requests?page=1&page_size=10")

        # Assert
        assert response.status_code == 200
        assert "records" in response.json()
        assert "page" in response.json()

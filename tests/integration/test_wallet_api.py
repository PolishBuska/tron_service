"""Integration tests for wallet API endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI

from app.models.wallet_request import Base
from app.main import app
from app.db.database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tron_wallet.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override dependency to use testing database."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Setup database for each test."""
    # Recreate tables for each test to ensure clean state
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestWalletAPI:
    """Integration tests for wallet API endpoints."""

    @pytest.mark.asyncio
    async def test_post_wallet_info_with_invalid_checksum(self):
        """Test POST /api/v1/wallet/info with invalid TRON address checksum."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            payload = {
                "address": "TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZYH12345678"
            }

            response = await client.post("/api/v1/wallet/info", json=payload)

            assert response.status_code == 500
            assert "Invalid TRON address" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_post_wallet_info_invalid_address(self):
        """Test POST /api/v1/wallet/info with invalid address returns validation error."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            payload = {
                "address": "InvalidAddress!"
            }

            response = await client.post("/api/v1/wallet/info", json=payload)

            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_wallet_requests(self):
        """Test GET /api/v1/wallet/requests returns paginated records."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/wallet/requests?page=1&page_size=10")

            assert response.status_code == 200
            assert "records" in response.json()
            assert "page" in response.json()

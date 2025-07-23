"""Unit tests for wallet service database operations."""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.wallet_request import Base, WalletRequest
from app.schemas.wallet import WalletInfoResponse
from app.services.wallet_service import WalletService
from app.services.tron_service import TronService


@pytest.fixture
def in_memory_db():
    """Create in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return TestingSessionLocal()


@pytest.fixture
def mock_tron_service():
    """Create mock TRON service."""
    return Mock(spec=TronService)


@pytest.fixture
def wallet_service(mock_tron_service):
    """Create wallet service with mocked dependencies."""
    return WalletService(mock_tron_service)


class TestWalletService:
    """Unit tests for WalletService database operations."""
    
    def test_save_wallet_request_success(self, wallet_service, in_memory_db):
        """Test successful saving of wallet request to database."""
        # Arrange
        address = "TTestAddress123456789012345678901234567890"
        wallet_info = WalletInfoResponse(
            address=address,
            balance=100.5,
            bandwidth=1000.0,
            energy=500.0
        )
        
        # Act
        result = wallet_service._save_wallet_request(
            db=in_memory_db,
            address=address,
            wallet_info=wallet_info
        )
        
        # Assert
        assert result.id is not None
        assert result.address == address
        assert result.balance == 100.5
        assert result.bandwidth == 1000.0
        assert result.energy == 500.0
        assert result.error_message is None
        assert result.response_data is not None
        assert result.request_timestamp is not None
        
        # Verify record was saved to database
        saved_record = in_memory_db.query(WalletRequest).filter_by(address=address).first()
        assert saved_record is not None
        assert saved_record.address == address
        assert saved_record.balance == 100.5
    
    def test_save_wallet_request_with_error(self, wallet_service, in_memory_db):
        """Test saving wallet request with error message."""
        # Arrange
        address = "TTestAddress123456789012345678901234567890"
        wallet_info = WalletInfoResponse(
            address=address,
            balance=None,
            bandwidth=None,
            energy=None
        )
        error_message = "TRON network error"
        
        # Act
        result = wallet_service._save_wallet_request(
            db=in_memory_db,
            address=address,
            wallet_info=wallet_info,
            error_message=error_message
        )
        
        # Assert
        assert result.id is not None
        assert result.address == address
        assert result.balance is None
        assert result.bandwidth is None
        assert result.energy is None
        assert result.error_message == error_message
        assert result.response_data is None
        
        # Verify record was saved to database
        saved_record = in_memory_db.query(WalletRequest).filter_by(address=address).first()
        assert saved_record is not None
        assert saved_record.error_message == error_message
    
    def test_get_wallet_requests_pagination(self, wallet_service, in_memory_db):
        """Test pagination of wallet requests retrieval."""
        # Arrange - Create test records
        addresses = [f"TTestAddress{i:036d}" for i in range(15)]
        for address in addresses:
            wallet_info = WalletInfoResponse(
                address=address,
                balance=float(100 + len(address)),
                bandwidth=1000.0,
                energy=500.0
            )
            wallet_service._save_wallet_request(
                db=in_memory_db,
                address=address,
                wallet_info=wallet_info
            )
        
        # Act - Get first page
        page1_result = wallet_service.get_wallet_requests(
            db=in_memory_db,
            page=1,
            page_size=10
        )
        
        # Assert - First page
        assert page1_result.total == 15
        assert page1_result.page == 1
        assert page1_result.page_size == 10
        assert page1_result.total_pages == 2
        assert len(page1_result.records) == 10
        
        # Act - Get second page
        page2_result = wallet_service.get_wallet_requests(
            db=in_memory_db,
            page=2,
            page_size=10
        )
        
        # Assert - Second page
        assert page2_result.total == 15
        assert page2_result.page == 2
        assert page2_result.page_size == 10
        assert page2_result.total_pages == 2
        assert len(page2_result.records) == 5
    
    def test_get_wallet_requests_empty_database(self, wallet_service, in_memory_db):
        """Test retrieval from empty database."""
        # Act
        result = wallet_service.get_wallet_requests(
            db=in_memory_db,
            page=1,
            page_size=10
        )
        
        # Assert
        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 10
        assert result.total_pages == 1
        assert len(result.records) == 0

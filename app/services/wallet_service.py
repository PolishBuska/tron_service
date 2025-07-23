"""Wallet service for business logic and database operations."""

import json
import math
from datetime import datetime
from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.exceptions import DatabaseException
from app.models.wallet_request import WalletRequest
from app.schemas.wallet import WalletInfoResponse, WalletRequestRecord, WalletRequestsResponse
from app.services.tron_service import TronService


class WalletService:
    """Service for wallet-related business logic."""
    
    def __init__(self, tron_service: TronService):
        """Initialize wallet service with dependencies."""
        self.tron_service = tron_service
    
    async def get_wallet_info_and_save(self, address: str, db: Session) -> WalletInfoResponse:
        """Get wallet information from TRON network and save request to database."""
        error_message = None
        wallet_info = None
        
        try:
            # Get wallet information from TRON network
            wallet_info = await self.tron_service.get_wallet_info(address)
        except Exception as e:
            error_message = str(e)
            # Create empty wallet info for failed requests
            wallet_info = WalletInfoResponse(
                address=address,
                balance=None,
                bandwidth=None,
                energy=None
            )
        
        # Save request to database
        try:
            self._save_wallet_request(
                db=db,
                address=address,
                wallet_info=wallet_info,
                error_message=error_message
            )
        except Exception as e:
            raise DatabaseException(f"Failed to save wallet request: {str(e)}")
        
        # If there was an error getting wallet info, re-raise it after saving
        if error_message:
            raise Exception(error_message)
        
        return wallet_info
    
    def _save_wallet_request(
        self,
        db: Session,
        address: str,
        wallet_info: WalletInfoResponse,
        error_message: str = None
    ) -> WalletRequest:
        """Save wallet request to database."""
        try:
            # Prepare response data
            response_data = None
            if not error_message:
                response_data = json.dumps({
                    "address": wallet_info.address,
                    "balance": wallet_info.balance,
                    "bandwidth": wallet_info.bandwidth,
                    "energy": wallet_info.energy
                })
            
            # Create wallet request record
            wallet_request = WalletRequest(
                address=address,
                balance=wallet_info.balance,
                bandwidth=wallet_info.bandwidth,
                energy=wallet_info.energy,
                request_timestamp=datetime.utcnow(),
                response_data=response_data,
                error_message=error_message
            )
            
            db.add(wallet_request)
            db.commit()
            db.refresh(wallet_request)
            
            return wallet_request
            
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Failed to save wallet request: {str(e)}")
    
    def get_wallet_requests(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 10
    ) -> WalletRequestsResponse:
        """Get paginated list of wallet requests from database."""
        try:
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Get total count
            total = db.query(WalletRequest).count()
            
            # Get paginated records
            records = (
                db.query(WalletRequest)
                .order_by(desc(WalletRequest.request_timestamp))
                .offset(offset)
                .limit(page_size)
                .all()
            )
            
            # Convert to response schema
            wallet_records = [
                WalletRequestRecord(
                    id=record.id,
                    address=record.address,
                    balance=record.balance,
                    bandwidth=record.bandwidth,
                    energy=record.energy,
                    request_timestamp=record.request_timestamp,
                    error_message=record.error_message
                )
                for record in records
            ]
            
            # Calculate total pages
            total_pages = math.ceil(total / page_size) if total > 0 else 1
            
            return WalletRequestsResponse(
                records=wallet_records,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )
            
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve wallet requests: {str(e)}")


def get_wallet_service(tron_service: TronService) -> WalletService:
    """Dependency injection for WalletService."""
    return WalletService(tron_service)

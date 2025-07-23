"""API routes for wallet operations."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.exceptions import (
    InvalidAddressException,
    TronNetworkException,
    DatabaseException
)
from app.db.database import get_db
from app.schemas.wallet import (
    WalletAddressRequest,
    WalletInfoResponse,
    WalletRequestsResponse,
    PaginationParams
)
from app.services.tron_service import get_tron_service, TronService
from app.services.wallet_service import get_wallet_service, WalletService

router = APIRouter(prefix="/api/v1/wallet", tags=["wallet"])


@router.post("/info", response_model=WalletInfoResponse)
async def get_wallet_info(
    request: WalletAddressRequest,
    db: Session = Depends(get_db),
    tron_service: TronService = Depends(get_tron_service)
) -> WalletInfoResponse:
    """Get wallet information including balance, bandwidth, and energy.
    
    This endpoint retrieves information about a TRON wallet address including:
    - TRX balance
    - Available bandwidth
    - Available energy
    
    Each request is logged to the database for audit purposes.
    """
    try:
        wallet_service = get_wallet_service(tron_service)
        return await wallet_service.get_wallet_info_and_save(request.address, db)
        
    except InvalidAddressException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TronNetworkException as e:
        raise HTTPException(status_code=502, detail=f"TRON network error: {str(e)}")
    except DatabaseException as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/requests", response_model=WalletRequestsResponse)
async def get_wallet_requests(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
    tron_service: TronService = Depends(get_tron_service)
) -> WalletRequestsResponse:
    """Get paginated list of wallet requests.
    
    This endpoint returns a paginated list of all wallet information requests
    that have been made to the service, including successful and failed requests.
    """
    try:
        wallet_service = get_wallet_service(tron_service)
        return wallet_service.get_wallet_requests(db, page, page_size)
        
    except DatabaseException as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

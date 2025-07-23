"""TRON network service for blockchain interactions."""

import asyncio
from typing import Dict, Any, Optional
from tronpy import Tron
from tronpy.exceptions import ValidationError, ApiError, BadAddress

from app.core.config import settings
from app.core.exceptions import InvalidAddressException, TronNetworkException
from app.schemas.wallet import WalletInfoResponse


class TronService:
    """Service for interacting with TRON blockchain."""
    
    def __init__(self):
        """Initialize TRON service with network configuration."""
        self._client = self._create_client()
    
    def _create_client(self) -> Tron:
        """Create TRON client based on network configuration."""
        try:
            if settings.tron_network == "mainnet":
                return Tron()
            elif settings.tron_network == "shasta":
                return Tron(network="shasta")
            elif settings.tron_network == "nile":
                return Tron(network="nile")
            else:
                raise TronNetworkException(f"Unsupported network: {settings.tron_network}")
        except Exception as e:
            raise TronNetworkException(f"Failed to create TRON client: {str(e)}")
    
    async def validate_address(self, address: str) -> bool:
        """Validate TRON address format asynchronously."""
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._client.is_address, address)
        except Exception:
            return False
    
    async def get_wallet_info(self, address: str) -> WalletInfoResponse:
        """Get wallet information including balance, bandwidth, and energy."""
        if not await self.validate_address(address):
            raise InvalidAddressException(f"Invalid TRON address: {address}")
        
        try:
            loop = asyncio.get_event_loop()
            
            account_info = await loop.run_in_executor(
                None, self._client.get_account, address
            )
            
            balance_sun = account_info.get('balance', 0)
            balance_trx = balance_sun / 1_000_000
            
            resources = await loop.run_in_executor(
                None, self._client.get_account_resource, address
            )
            
            bandwidth = self._get_bandwidth_info(resources)
            energy = self._get_energy_info(resources)
            
            return WalletInfoResponse(
                address=address,
                balance=balance_trx,
                bandwidth=bandwidth,
                energy=energy
            )
            
        except (ValidationError, BadAddress) as e:
            raise InvalidAddressException(f"Invalid address format: {str(e)}")
        except ApiError as e:
            raise TronNetworkException(f"TRON network error: {str(e)}")
        except Exception as e:
            raise TronNetworkException(f"Unexpected error: {str(e)}")
    
    def _get_bandwidth_info(self, resources: Dict[str, Any]) -> Optional[float]:
        """Extract bandwidth information from account resources."""
        try:
            free_bandwidth_limit = resources.get('freeNetLimit', 0)
            free_bandwidth_used = resources.get('freeNetUsed', 0)
            free_bandwidth_available = free_bandwidth_limit - free_bandwidth_used
            
            acquired_bandwidth_limit = resources.get('NetLimit', 0)
            acquired_bandwidth_used = resources.get('NetUsed', 0)
            acquired_bandwidth_available = acquired_bandwidth_limit - acquired_bandwidth_used
            
            return max(0, free_bandwidth_available + acquired_bandwidth_available)
        except Exception:
            return None
    
    def _get_energy_info(self, resources: Dict[str, Any]) -> Optional[float]:
        """Extract energy information from account resources."""
        try:
            energy_limit = resources.get('EnergyLimit', 0)
            energy_used = resources.get('EnergyUsed', 0)
            return max(0, energy_limit - energy_used)
        except Exception:
            return None


def get_tron_service() -> TronService:
    """Dependency injection for TronService."""
    return TronService()

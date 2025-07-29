"""
Backward compatibility wrapper for SePayBanking.
This allows you to replace the old implementation while keeping the same interface.
"""

from typing import Optional
from finkeith.clients.sepay_client import SePayClient
from finkeith.services.sepay_banking_service import SePayBankingService


def create_sepay_banking(api_key: Optional[str] = None) -> SePayBankingService:
    """
    Factory function to create a SePay banking service.
    
    This maintains the same interface as the old SePayBanking class
    but uses the new DTO-based architecture underneath.
    """
    client = SePayClient(api_key=api_key)
    return SePayBankingService(client)


# Alias for backward compatibility
SePayBanking = create_sepay_banking

from typing import Protocol, Optional
from datetime import datetime

from finkeith.clients.dtos.sepay_dtos import (
    SePayTransactionListResponseDTO,
    SePayTransactionCountResponseDTO,
    SePaySingleTransactionResponseDTO
)


class ISePayClient(Protocol):
    """Protocol for SePay API client that returns DTOs."""
    
    async def get_transactions(
        self,
        account_number: str,
        transaction_date_from: Optional[datetime] = None,
        transaction_date_to: Optional[datetime] = None,
        limit: Optional[int] = None,
        reference_id: Optional[str] = None,
        amount_in: Optional[float] = None,
        amount_out: Optional[float] = None
    ) -> SePayTransactionListResponseDTO:
        """Get transactions from SePay API and return DTOs."""
        ...

    async def get_transactions_count(
        self,
        account_number: str,
        transaction_date_from: Optional[datetime] = None,
        transaction_date_to: Optional[datetime] = None,
        id_from: Optional[str] = None
    ) -> SePayTransactionCountResponseDTO:
        """Get transaction count from SePay API."""
        ...

    async def get_transaction_by_id(
        self,
        transaction_id: str
    ) -> SePaySingleTransactionResponseDTO:
        """Get single transaction by ID from SePay API."""
        ...

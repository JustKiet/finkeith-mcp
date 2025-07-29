"""
Banking API request and response schemas.
"""

from typing import Optional, List
from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, field_validator
from pydantic.types import PositiveInt

from finkeith.schemas.base import BaseResponseModel


# ========== Request Schemas ==========

class TransactionHistoryRequest(BaseModel):
    """Request schema for transaction history."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )
    
    account_number: str = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="Bank account number",
        examples=["1234567890"]
    )
    
    transaction_date_from: Optional[datetime] = Field(
        None,
        description="Start date for transaction history (inclusive)",
        examples=["2025-01-01T00:00:00Z"]
    )
    
    transaction_date_to: Optional[datetime] = Field(
        None,
        description="End date for transaction history (inclusive)",
        examples=["2025-01-31T23:59:59Z"]
    )
    
    limit: Optional[PositiveInt] = Field(
        None,
        le=1000,
        description="Maximum number of transactions to return (max 1000)",
        examples=[100]
    )
    
    reference_id: Optional[str] = Field(
        None,
        max_length=100,
        description="Filter by reference ID",
        examples=["REF123456"]
    )
    
    amount_in: Optional[Decimal] = Field(
        None,
        ge=0,
        decimal_places=2,
        description="Filter by incoming amount",
        examples=[1000000.00]
    )
    
    amount_out: Optional[Decimal] = Field(
        None,
        ge=0,
        decimal_places=2,
        description="Filter by outgoing amount",
        examples=[500000.00]
    )

    @field_validator('transaction_date_to')
    @classmethod
    def validate_date_range(cls, v, info):
        """Validate that end date is after start date."""
        if v and info.data.get('transaction_date_from'):
            if v < info.data['transaction_date_from']:
                raise ValueError('transaction_date_to must be after transaction_date_from')
        return v


class TransactionCountRequest(BaseModel):
    """Request schema for transaction count."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )
    
    account_number: str = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="Bank account number",
        examples=["1234567890"]
    )
    
    transaction_date_from: Optional[datetime] = Field(
        None,
        description="Start date for counting transactions (inclusive)"
    )
    
    transaction_date_to: Optional[datetime] = Field(
        None,
        description="End date for counting transactions (inclusive)"
    )
    
    id_from: Optional[str] = Field(
        None,
        max_length=100,
        description="Count transactions starting from this ID"
    )


class BalanceRequest(BaseModel):
    """Request schema for account balance."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )
    
    account_number: str = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="Bank account number",
        examples=["1234567890"]
    )


class TransactionDetailRequest(BaseModel):
    """Request schema for single transaction details."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )
    
    transaction_id: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Unique transaction identifier",
        examples=["tx_123456789"]
    )


# ========== Response Schemas ==========

class TransactionResponse(BaseResponseModel):
    """Response schema for a single transaction."""
    
    id: str = Field(..., description="Unique transaction identifier")
    transaction_date: datetime = Field(..., description="Transaction date and time")
    account_number: str = Field(..., description="Account number")
    bank_name: str = Field(..., description="Bank name")
    sub_account: Optional[str] = Field(None, description="Sub-account identifier")
    
    amount_in: Decimal = Field(
        ..., 
        ge=0, 
        decimal_places=2,
        description="Incoming amount"
    )
    amount_out: Decimal = Field(
        ..., 
        ge=0, 
        decimal_places=2,
        description="Outgoing amount"
    )
    accumulated: Decimal = Field(
        ..., 
        decimal_places=2,
        description="Accumulated balance after transaction"
    )
    
    code: Optional[str] = Field(None, description="Transaction code")
    transaction_content: Optional[str] = Field(None, description="Transaction description")
    reference_number: Optional[str] = Field(None, description="Transaction reference number")


class TransactionHistoryResponse(BaseResponseModel):
    """Response schema for transaction history."""
    
    transactions: List[TransactionResponse] = Field(
        ..., 
        description="List of transactions"
    )
    total_count: int = Field(
        ..., 
        ge=0,
        description="Total number of transactions found"
    )


class BalanceResponse(BaseResponseModel):
    """Response schema for account balance."""
    
    account_number: str = Field(..., description="Account number")
    balance: Decimal = Field(
        ..., 
        decimal_places=2,
        description="Current account balance"
    )
    currency: str = Field(
        default="VND", 
        description="Currency code"
    )
    as_of: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Balance as of this timestamp"
    )


class TransactionCountResponse(BaseResponseModel):
    """Response schema for transaction count."""
    
    account_number: str = Field(..., description="Account number")
    count: int = Field(
        ..., 
        ge=0,
        description="Number of transactions"
    )
    filters_applied: dict = Field(
        default_factory=dict,
        description="Summary of filters that were applied"
    )


# ========== Query Parameter Schemas ==========

class PaginationParams(BaseModel):
    """Query parameters for pagination."""
    
    page: PositiveInt = Field(
        default=1,
        description="Page number (1-based)",
        examples=[1]
    )
    
    per_page: PositiveInt = Field(
        default=20,
        le=100,
        description="Items per page (max 100)",
        examples=[20]
    )

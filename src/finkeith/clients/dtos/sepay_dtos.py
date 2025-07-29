from dataclasses import dataclass
from typing import Optional


@dataclass
class SePayTransactionDTO:
    """Data Transfer Object for SePay transaction response."""
    id: str
    transaction_date: str
    account_number: str
    bank_brand_name: str
    sub_account: Optional[str] = None
    amount_in: Optional[float] = None
    amount_out: Optional[float] = None
    accumulated: Optional[float] = None
    code: Optional[str] = None
    transaction_content: Optional[str] = None
    reference_number: Optional[str] = None


@dataclass
class SePayTransactionListResponseDTO:
    """Data Transfer Object for SePay transaction list response."""
    transactions: list[SePayTransactionDTO]


@dataclass
class SePayTransactionCountResponseDTO:
    """Data Transfer Object for SePay transaction count response."""
    count_transactions: int


@dataclass
class SePaySingleTransactionResponseDTO:
    """Data Transfer Object for SePay single transaction response."""
    transaction: Optional[SePayTransactionDTO]

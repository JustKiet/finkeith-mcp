from typing import Optional
from datetime import datetime

from finkeith.core.interfaces.ibanking import IBanking
from finkeith.core.entities.transactions import Transaction
from finkeith.core.common.banks import SupportedBank
from finkeith.clients.interfaces.isepay_client import ISePayClient
from finkeith.clients.dtos.sepay_dtos import SePayTransactionDTO
from finkeith.utils.bank_mapping import BankMapping

class SePayBankingService(IBanking):
    """Service that converts SePay DTOs to domain entities and implements banking interface."""

    def __init__(self, sepay_client: ISePayClient):
        self._client = sepay_client

    def _dto_to_domain_entity(self, dto: SePayTransactionDTO) -> Transaction:
        """Convert SePay DTO to domain Transaction entity."""
        return Transaction(
            id=dto.id,
            transaction_date=datetime.fromisoformat(dto.transaction_date),
            account_number=dto.account_number,
            bank_name=BankMapping.map_bank_name(dto.bank_brand_name),
            sub_account=dto.sub_account,
            amount_in=float(dto.amount_in or 0.0),
            amount_out=float(dto.amount_out or 0.0),
            accumulated=float(dto.accumulated or 0.0),
            code=dto.code,
            transaction_content=dto.transaction_content,
            reference_number=dto.reference_number
        )

    async def get_transaction_history(
        self,
        account_number: str,
        transaction_date_from: Optional[datetime] = None,
        transaction_date_to: Optional[datetime] = None,
        limit: Optional[int] = None,
        reference_id: Optional[str] = None,
        amount_in: Optional[float] = None,
        amount_out: Optional[float] = None
    ) -> list[Transaction]:
        """Get transaction history and convert DTOs to domain entities."""
        response = await self._client.get_transactions(
            account_number=account_number,
            transaction_date_from=transaction_date_from,
            transaction_date_to=transaction_date_to,
            limit=limit,
            reference_id=reference_id,
            amount_in=amount_in,
            amount_out=amount_out
        )

        return [
            self._dto_to_domain_entity(dto)
            for dto in response.transactions
        ]

    async def get_transactions_count(
        self,
        account_number: str,
        transaction_date_from: Optional[datetime] = None,
        transaction_date_to: Optional[datetime] = None,
        id_from: Optional[str] = None
    ) -> int:
        """Get transaction count."""
        response = await self._client.get_transactions_count(
            account_number=account_number,
            transaction_date_from=transaction_date_from,
            transaction_date_to=transaction_date_to,
            id_from=id_from
        )
        return response.count_transactions

    async def get_transaction(
        self,
        transaction_id: str
    ) -> Optional[Transaction]:
        """Get single transaction and convert DTO to domain entity."""
        response = await self._client.get_transaction_by_id(transaction_id)
        
        if response.transaction:
            return self._dto_to_domain_entity(response.transaction)
        return None

    async def get_balance(
        self,
        account_number: str
    ) -> float:
        """Get account balance by analyzing transaction history."""
        transactions = await self.get_transaction_history(account_number=account_number)

        if not transactions:
            return 0.0

        if transactions[-1].accumulated != 0.0:
            return transactions[-1].accumulated

        # Calculate balance from transaction amounts
        total_in = sum(t.amount_in for t in transactions)
        total_out = sum(t.amount_out for t in transactions)
        return total_in - total_out

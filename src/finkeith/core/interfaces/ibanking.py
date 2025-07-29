from finkeith.core.entities.transactions import Transaction

from datetime import datetime
from typing import Protocol, Optional

class IBanking(Protocol):
    async def get_transaction_history(
        self, 
        account_number: str,
        transaction_date_from: Optional[datetime],
        transaction_date_to: Optional[datetime],
        limit: Optional[int] = None,
        reference_id: Optional[str] = None,
        amount_in: Optional[float] = None,
        amount_out: Optional[float] = None
    ) -> list[Transaction]:
        """
        Retrieve the transaction history for the specified account.
        
        :param str account_number: The account number to retrieve transactions for.
        :param Optional[datetime] transaction_date_from: Start date for filtering transactions.
        :param Optional[datetime] transaction_date_to: End date for filtering transactions.
        :param Optional[int] limit: Maximum number of transactions to retrieve.
        :param Optional[str] reference_id: Filter by a specific reference ID.
        :param Optional[float] amount_in: Filter by incoming transaction amount.
        :param Optional[float] amount_out: Filter by outgoing transaction amount.
        :return: A list of transactions matching the criteria.
        :rtype: list[Transaction]
        :raises IBankingServiceError: If there is an error retrieving the transaction history.
        """
        ...

    async def get_transactions_count(
        self,
        account_number: str,
        transaction_date_from: Optional[datetime] = None,
        transaction_date_to: Optional[datetime] = None,
        id_from: Optional[str] = None
    ) -> int:
        """
        Count the number of transactions for the specified account.
        
        :param str account_number: The account number to count transactions for.
        :param Optional[datetime] transaction_date_from: Start date for filtering transactions.
        :param Optional[datetime] transaction_date_to: End date for filtering transactions.
        :param Optional[str] id_from: Filter transactions starting from a specific ID.
        :return: The count of transactions matching the criteria.
        :rtype: int
        :raises IBankingServiceError: If there is an error counting the transactions.
        """
        ...

    async def get_transaction(
        self,
        transaction_id: str
    ) -> Optional[Transaction]:
        """
        Retrieve a specific transaction by its ID.
        
        :param str transaction_id: The ID of the transaction to retrieve.
        :return: The transaction object if found, otherwise None.
        :rtype: Optional[Transaction]
        :raises IBankingServiceError: If there is an error retrieving the transaction.
        """
        ...

    async def get_balance(
        self,
        account_number: str
    ) -> float:
        """
        Retrieve the current balance for the specified account.

        :param str account_number: The account number to retrieve the balance for.
        :return: The current balance of the account.
        :rtype: float
        :raises IBankingServiceError: If there is an error retrieving the balance.
        """
        ...
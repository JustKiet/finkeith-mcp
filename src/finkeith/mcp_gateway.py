from finkeith.api.v1.banking import (
    get_transaction_history as get_transaction_history_api,
    get_account_balance as get_account_balance_api,
    get_transaction_count as get_transaction_count_api,
    get_transaction_details as get_transaction_details_api,
)
from finkeith.schemas.common import Date
from finkeith.schemas.base import SuccessResponse
from finkeith.schemas.banking import (
    TransactionHistoryRequest,
    TransactionHistoryResponse,
    TransactionCountRequest,
    TransactionCountResponse,
    BalanceRequest,
    BalanceResponse,
    TransactionResponse,
)
from finkeith.dependencies import get_banking_service
from finkeith.config import settings
from decimal import Decimal

from fastapi import HTTPException
from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import Optional

mcp = FastMCP(
    "FinKeith",
    host=settings.MCP_HOST,
    port=settings.MCP_PORT,
)

@mcp.tool(
    title="Get Transaction History",
    description="Retrieve transaction history for a specific account.",
)
async def get_transaction_history(
    account_number: str,
    date_from: Optional[Date] = None,
    date_to: Optional[Date] = None,
    amount_in: Optional[float] = None,
    amount_out: Optional[float] = None,
    limit: Optional[int] = None,
) -> SuccessResponse[TransactionHistoryResponse]:
    """
    Get transaction history for a specific account.

    :param account_number: The account number to retrieve transactions for.
    :param date_from: Optional start date for filtering transactions.
    :param date_to: Optional end date for filtering transactions.
    :param amount_in: Optional filter for incoming transaction amounts.
    :param amount_out: Optional filter for outgoing transaction amounts.
    :param limit: Optional limit on the number of transactions to retrieve.
    :return: A response containing the transaction history.
    """
    try:
        payload = TransactionHistoryRequest(
            account_number=account_number,
            limit=limit,
            transaction_date_from=date_from.to_datetime() if date_from else None,
            transaction_date_to=date_to.to_datetime() if date_to else None,
            reference_id=None,
            amount_in=Decimal(amount_in) if amount_in else None,
            amount_out=Decimal(amount_out) if amount_out else None
        )
        banking_service = get_banking_service()
        transactions = await get_transaction_history_api(
            request=payload,
            banking_service=await banking_service
        )

        return transactions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving transaction history: {str(e)}"
        )

@mcp.tool(
    title="Get Account Balance",
    description="Retrieve the current balance of a specific account.",
)
async def get_account_balance(
    account_number: str,
) -> SuccessResponse[BalanceResponse]:
    """
    Get the current balance of a specific account.

    :param account_number: The account number to retrieve the balance for.
    :return: The current balance of the account.
    """
    try:
        payload = BalanceRequest(account_number=account_number)
        banking_service = get_banking_service()
        balance = await get_account_balance_api(
            request=payload,
            banking_service=await banking_service
        )

        return balance
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving account balance: {str(e)}"
        )

@mcp.tool(
    title="Get Transaction Count",
    description="Retrieve the number of transactions for a specific account.",
)
async def get_transaction_count(
    account_number: str,
    transaction_date_from: Optional[datetime] = None,
    transaction_date_to: Optional[datetime] = None,
) -> SuccessResponse[TransactionCountResponse]:
    """
    Get the count of transactions for a specific account.

    :param account_number: The account number to retrieve the transaction count for.
    :param transaction_date_from: Optional start date for filtering transactions.
    :param transaction_date_to: Optional end date for filtering transactions.
    :return: The count of transactions for the specified account.
    """
    try:
        payload = TransactionCountRequest(
            account_number=account_number,
            transaction_date_from=transaction_date_from,
            transaction_date_to=transaction_date_to,
            id_from=None  # Optional, can be used to start counting from a specific transaction ID
        )
        banking_service = get_banking_service()
        count = await get_transaction_count_api(
            request=payload,
            banking_service=await banking_service
        )

        return count
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving transaction count: {str(e)}"
        )

@mcp.tool(
    title="Get Transaction Details",
    description="Retrieve detailed information about a specific transaction.",
)
async def get_transaction_details(
    transaction_id: str,
) -> SuccessResponse[TransactionResponse]:
    """
    Get detailed information about a specific transaction. ONLY use if you have the transaction ID.

    :param transaction_id: The ID of the transaction to retrieve details for.
    :return: Detailed information about the specified transaction.
    """
    try:
        banking_service = get_banking_service()
        transaction_details = await get_transaction_details_api(
            transaction_id=transaction_id,
            banking_service=await banking_service
        )

        return transaction_details
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving transaction details: {str(e)}"
        )

if __name__ == "__main__":
    mcp.run(transport="sse")
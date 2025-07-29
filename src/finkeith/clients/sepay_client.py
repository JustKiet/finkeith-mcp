from typing import Optional, Any
from datetime import datetime
import httpx
import os

from finkeith.core.exceptions import MissingAPIKeyError, IBankingServiceError
from finkeith.clients.interfaces.isepay_client import ISePayClient
from finkeith.clients.dtos.sepay_dtos import (
    SePayTransactionDTO,
    SePayTransactionListResponseDTO,
    SePayTransactionCountResponseDTO,
    SePaySingleTransactionResponseDTO
)


class SePayClient(ISePayClient):
    """SePay API client that returns DTOs (Data Transfer Objects)."""

    def __init__(self, api_key: Optional[str] = None):
        if not api_key:
            api_key = os.getenv("SEPAY_API_KEY")

        if not api_key:
            raise MissingAPIKeyError(
                "API key is required for SePayService. "
                "Please set the `SEPAY_API_KEY` environment variable or pass it as an argument."
            )

        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self._base_url = "https://my.sepay.vn/userapi"

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
        try:
            params: dict[str, Any] = {
                "account_number": account_number,
                "transaction_date_min": transaction_date_from,
                "transaction_date_max": transaction_date_to,
                "limit": limit,
                "reference_id": reference_id,
                "amount_in": amount_in,
                "amount_out": amount_out,
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=f"{self._base_url}/transactions/list",
                    params=params,
                    headers=self._headers
                )
                response.raise_for_status()

            data = response.json()
            transactions_data = data.get("transactions", [])

            transaction_dtos = [
                SePayTransactionDTO(
                    id=tx["id"],
                    transaction_date=tx["transaction_date"],
                    account_number=tx["account_number"],
                    bank_brand_name=tx["bank_brand_name"],
                    sub_account=tx.get("sub_account"),
                    amount_in=tx.get("amount_in"),
                    amount_out=tx.get("amount_out"),
                    accumulated=tx.get("accumulated"),
                    code=tx.get("code"),
                    transaction_content=tx.get("transaction_content"),
                    reference_number=tx.get("reference_number")
                )
                for tx in transactions_data
            ]

            return SePayTransactionListResponseDTO(transactions=transaction_dtos)

        except httpx.HTTPStatusError as e:
            raise IBankingServiceError(
                f"HTTP error occurred: {e.response.status_code} - {e.response}"
            ) from e
        except httpx.RequestError as e:
            raise IBankingServiceError(f"Request error occurred: {str(e)}") from e
        except Exception as e:
            raise IBankingServiceError(f"An unexpected error occurred: {str(e)}") from e

    async def get_transactions_count(
        self,
        account_number: str,
        transaction_date_from: Optional[datetime] = None,
        transaction_date_to: Optional[datetime] = None,
        id_from: Optional[str] = None
    ) -> SePayTransactionCountResponseDTO:
        """Get transaction count from SePay API."""
        try:
            params: dict[str, Any] = {
                "account_number": account_number,
                "transaction_date_min": transaction_date_from,
                "transaction_date_max": transaction_date_to,
                "since_id": id_from
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=f"{self._base_url}/transactions/count",
                    params=params,
                    headers=self._headers
                )
                response.raise_for_status()

            data = response.json()
            count = data.get("count_transactions", 0)

            return SePayTransactionCountResponseDTO(count_transactions=count)

        except httpx.HTTPStatusError as e:
            raise IBankingServiceError(
                f"HTTP error occurred: {e.response.status_code} - {e.response}"
            ) from e
        except httpx.RequestError as e:
            raise IBankingServiceError(f"Request error occurred: {str(e)}") from e
        except Exception as e:
            raise IBankingServiceError(f"An unexpected error occurred: {str(e)}") from e

    async def get_transaction_by_id(
        self,
        transaction_id: str
    ) -> SePaySingleTransactionResponseDTO:
        """Get single transaction by ID from SePay API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=f"{self._base_url}/transactions/{transaction_id}",
                    headers=self._headers
                )
                response.raise_for_status()

            data = response.json()
            transaction_data = data.get("transaction")

            transaction_dto = None
            if transaction_data:
                transaction_dto = SePayTransactionDTO(
                    id=transaction_data["id"],
                    transaction_date=transaction_data["transaction_date"],
                    account_number=transaction_data["account_number"],
                    bank_brand_name=transaction_data["bank_name"],  # Note: different field name
                    sub_account=transaction_data.get("sub_account"),
                    amount_in=transaction_data.get("amount_in"),
                    amount_out=transaction_data.get("amount_out"),
                    accumulated=transaction_data.get("accumulated"),
                    code=transaction_data.get("code"),
                    transaction_content=transaction_data.get("transaction_content"),
                    reference_number=transaction_data.get("reference_number")
                )

            return SePaySingleTransactionResponseDTO(transaction=transaction_dto)

        except httpx.HTTPStatusError as e:
            raise IBankingServiceError(
                f"HTTP error occurred: {e.response.status_code} - {e.response}"
            ) from e
        except httpx.RequestError as e:
            raise IBankingServiceError(f"Request error occurred: {str(e)}") from e
        except Exception as e:
            raise IBankingServiceError(f"An unexpected error occurred: {str(e)}") from e

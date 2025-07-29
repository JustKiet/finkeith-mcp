import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime
from typing import Any, Dict

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from finkeith.clients.sepay_client import SePayClient
from finkeith.services.sepay_banking_service import SePayBankingService
from finkeith.clients.dtos.sepay_dtos import SePayTransactionDTO, SePayTransactionListResponseDTO
from finkeith.core.entities.transactions import Transaction
from finkeith.core.exceptions import MissingAPIKeyError, IBankingServiceError


class TestSePayNewArchitecture:
    """Test suite for new SePay architecture (Client + Service)."""

    @pytest.fixture
    def mock_api_key(self) -> str:
        return "test_api_key_123"

    @pytest.fixture
    def sepay_client(self, mock_api_key: str) -> SePayClient:
        return SePayClient(api_key=mock_api_key)

    @pytest.fixture
    def sepay_service(self, sepay_client: SePayClient) -> SePayBankingService:
        return SePayBankingService(sepay_client)

    @pytest.fixture
    def sample_transaction_dto(self) -> SePayTransactionDTO:
        return SePayTransactionDTO(
            id="tx_123456",
            transaction_date="2025-01-15T10:30:00",
            account_number="1234567890",
            bank_brand_name="MBBANK",
            sub_account="001",
            amount_in=1000000.0,
            amount_out=0.0,
            accumulated=5000000.0,
            code="TXN001",
            transaction_content="Test transfer",
            reference_number="REF123456"
        )

    @pytest.mark.asyncio
    async def test_client_returns_dtos(self, sepay_client: SePayClient, sample_transaction_dto: SePayTransactionDTO):
        """Test that client returns DTOs."""
        mock_response_data = {
            "transactions": [{
                "id": "tx_123456",
                "transaction_date": "2025-01-15T10:30:00",
                "account_number": "1234567890",
                "bank_brand_name": "MBBANK",
                "sub_account": "001",
                "amount_in": 1000000.0,
                "amount_out": 0.0,
                "accumulated": 5000000.0,
                "code": "TXN001",
                "transaction_content": "Test transfer",
                "reference_number": "REF123456"
            }]
        }

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            response = await sepay_client.get_transactions(account_number="1234567890")

            assert isinstance(response, SePayTransactionListResponseDTO)
            assert len(response.transactions) == 1
            assert isinstance(response.transactions[0], SePayTransactionDTO)
            assert response.transactions[0].id == "tx_123456"

    @pytest.mark.asyncio
    async def test_service_returns_domain_entities(self, sepay_service: SePayBankingService):
        """Test that service returns domain entities."""
        mock_response_data = {
            "transactions": [{
                "id": "tx_123456",
                "transaction_date": "2025-01-15T10:30:00",
                "account_number": "1234567890",
                "bank_brand_name": "MBBANK",
                "amount_in": 1000000.0,
                "amount_out": 0.0,
                "accumulated": 5000000.0,
            }]
        }

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            transactions = await sepay_service.get_transaction_history(account_number="1234567890")

            assert len(transactions) == 1
            assert isinstance(transactions[0], Transaction)
            assert transactions[0].id == "tx_123456"


if __name__ == "__main__":
    pytest.main([__file__])

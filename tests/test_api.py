"""
API integration tests.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from finkeith.app import app
from finkeith.api.v1.banking import get_banking_service
from finkeith.core.entities.transactions import Transaction
from finkeith.core.common.banks import SupportedBank
from datetime import datetime


class TestBankingAPI:
    """Test suite for Banking API endpoints."""

    @pytest.fixture
    def client(self):
        """FastAPI test client."""
        return TestClient(app)

    @pytest.fixture
    def mock_transaction(self):
        """Mock transaction entity."""
        return Transaction(
            id="tx_123456",
            transaction_date=datetime(2025, 1, 15, 10, 30, 0),
            account_number="1234567890",
            bank_name=SupportedBank.MBBANK,
            sub_account="001",
            amount_in=1000000.0,
            amount_out=0.0,
            accumulated=5000000.0,
            code="TXN001",
            transaction_content="Test transfer",
            reference_number="REF123456"
        )

    @pytest.fixture
    def mock_banking_service(self):
        """Mock banking service."""
        return AsyncMock()

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data

    def test_health_endpoint(self, client):
        """Test health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_banking_health_endpoint(self, client, mock_banking_service):
        """Test banking health endpoint."""
        app.dependency_overrides[get_banking_service] = lambda: mock_banking_service
        
        try:
            response = client.get("/v1/banking/health")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "data" in data
        finally:
            app.dependency_overrides.clear()

    def test_transaction_history_success(self, client, mock_banking_service, mock_transaction):
        """Test successful transaction history retrieval."""
        mock_banking_service.get_transaction_history.return_value = [mock_transaction]
        app.dependency_overrides[get_banking_service] = lambda: mock_banking_service

        try:
            payload = {
                "account_number": "1234567890",
                "limit": 10
            }

            response = client.post("/v1/banking/transactions/history", json=payload)
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] is True
            assert "data" in data
            assert len(data["data"]["transactions"]) == 1
            
            transaction = data["data"]["transactions"][0]
            assert transaction["id"] == "tx_123456"
            assert transaction["account_number"] == "1234567890"
        finally:
            app.dependency_overrides.clear()

    def test_transaction_count_success(self, client, mock_banking_service):
        """Test successful transaction count."""
        mock_banking_service.get_transactions_count.return_value = 25
        app.dependency_overrides[get_banking_service] = lambda: mock_banking_service

        try:
            payload = {
                "account_number": "1234567890"
            }

            response = client.post("/v1/banking/transactions/count", json=payload)
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] is True
            assert data["data"]["count"] == 25
        finally:
            app.dependency_overrides.clear()

    def test_account_balance_success(self, client, mock_banking_service):
        """Test successful balance retrieval."""
        mock_banking_service.get_balance.return_value = 5000000.0
        app.dependency_overrides[get_banking_service] = lambda: mock_banking_service

        try:
            payload = {
                "account_number": "1234567890"
            }

            response = client.post("/v1/banking/account/balance", json=payload)
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] is True
            assert float(data["data"]["balance"]) == 5000000.0
        finally:
            app.dependency_overrides.clear()

    def test_transaction_details_success(self, client, mock_banking_service, mock_transaction):
        """Test successful transaction details retrieval."""
        mock_banking_service.get_transaction.return_value = mock_transaction
        app.dependency_overrides[get_banking_service] = lambda: mock_banking_service

        try:
            response = client.get("/v1/banking/transactions/tx_123456")
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] is True
            assert data["data"]["id"] == "tx_123456"
        finally:
            app.dependency_overrides.clear()

    def test_transaction_details_not_found(self, client, mock_banking_service):
        """Test transaction details when transaction not found."""
        mock_banking_service.get_transaction.return_value = None
        app.dependency_overrides[get_banking_service] = lambda: mock_banking_service

        try:
            response = client.get("/v1/banking/transactions/nonexistent")
            assert response.status_code == 404
        finally:
            app.dependency_overrides.clear()

    def test_validation_error(self, client, mock_banking_service):
        """Test validation error handling."""
        app.dependency_overrides[get_banking_service] = lambda: mock_banking_service

        try:
            # Missing required field
            payload = {}

            response = client.post("/v1/banking/transactions/history", json=payload)
            assert response.status_code == 422
            
            data = response.json()
            assert data["success"] is False
            assert "error" in data
            assert "details" in data
        finally:
            app.dependency_overrides.clear()

    def test_invalid_account_number(self, client, mock_banking_service):
        """Test validation with invalid account number."""
        app.dependency_overrides[get_banking_service] = lambda: mock_banking_service

        try:
            payload = {
                "account_number": "",  # Empty string should fail validation
            }

            response = client.post("/v1/banking/transactions/history", json=payload)
            assert response.status_code == 422
        finally:
            app.dependency_overrides.clear()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

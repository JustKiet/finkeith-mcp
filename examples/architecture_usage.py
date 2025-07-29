# Example usage of the new DTO-based architecture

from finkeith.clients.sepay_client import SePayClient
from finkeith.services.sepay_banking_service import SePayBankingService

# Usage example
async def example_usage():
    # 1. Create the client (returns DTOs)
    sepay_client = SePayClient(api_key="your_api_key")
    
    # 2. Create the service (converts DTOs to domain entities)
    banking_service = SePayBankingService(sepay_client)
    
    # 3. Use the service (returns domain entities)
    transactions = await banking_service.get_transaction_history(
        account_number="1234567890"
    )
    
    # 4. Work with domain entities
    for transaction in transactions:
        print(f"Transaction {transaction.id}: {transaction.amount_in}")


# Direct client usage (returns DTOs)
async def direct_client_usage():
    client = SePayClient(api_key="your_api_key")
    
    # Returns DTOs - useful for API integration tests
    response = await client.get_transactions(account_number="1234567890")
    
    for transaction_dto in response.transactions:
        print(f"DTO: {transaction_dto.id} - {transaction_dto.bank_brand_name}")

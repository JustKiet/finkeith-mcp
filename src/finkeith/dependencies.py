from finkeith.clients.sepay_client import SePayClient
from finkeith.services.sepay_banking_service import SePayBankingService
from finkeith.core.exceptions import MissingAPIKeyError
from finkeith.cologger import Cologger
from finkeith.config import settings

from fastapi import HTTPException, status

logger = Cologger(__name__).get_logger()

# Dependency injection
async def get_banking_service() -> SePayBankingService:
    """Get banking service instance."""
    try:
        client = SePayClient(api_key=settings.SEPAY_API_KEY)  # Will use environment variable for API key
        return SePayBankingService(client)
    except MissingAPIKeyError as e:
        logger.error(f"Banking service initialization failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Banking service is not properly configured"
        )
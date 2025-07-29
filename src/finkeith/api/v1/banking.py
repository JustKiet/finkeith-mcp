"""
Banking API endpoints.
"""

from typing import Annotated
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status

from finkeith.schemas.base import SuccessResponse, ErrorResponse, HealthResponse, HealthStatus
from finkeith.schemas.banking import (
    TransactionHistoryRequest,
    TransactionHistoryResponse,
    TransactionCountRequest,
    TransactionCountResponse,
    BalanceRequest,
    BalanceResponse,
    TransactionResponse,
)
from finkeith.services.sepay_banking_service import SePayBankingService
from finkeith.core.exceptions import IBankingServiceError
from finkeith.dependencies import get_banking_service
from finkeith.cologger import Cologger

logger = Cologger(__name__).get_logger()

# Create router
router = APIRouter(
    prefix="/v1/banking",
    tags=["Banking"],
    responses={
        404: {"model": ErrorResponse, "description": "Resource not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

# Health check endpoint
@router.get(
    "/health",
    response_model=SuccessResponse[HealthResponse],
    summary="Health Check",
    description="Check the health status of the banking service"
)
async def health_check():
    """Health check endpoint for banking service."""
    try:
        # Try to initialize the service to check if API key is configured
        await get_banking_service()
        health_status = HealthStatus.HEALTHY
        services = {"sepay_api": "healthy"}
    except Exception as e:
        logger.warning(f"Health check failed: {e}")
        health_status = HealthStatus.DEGRADED
        services = {"sepay_api": "unhealthy"}
    
    health_data = HealthResponse(
        status=health_status,
        version="1.0.0",
        services=services
    )
    
    return SuccessResponse(
        success=True,
        data=health_data,
        message="Health check completed"
    )


# Transaction history endpoint
@router.post(
    "/transactions/history",
    response_model=SuccessResponse[TransactionHistoryResponse],
    summary="Get Transaction History",
    description="Retrieve transaction history for a bank account with optional filters",
    status_code=status.HTTP_200_OK
)
async def get_transaction_history(
    request: TransactionHistoryRequest,
    banking_service: Annotated[SePayBankingService, Depends(get_banking_service)]
):
    """
    Get transaction history for a bank account.
    
    - **account_number**: Bank account number (required)
    - **transaction_date_from**: Start date for filtering (optional)
    - **transaction_date_to**: End date for filtering (optional)
    - **limit**: Maximum number of transactions to return (optional, max 1000)
    - **reference_id**: Filter by reference ID (optional)
    - **amount_in**: Filter by incoming amount (optional)
    - **amount_out**: Filter by outgoing amount (optional)
    """
    try:
        logger.info(f"Getting transaction history for account: {request.account_number}")
        
        transactions = await banking_service.get_transaction_history(
            account_number=request.account_number,
            transaction_date_from=request.transaction_date_from,
            transaction_date_to=request.transaction_date_to,
            limit=request.limit,
            reference_id=request.reference_id,
            amount_in=float(request.amount_in) if request.amount_in else None,
            amount_out=float(request.amount_out) if request.amount_out else None
        )
        
        # Convert domain entities to response DTOs
        transaction_responses = [
            TransactionResponse(
                id=t.id,
                transaction_date=t.transaction_date,
                account_number=t.account_number,
                bank_name=t.bank_name.value,
                sub_account=t.sub_account,
                amount_in=Decimal(str(t.amount_in)),
                amount_out=Decimal(str(t.amount_out)),
                accumulated=Decimal(str(t.accumulated)),
                code=t.code,
                transaction_content=t.transaction_content,
                reference_number=t.reference_number
            )
            for t in transactions
        ]
        
        response_data = TransactionHistoryResponse(
            transactions=transaction_responses,
            total_count=len(transaction_responses)
        )
        
        logger.info(f"Successfully retrieved {len(transaction_responses)} transactions")
        
        return SuccessResponse(
            success=True,
            data=response_data,
            message=f"Retrieved {len(transaction_responses)} transactions"
        )
        
    except IBankingServiceError as e:
        logger.error(f"Banking service error: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Banking service error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


# Transaction count endpoint
@router.post(
    "/transactions/count",
    response_model=SuccessResponse[TransactionCountResponse],
    summary="Get Transaction Count",
    description="Get the count of transactions for a bank account with optional filters",
    status_code=status.HTTP_200_OK
)
async def get_transaction_count(
    request: TransactionCountRequest,
    banking_service: Annotated[SePayBankingService, Depends(get_banking_service)]
):
    """
    Get the count of transactions for a bank account.
    
    - **account_number**: Bank account number (required)
    - **transaction_date_from**: Start date for filtering (optional)
    - **transaction_date_to**: End date for filtering (optional)
    - **id_from**: Count transactions starting from this ID (optional)
    """
    try:
        logger.info(f"Getting transaction count for account: {request.account_number}")
        
        count = await banking_service.get_transactions_count(
            account_number=request.account_number,
            transaction_date_from=request.transaction_date_from,
            transaction_date_to=request.transaction_date_to,
            id_from=request.id_from
        )
        
        filters_applied = {
            "account_number": request.account_number,
            "transaction_date_from": request.transaction_date_from.isoformat() if request.transaction_date_from else None,
            "transaction_date_to": request.transaction_date_to.isoformat() if request.transaction_date_to else None,
            "id_from": request.id_from
        }
        # Remove None values
        filters_applied = {k: v for k, v in filters_applied.items() if v is not None}
        
        response_data = TransactionCountResponse(
            account_number=request.account_number,
            count=count,
            filters_applied=filters_applied
        )
        
        logger.info(f"Successfully retrieved transaction count: {count}")
        
        return SuccessResponse(
            success=True,
            data=response_data,
            message=f"Found {count} transactions"
        )
        
    except IBankingServiceError as e:
        logger.error(f"Banking service error: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Banking service error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


# Account balance endpoint
@router.post(
    "/account/balance",
    response_model=SuccessResponse[BalanceResponse],
    summary="Get Account Balance",
    description="Get the current balance for a bank account",
    status_code=status.HTTP_200_OK
)
async def get_account_balance(
    request: BalanceRequest,
    banking_service: Annotated[SePayBankingService, Depends(get_banking_service)]
):
    """
    Get the current balance for a bank account.
    
    - **account_number**: Bank account number (required)
    """
    try:
        logger.info(f"Getting balance for account: {request.account_number}")
        
        balance = await banking_service.get_balance(account_number=request.account_number)
        
        response_data = BalanceResponse(
            account_number=request.account_number,
            balance=Decimal(str(balance)),
            currency="VND"
        )
        
        logger.info(f"Successfully retrieved balance: {balance}")
        
        return SuccessResponse(
            success=True,
            data=response_data,
            message="Balance retrieved successfully"
        )
        
    except IBankingServiceError as e:
        logger.error(f"Banking service error: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Banking service error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


# Single transaction endpoint
@router.get(
    "/transactions/{transaction_id}",
    response_model=SuccessResponse[TransactionResponse],
    summary="Get Transaction Details",
    description="Get details for a specific transaction by ID",
    status_code=status.HTTP_200_OK
)
async def get_transaction_details(
    transaction_id: str,
    banking_service: Annotated[SePayBankingService, Depends(get_banking_service)]
):
    """
    Get details for a specific transaction.
    
    - **transaction_id**: Unique transaction identifier (required)
    """
    try:
        logger.info(f"Getting transaction details for ID: {transaction_id}")
        
        transaction = await banking_service.get_transaction(transaction_id=transaction_id)
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transaction with ID '{transaction_id}' not found"
            )
        
        response_data = TransactionResponse(
            id=transaction.id,
            transaction_date=transaction.transaction_date,
            account_number=transaction.account_number,
            bank_name=transaction.bank_name.value,
            sub_account=transaction.sub_account,
            amount_in=Decimal(str(transaction.amount_in)),
            amount_out=Decimal(str(transaction.amount_out)),
            accumulated=Decimal(str(transaction.accumulated)),
            code=transaction.code,
            transaction_content=transaction.transaction_content,
            reference_number=transaction.reference_number
        )
        
        logger.info(f"Successfully retrieved transaction details")
        
        return SuccessResponse(
            success=True,
            data=response_data,
            message="Transaction details retrieved successfully"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except IBankingServiceError as e:
        logger.error(f"Banking service error: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Banking service error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

"""
FastAPI application main module.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging
import sys

from finkeith.api.v1.banking import router as banking_router
from finkeith.schemas.base import ErrorResponse, ErrorDetail
from finkeith.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("🚀 FinKeith MCP Banking API starting up...")
    yield
    # Shutdown
    logger.info("🛑 FinKeith MCP Banking API shutting down...")


# Create FastAPI application
app = FastAPI(
    title="FinKeith MCP Banking API",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    logger.warning(f"Validation error on {request.url}: {exc}")
    
    error_details = [
        ErrorDetail(
            field=".".join(str(loc) for loc in error["loc"][1:]) if len(error["loc"]) > 1 else str(error["loc"][0]),
            message=error["msg"],
            code=error["type"]
        )
        for error in exc.errors()
    ]
    
    error_response = ErrorResponse(
        error="Validation failed",
        details=error_details,
        error_code="VALIDATION_ERROR"
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(error_response.model_dump())
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error on {request.url}: {exc}", exc_info=True)
    
    error_response = ErrorResponse(
        error="Internal server error",
        error_code="INTERNAL_ERROR"
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(error_response.model_dump())
    )


# Health check endpoint
@app.get(
    "/health",
    summary="API Health Check",
    description="Check if the API is running and healthy",
    tags=["Health"]
)
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "FinKeith MCP Banking API",
        "version": "1.0.0"
    }


# Include routers
app.include_router(banking_router)


# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint redirect."""
    return {
        "message": "Welcome to FinKeith MCP Banking API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "finkeith.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        log_level="info"
    )

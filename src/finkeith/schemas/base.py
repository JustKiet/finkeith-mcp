"""
Base schemas and common components for API requests and responses.
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T")


class BaseResponseModel(BaseModel):
    """Base response model with common fields."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="forbid"
    )


class SuccessResponse(BaseResponseModel, Generic[T]):
    """Standard success response wrapper."""
    
    success: bool = Field(True, description="Indicates successful operation")
    data: T = Field(..., description="Response data")
    message: Optional[str] = Field(None, description="Optional success message")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Response timestamp")


class ErrorDetail(BaseModel):
    """Error detail information."""
    
    field: Optional[str] = Field(None, description="Field name that caused the error")
    message: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code for programmatic handling")


class ErrorResponse(BaseResponseModel):
    """Standard error response."""
    
    success: bool = Field(default=False, description="Indicates failed operation")
    error: str = Field(..., description="Error message")
    details: Optional[List[ErrorDetail]] = Field(default=None, description="Detailed error information")
    error_code: Optional[str] = Field(default=None, description="Error code for programmatic handling")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Response timestamp")


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    
    page: int = Field(..., ge=1, description="Current page number")
    per_page: int = Field(..., ge=1, le=100, description="Items per page")
    total: int = Field(..., ge=0, description="Total number of items")
    pages: int = Field(..., ge=0, description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class PaginatedResponse(BaseResponseModel, Generic[T]):
    """Paginated response wrapper."""
    
    success: bool = Field(True, description="Indicates successful operation")
    data: List[T] = Field(..., description="List of items")
    meta: PaginationMeta = Field(..., description="Pagination metadata")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Response timestamp")


class HealthStatus(str, Enum):
    """Health check status values."""
    
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthResponse(BaseResponseModel):
    """Health check response."""
    
    status: HealthStatus = Field(..., description="Overall health status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Health check timestamp")
    services: Dict[str, str] = Field(default_factory=dict, description="Status of dependent services")

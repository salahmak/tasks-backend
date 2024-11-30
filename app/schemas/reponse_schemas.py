from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# Generic type for data payload
T = TypeVar('T')

# Pagination Model
class PaginationMetadata(BaseModel):
    total_items: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")
    current_page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_previous: bool = Field(..., description="Whether there are previous pages")

# Error Model
class ErrorCode(str, Enum):
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"
    INTERNAL_SERVER_ERROR = "internal_server_error"

class ErrorResponse(BaseModel):
    code: ErrorCode
    message: str
    details: Optional[dict] = None

# Generic Response Model
class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(..., description="Indicates if the request was successful")
    data: Optional[T] = Field(None, description="Response payload")
    error: Optional[ErrorResponse] = Field(None, description="Error details if request failed")
    pagination: Optional[PaginationMetadata] = Field(None, description="Pagination metadata for list responses")

# Specific Task-related Response Models
class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    is_deleted: bool

    class Config:
        from_attributes = True

# Example of how to use these models in routes
def create_success_response(
    data: Optional[T] = None,
    pagination: Optional[PaginationMetadata] = None
) -> APIResponse[T]:
    return APIResponse(
        success=True,
        data=data,
        error=None,
        pagination=pagination,
    )

def create_error_response(
    code: ErrorCode,
    message: str,
    details: Optional[dict] = None
) -> APIResponse[object]:
    return APIResponse(
        success=False,
        data=None,
        pagination=None,
        error=ErrorResponse(
            code=code,
            message=message,
            details=details
        )
    )

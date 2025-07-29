from pydantic import BaseModel, Field
from datetime import datetime

class Date(BaseModel):
    """Date schema for date-related fields."""
    
    year: int = Field(..., description="Year of the date")
    month: int = Field(..., ge=1, le=12, description="Month of the date (1-12)")
    day: int = Field(..., ge=1, le=31, description="Day of the month (1-31)")

    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        str_strip_whitespace = True
        validate_assignment = True

    def to_datetime(self):
        """Convert to a datetime object."""
        return datetime(self.year, self.month, self.day)
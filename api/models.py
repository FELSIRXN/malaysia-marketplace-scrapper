"""
Pydantic models for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SearchRequest(BaseModel):
    """Search request model."""
    keyword: str = Field(..., min_length=1, max_length=200, description="Search keyword")
    platforms: List[str] = Field(default=['shopee', 'lazada', 'mudah'], description="Platforms to search")
    limit: int = Field(default=50, ge=1, le=200, description="Results per platform")


class BestSellerRequest(BaseModel):
    """Best-seller search request model."""
    keyword: str = Field(..., min_length=1, max_length=200)
    platforms: List[str] = Field(default=['shopee', 'lazada', 'mudah'])
    limit: int = Field(default=100, ge=1, le=200)
    max_price: float = Field(default=50.0, gt=0, description="Maximum price in RM")
    top_n: int = Field(default=50, ge=1, le=100, description="Top N results to return")


class ProductData(BaseModel):
    """Product data model."""
    name: str
    price: float
    rating: Optional[float] = 0
    sold: Optional[int] = 0
    url: Optional[str] = ""
    merchant: Optional[str] = ""
    platform: str


class SearchResponse(BaseModel):
    """Search response model."""
    search_id: int
    keyword: str
    platforms: List[str]
    status: str = "pending"
    message: str = "Search started"


class SearchResultsResponse(BaseModel):
    """Search results response model."""
    search_id: int
    keyword: str
    platforms: List[str]
    results: Dict[str, List[Dict[str, Any]]]
    total_count: int
    status: str
    timestamp: str


class SearchHistoryItem(BaseModel):
    """Search history item model."""
    id: int
    keyword: str
    platforms: List[str]
    limit_per_platform: int
    max_price: Optional[float] = None
    top_n: Optional[int] = None
    timestamp: str
    result_count: int
    status: str
    error_message: Optional[str] = None


class PlatformInfo(BaseModel):
    """Platform information model."""
    id: str
    name: str
    enabled: bool
    region: str
    currency: str


class StatusResponse(BaseModel):
    """System status response model."""
    status: str
    version: str
    platforms_available: int
    database_connected: bool


class ExportRequest(BaseModel):
    """Export request model."""
    search_id: int
    format: str = Field(default="csv", pattern="^(csv|json|excel)$")
    
    
class ComparisonRequest(BaseModel):
    """Platform comparison request model."""
    keyword: str
    platforms: List[str]
    limit: int = Field(default=50, ge=1, le=200)


class ProgressUpdate(BaseModel):
    """WebSocket progress update model."""
    search_id: int
    platform: Optional[str] = None
    status: str
    progress: int = Field(ge=0, le=100)
    message: str
    current_count: int = 0

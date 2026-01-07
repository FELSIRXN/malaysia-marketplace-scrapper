"""
History endpoints for managing search history.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from api.models import SearchHistoryItem
from api.database import db

router = APIRouter()


@router.get("/history", response_model=List[SearchHistoryItem])
async def get_history(limit: int = 20):
    """
    Get recent search history.
    
    Args:
        limit: Maximum number of results
        
    Returns:
        List of search history items
    """
    history = db.get_search_history(limit=limit)
    return history


@router.get("/history/{search_id}", response_model=SearchHistoryItem)
async def get_history_item(search_id: int):
    """
    Get specific search history item.
    
    Args:
        search_id: Search ID
        
    Returns:
        Search history item
    """
    search = db.get_search_by_id(search_id)
    
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    return SearchHistoryItem(
        id=search['id'],
        keyword=search['keyword'],
        platforms=search['platforms'],
        limit_per_platform=search['limit_per_platform'],
        max_price=search['max_price'],
        top_n=search['top_n'],
        timestamp=search['timestamp'],
        result_count=search['result_count'],
        status=search['status'],
        error_message=search['error_message']
    )


@router.delete("/history/{search_id}")
async def delete_history_item(search_id: int):
    """
    Delete a search history item.
    
    Args:
        search_id: Search ID
        
    Returns:
        Success message
    """
    search = db.get_search_by_id(search_id)
    
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    db.delete_search(search_id)
    
    return {"message": f"Search {search_id} deleted successfully"}


@router.delete("/history")
async def clear_history():
    """
    Clear all search history.
    
    Returns:
        Success message
    """
    history = db.get_search_history(limit=1000)
    count = 0
    
    for item in history:
        db.delete_search(item['id'])
        count += 1
    
    return {"message": f"Cleared {count} search history items"}

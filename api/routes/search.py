"""
Search endpoints for product searching and best-seller analysis.
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from api.models import SearchRequest, BestSellerRequest, SearchResponse, SearchResultsResponse
from api.database import db
from multi_platform_scraper import MultiPlatformScraper
from advanced_analyzer import AdvancedAnalyzer
import asyncio

router = APIRouter()


async def perform_search_task(search_id: int, keyword: str, platforms: list, 
                             limit: int, ws_manager, is_bestseller: bool = False,
                             max_price: float = None, top_n: int = None):
    """
    Background task to perform search.
    
    Args:
        search_id: Search ID
        keyword: Search keyword
        platforms: List of platforms
        limit: Results per platform
        ws_manager: WebSocket manager
        is_bestseller: Whether this is a best-seller search
        max_price: Maximum price filter
        top_n: Top N results
    """
    try:
        # Send initial status
        await ws_manager.send_message({
            "search_id": search_id,
            "status": "started",
            "progress": 0,
            "message": f"Starting search for '{keyword}'",
            "current_count": 0
        }, search_id)
        
        # Initialize scraper
        scraper = MultiPlatformScraper()
        
        if is_bestseller and max_price and top_n:
            # Best-seller analysis
            analyzer = AdvancedAnalyzer()
            
            # Search all platforms
            results = scraper.search_specific_platforms(keyword, platforms, limit)
            
            # Combine products
            all_products = []
            for platform, products in results.items():
                for product in products:
                    product['platform'] = platform
                    all_products.append(product)
            
            # Analyze best-sellers
            analysis = analyzer.analyze_affordable_bestsellers(
                all_products, 
                max_price=max_price,
                top_n=top_n
            )
            
            # Extract top products
            if 'top_products' in analysis:
                # Reorganize by platform
                results = {}
                for product in analysis['top_products']:
                    platform = product.get('platform', 'unknown')
                    if platform not in results:
                        results[platform] = []
                    results[platform].append(product)
        else:
            # Regular search
            results = scraper.search_specific_platforms(keyword, platforms, limit)
        
        # Save results to database
        total_count = db.save_results(search_id, results)
        db.update_search_status(search_id, 'completed', total_count)
        
        # Send completion message
        await ws_manager.send_message({
            "search_id": search_id,
            "status": "completed",
            "progress": 100,
            "message": f"Search completed! Found {total_count} products",
            "current_count": total_count
        }, search_id)
        
    except Exception as e:
        # Update database with error
        db.update_search_status(search_id, 'failed', 0, str(e))
        
        # Send error message
        await ws_manager.send_message({
            "search_id": search_id,
            "status": "failed",
            "progress": 0,
            "message": f"Search failed: {str(e)}",
            "current_count": 0
        }, search_id)


@router.post("/search", response_model=SearchResponse)
async def search_products(request: SearchRequest, background_tasks: BackgroundTasks, 
                         req: Request):
    """
    Search for products across multiple platforms.
    
    Args:
        request: Search request parameters
        background_tasks: FastAPI background tasks
        req: FastAPI request object
        
    Returns:
        Search response with search ID
    """
    # Create search in database
    search_id = db.create_search(
        keyword=request.keyword,
        platforms=request.platforms,
        limit_per_platform=request.limit
    )
    
    # Get WebSocket manager
    ws_manager = req.app.state.ws_manager
    
    # Start background search task
    background_tasks.add_task(
        perform_search_task,
        search_id,
        request.keyword,
        request.platforms,
        request.limit,
        ws_manager,
        False
    )
    
    return SearchResponse(
        search_id=search_id,
        keyword=request.keyword,
        platforms=request.platforms,
        status="pending",
        message=f"Search started for '{request.keyword}'"
    )


@router.post("/search/bestsellers", response_model=SearchResponse)
async def search_bestsellers(request: BestSellerRequest, background_tasks: BackgroundTasks,
                            req: Request):
    """
    Search for best-selling affordable items.
    
    Args:
        request: Best-seller request parameters
        background_tasks: FastAPI background tasks
        req: FastAPI request object
        
    Returns:
        Search response with search ID
    """
    # Create search in database
    search_id = db.create_search(
        keyword=request.keyword,
        platforms=request.platforms,
        limit_per_platform=request.limit,
        max_price=request.max_price,
        top_n=request.top_n
    )
    
    # Get WebSocket manager
    ws_manager = req.app.state.ws_manager
    
    # Start background search task
    background_tasks.add_task(
        perform_search_task,
        search_id,
        request.keyword,
        request.platforms,
        request.limit,
        ws_manager,
        True,
        request.max_price,
        request.top_n
    )
    
    return SearchResponse(
        search_id=search_id,
        keyword=request.keyword,
        platforms=request.platforms,
        status="pending",
        message=f"Best-seller search started for '{request.keyword}'"
    )


@router.get("/search/{search_id}", response_model=SearchResultsResponse)
async def get_search_results(search_id: int):
    """
    Get search results by ID.
    
    Args:
        search_id: Search ID
        
    Returns:
        Search results with products
    """
    search = db.get_search_by_id(search_id)
    
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    return SearchResultsResponse(
        search_id=search['id'],
        keyword=search['keyword'],
        platforms=search['platforms'],
        results=search['results'],
        total_count=search['result_count'],
        status=search['status'],
        timestamp=search['timestamp']
    )

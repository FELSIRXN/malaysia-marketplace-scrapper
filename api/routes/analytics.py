"""
Analytics endpoints for data analysis and comparison.
"""

from fastapi import APIRouter, HTTPException
from api.models import ComparisonRequest
from api.database import db
from advanced_analyzer import AdvancedAnalyzer

router = APIRouter()


@router.post("/analyze/comparison")
async def platform_comparison(request: ComparisonRequest):
    """
    Compare platforms for a keyword.
    
    Args:
        request: Comparison request parameters
        
    Returns:
        Platform comparison analysis
    """
    from multi_platform_scraper import MultiPlatformScraper
    
    scraper = MultiPlatformScraper()
    analyzer = AdvancedAnalyzer()
    
    # Search across platforms
    results = scraper.search_specific_platforms(
        request.keyword,
        request.platforms,
        request.limit
    )
    
    # Prepare combined data
    all_products = []
    for platform, products in results.items():
        for product in products:
            product['platform'] = platform
            all_products.append(product)
    
    if not all_products:
        return {
            "keyword": request.keyword,
            "platforms": request.platforms,
            "comparison": {},
            "message": "No products found"
        }
    
    # Perform analysis
    analysis = analyzer.analyze_products(all_products)
    platform_comparison = analyzer.compare_platforms(all_products)
    
    return {
        "keyword": request.keyword,
        "platforms": request.platforms,
        "total_products": len(all_products),
        "analysis": analysis,
        "platform_comparison": platform_comparison
    }


@router.get("/analyze/price/{search_id}")
async def price_analysis(search_id: int):
    """
    Get price analysis for a search.
    
    Args:
        search_id: Search ID
        
    Returns:
        Price analysis
    """
    search = db.get_search_by_id(search_id)
    
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    # Combine all products
    all_products = []
    for platform, products in search['results'].items():
        for product in products:
            product['platform'] = platform
            all_products.append(product)
    
    if not all_products:
        return {"error": "No products found"}
    
    analyzer = AdvancedAnalyzer()
    analysis = analyzer.analyze_products(all_products)
    
    return {
        "search_id": search_id,
        "keyword": search['keyword'],
        "price_analysis": analysis.get('price_analysis', {}),
        "rating_analysis": analysis.get('rating_analysis', {})
    }


@router.get("/analyze/trends/{search_id}")
async def trend_analysis(search_id: int):
    """
    Get trend analysis for a search.
    
    Args:
        search_id: Search ID
        
    Returns:
        Trend analysis
    """
    search = db.get_search_by_id(search_id)
    
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    # Combine all products
    all_products = []
    for platform, products in search['results'].items():
        for product in products:
            product['platform'] = platform
            all_products.append(product)
    
    if not all_products:
        return {"error": "No products found"}
    
    # Calculate trends
    price_ranges = {
        "under_10": 0,
        "10_to_25": 0,
        "25_to_50": 0,
        "50_to_100": 0,
        "over_100": 0
    }
    
    rating_distribution = {
        "5_stars": 0,
        "4_to_5": 0,
        "3_to_4": 0,
        "2_to_3": 0,
        "under_2": 0
    }
    
    for product in all_products:
        price = product.get('price', 0)
        rating = product.get('rating', 0)
        
        # Price ranges
        if price < 10:
            price_ranges["under_10"] += 1
        elif price < 25:
            price_ranges["10_to_25"] += 1
        elif price < 50:
            price_ranges["25_to_50"] += 1
        elif price < 100:
            price_ranges["50_to_100"] += 1
        else:
            price_ranges["over_100"] += 1
        
        # Rating distribution
        if rating >= 5:
            rating_distribution["5_stars"] += 1
        elif rating >= 4:
            rating_distribution["4_to_5"] += 1
        elif rating >= 3:
            rating_distribution["3_to_4"] += 1
        elif rating >= 2:
            rating_distribution["2_to_3"] += 1
        else:
            rating_distribution["under_2"] += 1
    
    return {
        "search_id": search_id,
        "keyword": search['keyword'],
        "price_ranges": price_ranges,
        "rating_distribution": rating_distribution,
        "total_products": len(all_products)
    }

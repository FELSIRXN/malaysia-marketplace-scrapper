"""
Export endpoints for downloading search results.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from api.models import ExportRequest
from api.database import db
import pandas as pd
import json
import io
from pathlib import Path

router = APIRouter()


@router.get("/export/{search_id}")
async def export_results(search_id: int, format: str = "csv"):
    """
    Export search results in specified format.
    
    Args:
        search_id: Search ID
        format: Export format (csv, json, excel)
        
    Returns:
        File download response
    """
    # Get search results
    search = db.get_search_by_id(search_id)
    
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    if not search['results']:
        raise HTTPException(status_code=404, detail="No results found for this search")
    
    keyword = search['keyword'].replace(' ', '_')
    timestamp = search['timestamp'].replace(' ', '_').replace(':', '-')
    
    if format == "json":
        # JSON export
        filename = f"search_{keyword}_{timestamp}.json"
        content = json.dumps(search, indent=2, ensure_ascii=False)
        
        return StreamingResponse(
            io.BytesIO(content.encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    elif format == "csv":
        # CSV export
        filename = f"search_{keyword}_{timestamp}.csv"
        
        # Flatten results
        rows = []
        for platform, products in search['results'].items():
            for product in products:
                rows.append({
                    'keyword': search['keyword'],
                    'platform': platform,
                    'name': product.get('name', ''),
                    'price': product.get('price', 0),
                    'rating': product.get('rating', 0),
                    'sold': product.get('sold', 0),
                    'merchant': product.get('merchant', ''),
                    'url': product.get('url', '')
                })
        
        df = pd.DataFrame(rows)
        csv_content = df.to_csv(index=False)
        
        return StreamingResponse(
            io.BytesIO(csv_content.encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    elif format == "excel":
        # Excel export
        filename = f"search_{keyword}_{timestamp}.xlsx"
        
        # Flatten results
        rows = []
        for platform, products in search['results'].items():
            for product in products:
                rows.append({
                    'keyword': search['keyword'],
                    'platform': platform,
                    'name': product.get('name', ''),
                    'price': product.get('price', 0),
                    'rating': product.get('rating', 0),
                    'sold': product.get('sold', 0),
                    'merchant': product.get('merchant', ''),
                    'url': product.get('url', '')
                })
        
        df = pd.DataFrame(rows)
        
        # Write to BytesIO
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Results')
        output.seek(0)
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use csv, json, or excel")

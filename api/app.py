"""
FastAPI application for Malaysia Marketplace Scraper web interface.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.routes import search, export, analytics, history
from api.database import db
from api.models import StatusResponse
from config import get_enabled_platforms, SUPPORTED_PLATFORMS

# Initialize FastAPI app
app = FastAPI(
    title="Malaysia Marketplace Scraper API",
    description="REST API for multi-platform e-commerce scraping and analysis",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(export.router, prefix="/api", tags=["Export"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(history.router, prefix="/api", tags=["History"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Malaysia Marketplace Scraper API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Get system status."""
    enabled_platforms = get_enabled_platforms()
    
    return StatusResponse(
        status="healthy",
        version="1.0.0",
        platforms_available=len(enabled_platforms),
        database_connected=True
    )


@app.get("/api/platforms")
async def get_platforms():
    """Get available platforms."""
    platforms = []
    for platform_id, platform_config in SUPPORTED_PLATFORMS.items():
        platforms.append({
            "id": platform_id,
            "name": platform_config['name'],
            "enabled": platform_config['enabled'],
            "region": platform_config.get('region', ''),
            "currency": platform_config.get('currency', '')
        })
    
    return {"platforms": platforms}


# WebSocket connection manager
class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: dict = {}
    
    async def connect(self, websocket: WebSocket, search_id: int):
        """Connect a new WebSocket client."""
        await websocket.accept()
        if search_id not in self.active_connections:
            self.active_connections[search_id] = []
        self.active_connections[search_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, search_id: int):
        """Disconnect a WebSocket client."""
        if search_id in self.active_connections:
            self.active_connections[search_id].remove(websocket)
            if not self.active_connections[search_id]:
                del self.active_connections[search_id]
    
    async def send_message(self, message: dict, search_id: int):
        """Send message to all clients for a search ID."""
        if search_id in self.active_connections:
            for connection in self.active_connections[search_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass


manager = ConnectionManager()


@app.websocket("/ws/search/{search_id}")
async def websocket_endpoint(websocket: WebSocket, search_id: int):
    """WebSocket endpoint for real-time search progress."""
    await manager.connect(websocket, search_id)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket, search_id)


# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "detail": "An error occurred processing your request"}
    )


# Export manager for WebSocket access
app.state.ws_manager = manager


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

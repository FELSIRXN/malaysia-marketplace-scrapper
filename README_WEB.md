# Web Interface Guide

## Overview

The Malaysia Marketplace Scraper now includes a modern web interface built with React and FastAPI. Users can access all scraper functionality through a browser without using the terminal.

## Quick Start

### Starting the Web Interface

1. **Install Python dependencies** (if not already done):
   ```bash
   pip install -e .
   ```

2. **Install Node.js dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **Start both servers**:
   ```bash
   python start_web.py
   ```

   Or start them separately:
   ```bash
   # Terminal 1 - Backend
   uvicorn api.app:app --reload --port 8000
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

4. **Access the web interface**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Features

### 🏠 Home Page
- Overview of the application
- Quick links to main features
- Feature highlights

### 🔍 Product Search
- Search across multiple platforms (Shopee, Lazada, Mudah)
- Real-time progress updates via WebSocket
- Interactive results table with pagination
- Advanced filtering (price, rating, sales)
- Export to CSV, JSON, or Excel
- Interactive charts (price distribution, ratings, sales)

### 📊 Best Sellers Analysis
- Find top-selling affordable items
- Price range filter (max RM)
- Top N selector (10, 20, 50, 100)
- Platform selection
- Ranked results display

### 📈 Platform Comparison
- Side-by-side platform comparison
- Price analysis (min/max/average)
- Platform metrics and scores
- Best value recommendations

### 📜 Search History
- View recent searches
- Click to reload results
- Delete individual searches
- Clear all history

## API Endpoints

### Search
- `POST /api/search` - General product search
- `POST /api/search/bestsellers` - Best-seller analysis
- `GET /api/search/{search_id}` - Get search results

### Export
- `GET /api/export/{search_id}?format=csv|json|excel` - Download results

### Analytics
- `POST /api/analyze/comparison` - Platform comparison
- `GET /api/analyze/price/{search_id}` - Price analysis
- `GET /api/analyze/trends/{search_id}` - Trend analysis

### History
- `GET /api/history` - Get search history
- `GET /api/history/{id}` - Get specific search
- `DELETE /api/history/{id}` - Delete search

### Status
- `GET /api/status` - System health check
- `GET /api/platforms` - List available platforms

### WebSocket
- `WS /ws/search/{search_id}` - Real-time search progress

## Development

### Frontend Structure
```
frontend/
├── src/
│   ├── components/     # Reusable components
│   ├── pages/         # Page components
│   ├── services/      # API integration
│   ├── hooks/         # Custom React hooks
│   ├── utils/         # Helper functions
│   └── App.jsx        # Main app component
```

### Backend Structure
```
api/
├── app.py            # FastAPI application
├── routes/           # API endpoints
├── models.py         # Pydantic models
├── database.py       # SQLite database
└── ...
```

### Environment Variables

Create `.env` file in frontend directory (optional):
```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Ensure all Python dependencies are installed
- Check logs for errors

### Frontend won't start
- Check if Node.js and npm are installed
- Run `npm install` in frontend directory
- Check if port 3000 is available

### WebSocket connection fails
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify CORS settings in backend

### API calls fail
- Check backend is running
- Verify API URL in frontend services
- Check browser network tab for errors

## Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
```

### Serve Frontend from FastAPI
Update `api/app.py` to serve static files:
```python
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
```

### Run Production Server
```bash
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Notes

- The web interface uses WebSocket for real-time updates
- Search history is stored in SQLite database (`data/search_history.db`)
- All exports are downloaded directly to your browser's download folder
- The interface is fully responsive and works on mobile devices

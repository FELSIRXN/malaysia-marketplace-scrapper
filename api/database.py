"""
Database configuration and session management for SQLite.
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class Database:
    """SQLite database handler for search history and results."""
    
    def __init__(self, db_path: str = "data/search_history.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        # Ensure data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.create_tables()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_tables(self):
        """Create necessary database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Search history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                platforms TEXT NOT NULL,
                limit_per_platform INTEGER DEFAULT 50,
                max_price REAL,
                top_n INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                result_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',
                error_message TEXT
            )
        """)
        
        # Search results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id INTEGER NOT NULL,
                platform TEXT NOT NULL,
                product_name TEXT,
                price REAL,
                rating REAL,
                sold INTEGER DEFAULT 0,
                url TEXT,
                merchant TEXT,
                FOREIGN KEY (search_id) REFERENCES search_history (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_search(self, keyword: str, platforms: List[str], 
                     limit_per_platform: int = 50, max_price: Optional[float] = None,
                     top_n: Optional[int] = None) -> int:
        """
        Create new search record.
        
        Args:
            keyword: Search keyword
            platforms: List of platforms to search
            limit_per_platform: Results limit per platform
            max_price: Maximum price filter
            top_n: Top N results to return
            
        Returns:
            Search ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO search_history 
            (keyword, platforms, limit_per_platform, max_price, top_n, status)
            VALUES (?, ?, ?, ?, ?, 'pending')
        """, (keyword, json.dumps(platforms), limit_per_platform, max_price, top_n))
        
        search_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return search_id
    
    def update_search_status(self, search_id: int, status: str, 
                            result_count: int = 0, error_message: Optional[str] = None):
        """Update search status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE search_history 
            SET status = ?, result_count = ?, error_message = ?
            WHERE id = ?
        """, (status, result_count, error_message, search_id))
        
        conn.commit()
        conn.close()
    
    def save_results(self, search_id: int, results: Dict[str, List[Dict[str, Any]]]):
        """
        Save search results to database.
        
        Args:
            search_id: Search ID
            results: Results by platform
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        total_count = 0
        for platform, products in results.items():
            for product in products:
                cursor.execute("""
                    INSERT INTO search_results 
                    (search_id, platform, product_name, price, rating, sold, url, merchant)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    search_id,
                    platform,
                    product.get('name', ''),
                    product.get('price', 0),
                    product.get('rating', 0),
                    product.get('sold', 0),
                    product.get('url', ''),
                    product.get('merchant', '')
                ))
                total_count += 1
        
        conn.commit()
        conn.close()
        
        return total_count
    
    def get_search_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent search history."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM search_history 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'id': row['id'],
                'keyword': row['keyword'],
                'platforms': json.loads(row['platforms']),
                'limit_per_platform': row['limit_per_platform'],
                'max_price': row['max_price'],
                'top_n': row['top_n'],
                'timestamp': row['timestamp'],
                'result_count': row['result_count'],
                'status': row['status'],
                'error_message': row['error_message']
            })
        
        return history
    
    def get_search_by_id(self, search_id: int) -> Optional[Dict[str, Any]]:
        """Get search by ID with results."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get search info
        cursor.execute("SELECT * FROM search_history WHERE id = ?", (search_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        search = {
            'id': row['id'],
            'keyword': row['keyword'],
            'platforms': json.loads(row['platforms']),
            'limit_per_platform': row['limit_per_platform'],
            'max_price': row['max_price'],
            'top_n': row['top_n'],
            'timestamp': row['timestamp'],
            'result_count': row['result_count'],
            'status': row['status'],
            'error_message': row['error_message']
        }
        
        # Get results
        cursor.execute("SELECT * FROM search_results WHERE search_id = ?", (search_id,))
        result_rows = cursor.fetchall()
        
        results = {}
        for result_row in result_rows:
            platform = result_row['platform']
            if platform not in results:
                results[platform] = []
            
            results[platform].append({
                'name': result_row['product_name'],
                'price': result_row['price'],
                'rating': result_row['rating'],
                'sold': result_row['sold'],
                'url': result_row['url'],
                'merchant': result_row['merchant']
            })
        
        search['results'] = results
        conn.close()
        
        return search
    
    def delete_search(self, search_id: int):
        """Delete search and its results."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM search_results WHERE search_id = ?", (search_id,))
        cursor.execute("DELETE FROM search_history WHERE id = ?", (search_id,))
        
        conn.commit()
        conn.close()


# Global database instance
db = Database()

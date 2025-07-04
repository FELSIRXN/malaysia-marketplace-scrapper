from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import time
import random
import re
import json
from urllib.parse import urljoin, quote
from typing import Dict, List, Any, Optional

from config import get_config, USER_AGENTS, DEFAULT_CONFIG
from logger import get_logger

class BaseEcommerceScraper(ABC):
    """Base class for e-commerce scrapers with clean architecture and centralized config."""
    
    def __init__(self, country: str = None):
        self.config = get_config()
        self.country = country or self.config['country']
        self.session = requests.Session()
        self.logger = get_logger(self.__class__.__name__)
        
        # Use random user agent from config
        user_agent = random.choice(USER_AGENTS)
        
        # Common headers with Indonesian region priority
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
        # Configure timeouts and retries
        self.session.timeout = self.config['request_timeout']
        self.max_retries = self.config['retry_attempts']
        self.request_delay = self.config['delay_between_requests']
    
    @abstractmethod
    def get_base_url(self):
        """Get the base URL for the platform"""
        pass
    
    @abstractmethod
    def search_products(self, keyword, limit=50):
        """Search for products"""
        pass
    
    @abstractmethod
    def get_shop_info(self, shop_id):
        """Get shop information"""
        pass
    
    @abstractmethod
    def get_shop_products(self, shop_id, limit=50):
        """Get products from a shop"""
        pass
    
    def get_random_delay(self, min_delay: float = None, max_delay: float = None) -> float:
        """Random delay to avoid being blocked - uses config defaults."""
        min_delay = min_delay or self.request_delay
        max_delay = max_delay or (self.request_delay * 2)
        return random.uniform(min_delay, max_delay)
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with retry logic and proper logging."""
        start_time = time.time()
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method, url, timeout=self.session.timeout, **kwargs)
                duration = time.time() - start_time
                
                # Log request details
                self.logger.debug(f"{method} {url} -> {response.status_code} ({duration:.2f}s)")
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Rate limited
                    delay = self.get_random_delay(2, 5)
                    self.logger.warning(f"Rate limited, delaying {delay:.2f}s")
                    time.sleep(delay)
                else:
                    self.logger.warning(f"Request failed with status {response.status_code}")
                    
            except requests.RequestException as e:
                self.logger.error(f"Request failed (attempt {attempt + 1}): {str(e)}")
                if attempt < self.max_retries - 1:
                    delay = self.get_random_delay(1, 3)
                    time.sleep(delay)
        
        return None
    
    def save_to_csv(self, data: List[Dict], filename: str) -> bool:
        """Save data to CSV file with error handling."""
        try:
            import pandas as pd
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8')
            self.logger.info(f"Data saved to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save CSV: {str(e)}")
            return False
    
    def save_to_json(self, data: Any, filename: str) -> bool:
        """Save data to JSON file with error handling."""
        try:
            import numpy as np
            
            class NumpyEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, np.integer):
                        return int(obj)
                    elif isinstance(obj, np.floating):
                        return float(obj)
                    elif isinstance(obj, np.ndarray):
                        return obj.tolist()
                    return super().default(obj)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)
            self.logger.info(f"Data saved to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save JSON: {str(e)}")
            return False
    
    def normalize_price(self, price_text: str) -> float:
        """Extract and normalize price from text (Indonesian Rupiah focus)."""
        if not price_text:
            return 0.0
        
        # Remove currency symbols and normalize
        price_text = str(price_text).replace('Rp', '').replace('$', '').replace(',', '').replace('.', '')
        
        # Extract numeric value
        price_match = re.search(r'(\d+)', price_text.replace('.', '').replace(',', ''))
        if price_match:
            price = int(price_match.group(1))
            # Convert to standard format (assuming Indonesian Rupiah)
            if price > 100000:  # If price seems to be in smallest unit
                return price / 1000  # Convert to thousands
            return price
        return 0.0
    
    def normalize_rating(self, rating_text: str) -> float:
        """Extract and normalize rating from text."""
        if not rating_text:
            return 0.0
        
        rating_match = re.search(r'(\d+\.?\d*)', str(rating_text))
        if rating_match:
            rating = float(rating_match.group(1))
            return min(rating, 5.0)  # Cap at 5.0
        return 0.0
    
    def normalize_sold_count(self, sold_text: str) -> int:
        """Extract and normalize sold count from text."""
        if not sold_text:
            return 0
        
        sold_text = str(sold_text).lower()
        
        # Handle Indonesian terms
        if 'rb' in sold_text or 'ribu' in sold_text:
            multiplier = 1000
        elif 'jt' in sold_text or 'juta' in sold_text:
            multiplier = 1000000
        else:
            multiplier = 1
        
        # Extract number
        number_match = re.search(r'(\d+\.?\d*)', sold_text)
        if number_match:
            number = float(number_match.group(1))
            return int(number * multiplier)
        
        return 0
    
    def validate_product_data(self, product: Dict[str, Any]) -> bool:
        """Validate product data structure."""
        required_fields = ['name', 'price', 'rating', 'platform']
        return all(field in product for field in required_fields)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data."""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', str(text).strip())
        return text
        
        # Handle different formats
        if 'rb' in sold_text or 'ribu' in sold_text:
            number_match = re.search(r'(\d+\.?\d*)', sold_text)
            if number_match:
                return int(float(number_match.group(1)) * 1000)
        
        number_match = re.search(r'(\d+)', sold_text.replace(',', '').replace('.', ''))
        if number_match:
            return int(number_match.group(1))
        
        return 0

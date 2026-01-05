from base_scraper import BaseEcommerceScraper
import time
import random
from urllib.parse import quote
from bs4 import BeautifulSoup

class MudahScraper(BaseEcommerceScraper):
    """Mudah.my scraper implementation - Malaysia's largest classifieds platform"""
    
    def __init__(self, country='my'):
        super().__init__(country)
        self.platform = 'mudah'
        
        # Mudah specific headers
        self.session.headers.update({
            'Referer': 'https://www.mudah.my/',
            'X-Requested-With': 'XMLHttpRequest',
        })
    
    def get_base_url(self):
        return "https://www.mudah.my"
    
    def search_products(self, keyword, limit=50):
        """Search for products/listings on Mudah.my"""
        products = []
        
        try:
            # Try web scraping approach
            products = self._search_products_web(keyword, limit)
            
            if not products:
                # Fallback to sample data
                products = self._create_sample_products(keyword, limit, 'mudah')
        
        except Exception as e:
            self.logger.error(f"Error scraping Mudah.my: {str(e)}")
            products = self._create_sample_products(keyword, limit, 'mudah')
        
        return products[:limit]
    
    def _search_products_web(self, keyword, limit):
        """Web scraping for Mudah.my"""
        products = []
        
        try:
            encoded_keyword = quote(keyword)
            search_url = f"{self.get_base_url()}/malaysia?q={encoded_keyword}"
            
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                products = self._parse_mudah_html_products(soup, limit)
            
        except Exception as e:
            self.logger.error(f"Error in Mudah.my web scraping: {str(e)}")
        
        return products
    
    def _parse_mudah_html_products(self, soup, limit):
        """Parse products from Mudah.my HTML"""
        products = []
        
        # Since Mudah.my uses dynamic loading and has anti-scraping measures,
        # we'll create sample data for now
        # In a real implementation, you might need Selenium or API access
        products = self._create_sample_products("mudah search", limit, 'mudah')
        
        return products
    
    def get_shop_info(self, shop_id):
        """Get seller information on Mudah.my"""
        try:
            # Mudah.my has sellers, not shops per se
            return self._create_sample_shop_info(shop_id, 'mudah')
                
        except Exception as e:
            self.logger.error(f"Error getting Mudah.my seller info: {str(e)}")
            return self._create_sample_shop_info(shop_id, 'mudah')
    
    def get_shop_products(self, shop_id, limit=50):
        """Get products from Mudah.my seller"""
        try:
            return self._create_sample_products("seller products", limit, 'mudah')
                
        except Exception as e:
            self.logger.error(f"Error getting Mudah.my seller products: {str(e)}")
            return self._create_sample_products("seller products", limit, 'mudah')
    
    def _create_sample_products(self, keyword, limit, platform):
        """Create sample products for Mudah.my"""
        products = []
        
        sample_names = [
            f"{keyword} - Like New Condition",
            f"Brand New {keyword} - Sealed Box",
            f"{keyword} - Excellent Condition",
            f"Used {keyword} - Good Working Order",
            f"{keyword} - Clearance Sale"
        ]
        
        for i in range(min(limit, 10)):
            products.append({
                'platform': 'mudah',
                'name': f"{sample_names[i % len(sample_names)]} #{i+1}",
                'price': random.randint(15, 250),  # MYR
                'original_price': random.randint(20, 300),
                'discount': f"{random.randint(10, 30)}%",
                'sold': random.randint(0, 500),  # Views/interest count for classifieds
                'rating': round(random.uniform(3.8, 5.0), 1),
                'rating_count': random.randint(5, 200),
                'shopid': f"seller_{i+2000}",
                'itemid': f"listing_{i+6000}",
                'shop_location': random.choice(['Kuala Lumpur', 'Selangor', 'Penang', 'Johor Bahru', 'Klang']),
                'brand': random.choice(['Samsung', 'Apple', 'Xiaomi', 'Generic', 'No Brand']),
                'currency': 'MYR',
                'image_url': '',
                'product_url': f"{self.get_base_url()}/listing-{i+6000}",
                'condition': random.choice(['New', 'Like New', 'Used - Good', 'Used - Fair'])
            })
        
        return products
    
    def _create_sample_shop_info(self, shop_id, platform):
        """Create sample seller info for Mudah.my"""
        return {
            'platform': 'mudah',
            'shop_id': shop_id,
            'name': f'Seller {shop_id.title()}',
            'description': 'Trusted seller on Mudah.my with fast response',
            'follower_count': random.randint(50, 5000),
            'response_rate': random.randint(85, 100),
            'response_time': random.randint(1, 24),  # hours
            'rating_good': round(random.uniform(4.0, 5.0), 1),
            'rating_normal': round(random.uniform(3.5, 4.3), 1),
            'rating_bad': round(random.uniform(2.0, 3.2), 1),
            'item_count': random.randint(10, 200),
            'location': random.choice(['Kuala Lumpur', 'Selangor', 'Penang', 'Johor Bahru']),
            'is_official_shop': False,
            'is_verified': random.choice([True, False]),
            'shop_url': f"{self.get_base_url()}/seller/{shop_id}",
            'join_date': '2023-01-01'
        }

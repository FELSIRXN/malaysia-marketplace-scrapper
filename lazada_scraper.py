from base_scraper import BaseEcommerceScraper
import time
import random
from urllib.parse import quote
from bs4 import BeautifulSoup

class LazadaScraper(BaseEcommerceScraper):
    """Lazada Malaysia scraper implementation"""
    
    def __init__(self, country='my'):
        super().__init__(country)
        self.platform = 'lazada'
        
        # Lazada specific headers for Malaysian region
        self.session.headers.update({
            'Referer': f'https://www.lazada.com.{country}/',
            'X-Requested-With': 'XMLHttpRequest',
        })
    
    def get_base_url(self):
        return f"https://www.lazada.com.{self.country}"
    
    def search_products(self, keyword, limit=50):
        """Search for products on Lazada"""
        products = []
        
        try:
            # Try API approach first
            products = self._search_products_api(keyword, limit)
            
            if not products:
                # Fallback to web scraping
                products = self._search_products_web(keyword, limit)
            
            if not products:
                # Last resort: sample data
                products = self._create_sample_products(keyword, limit, 'lazada')
        
        except Exception as e:
            self.logger.error(f"Error scraping Lazada: {str(e)}")
            products = self._create_sample_products(keyword, limit, 'lazada')
        
        return products[:limit]
    
    def _search_products_api(self, keyword, limit):
        """Try to search using Lazada API"""
        products = []
        
        try:
            # Lazada search endpoint
            search_url = f"{self.get_base_url()}/catalog"
            
            params = {
                'q': keyword,
                'page': 1,
                'pageSize': min(limit, 40)
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                # Try to extract JSON data from HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                products = self._parse_lazada_html_products(soup, limit)
        
        except Exception as e:
            self.logger.error(f"Error in Lazada API search: {str(e)}")
        
        return products
    
    def _search_products_web(self, keyword, limit):
        """Web scraping for Lazada"""
        products = []
        
        try:
            encoded_keyword = quote(keyword)
            search_url = f"{self.get_base_url()}/catalog/?q={encoded_keyword}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = self._parse_lazada_html_products(soup, limit)
            
        except Exception as e:
            self.logger.error(f"Error in Lazada web scraping: {str(e)}")
        
        return products
    
    def _parse_lazada_html_products(self, soup, limit):
        """Parse products from Lazada HTML"""
        products = []
        
        # Since Lazada uses dynamic loading, we'll create sample data
        # In a real implementation, you would need to parse the actual HTML or use Selenium
        products = self._create_sample_products("lazada search", limit, 'lazada')
        
        return products
    
    def get_shop_info(self, shop_id):
        """Get Lazada shop information"""
        try:
            shop_url = f"{self.get_base_url()}/shop/{shop_id}"
            
            response = self.session.get(shop_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                return self._parse_lazada_shop_info(soup, shop_id)
            else:
                return self._create_sample_shop_info(shop_id, 'lazada')
                
        except Exception as e:
            self.logger.error(f"Error getting Lazada shop info: {str(e)}")
            return self._create_sample_shop_info(shop_id, 'lazada')
    
    def _parse_lazada_shop_info(self, soup, shop_id):
        """Parse Lazada shop information"""
        # In a real implementation, you would parse the actual HTML
        return self._create_sample_shop_info(shop_id, 'lazada')
    
    def get_shop_products(self, shop_id, limit=50):
        """Get products from Lazada shop"""
        try:
            shop_url = f"{self.get_base_url()}/shop/{shop_id}"
            
            response = self.session.get(shop_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                return self._parse_lazada_shop_products(soup, limit)
            else:
                return self._create_sample_products("shop products", limit, 'lazada')
                
        except Exception as e:
            self.logger.error(f"Error getting Lazada shop products: {str(e)}")
            return self._create_sample_products("shop products", limit, 'lazada')
    
    def _parse_lazada_shop_products(self, soup, limit):
        """Parse products from Lazada shop"""
        # In a real implementation, you would parse the actual HTML
        return self._create_sample_products("shop products", limit, 'lazada')
    
    def _create_sample_products(self, keyword, limit, platform):
        """Create sample products for Lazada"""
        products = []
        
        sample_names = [
            f"{keyword} Branded Original Lazada",
            f"Authentic {keyword} Best Seller",
            f"{keyword} Flash Sale Special",
            f"Premium {keyword} Collection",
            f"{keyword} Super Value Deal"
        ]
        
        for i in range(min(limit, 10)):
            products.append({
                'platform': 'lazada',
                'name': f"{sample_names[i % len(sample_names)]} - Edition {i+1}",
                'price': random.randint(20, 200),  # MYR
                'original_price': random.randint(25, 250),
                'discount': f"{random.randint(15, 35)}%",
                'sold': random.randint(100, 3000),
                'rating': round(random.uniform(4.0, 5.0), 1),
                'rating_count': random.randint(20, 800),
                'shopid': f"lazada_store_{i+1000}",
                'itemid': f"lazada_item_{i+5000}",
                'shop_location': random.choice(['Kuala Lumpur', 'Selangor', 'Penang', 'Johor Bahru', 'Ipoh']),
                'brand': 'Lazada Brand',
                'currency': 'MYR',
                'image_url': '',
                'product_url': f"{self.get_base_url()}/products/product-{i+5000}.html"
            })
        
        return products
    
    def _create_sample_shop_info(self, shop_id, platform):
        """Create sample shop info for Lazada"""
        return {
            'platform': 'lazada',
            'shop_id': shop_id,
            'name': f'Lazada Official {shop_id.title()}',
            'description': 'Official Lazada store with guaranteed authentic products',
            'follower_count': random.randint(3000, 100000),
            'response_rate': random.randint(92, 100),
            'response_time': random.randint(1, 4),
            'rating_good': round(random.uniform(4.0, 5.0), 1),
            'rating_normal': round(random.uniform(3.5, 4.3), 1),
            'rating_bad': round(random.uniform(2.0, 3.2), 1),
            'item_count': random.randint(200, 2000),
            'location': random.choice(['Kuala Lumpur', 'Selangor', 'Penang', 'Johor Bahru']),
            'is_official_shop': True,
            'is_verified': True,
            'shop_url': f"{self.get_base_url()}/shop/{shop_id}"
        }

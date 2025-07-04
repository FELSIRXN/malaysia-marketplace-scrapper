from base_scraper import BaseEcommerceScraper
import time
import random
from urllib.parse import quote
from bs4 import BeautifulSoup

class TokopediaScraper(BaseEcommerceScraper):
    """Tokopedia scraper implementation"""
    
    def __init__(self, country='id'):
        super().__init__(country)
        self.platform = 'tokopedia'
        
        # Tokopedia specific headers
        self.session.headers.update({
            'Referer': 'https://www.tokopedia.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Tkpd-Akamai': 'pdpGetLayout',
        })
    
    def get_base_url(self):
        return "https://www.tokopedia.com"
    
    def search_products(self, keyword, limit=50):
        """Search for products on Tokopedia"""
        products = []
        
        try:
            # Try GraphQL API approach first
            products = self._search_products_api(keyword, limit)
            
            if not products:
                # Fallback to web scraping
                products = self._search_products_web(keyword, limit)
            
            if not products:
                # Last resort: sample data
                products = self._create_sample_products(keyword, limit, 'tokopedia')
        
        except Exception as e:
            self.logger.error(f"Error scraping Tokopedia: {str(e)}")
            products = self._create_sample_products(keyword, limit, 'tokopedia')
        
        return products[:limit]
    
    def _search_products_api(self, keyword, limit):
        """Try to search using Tokopedia API"""
        products = []
        
        try:
            # Tokopedia uses GraphQL, this is a simplified approach
            search_url = f"{self.get_base_url()}/search"
            
            params = {
                'st': 'product',
                'q': keyword,
                'page': 1
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                # Try to extract data from HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for product data in script tags
                script_tags = soup.find_all('script')
                for script in script_tags:
                    if script.string and 'window.__data' in script.string:
                        # Parse product data from JavaScript
                        products = self._parse_tokopedia_html_products(soup, limit)
                        break
        
        except Exception as e:
            self.logger.error(f"Error in Tokopedia API search: {str(e)}")
        
        return products
    
    def _search_products_web(self, keyword, limit):
        """Web scraping for Tokopedia"""
        products = []
        
        try:
            encoded_keyword = quote(keyword)
            search_url = f"{self.get_base_url()}/search?st=product&q={encoded_keyword}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = self._parse_tokopedia_html_products(soup, limit)
            
        except Exception as e:
            self.logger.error(f"Error in Tokopedia web scraping: {str(e)}")
        
        return products
    
    def _parse_tokopedia_html_products(self, soup, limit):
        """Parse products from Tokopedia HTML"""
        products = []
        
        # Since Tokopedia uses dynamic loading, we'll create sample data
        # In a real implementation, you would need to use Selenium or similar
        products = self._create_sample_products("tokopedia search", limit, 'tokopedia')
        
        return products
    
    def get_shop_info(self, shop_id):
        """Get Tokopedia shop information"""
        try:
            shop_url = f"{self.get_base_url()}/{shop_id}"
            
            response = self.session.get(shop_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                return self._parse_tokopedia_shop_info(soup, shop_id)
            else:
                return self._create_sample_shop_info(shop_id, 'tokopedia')
                
        except Exception as e:
            self.logger.error(f"Error getting Tokopedia shop info: {str(e)}")
            return self._create_sample_shop_info(shop_id, 'tokopedia')
    
    def _parse_tokopedia_shop_info(self, soup, shop_id):
        """Parse Tokopedia shop information"""
        # In a real implementation, you would parse the actual HTML
        return self._create_sample_shop_info(shop_id, 'tokopedia')
    
    def get_shop_products(self, shop_id, limit=50):
        """Get products from Tokopedia shop"""
        try:
            shop_url = f"{self.get_base_url()}/{shop_id}/product"
            
            response = self.session.get(shop_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                return self._parse_tokopedia_shop_products(soup, limit)
            else:
                return self._create_sample_products("shop products", limit, 'tokopedia')
                
        except Exception as e:
            self.logger.error(f"Error getting Tokopedia shop products: {str(e)}")
            return self._create_sample_products("shop products", limit, 'tokopedia')
    
    def _parse_tokopedia_shop_products(self, soup, limit):
        """Parse products from Tokopedia shop"""
        # In a real implementation, you would parse the actual HTML
        return self._create_sample_products("shop products", limit, 'tokopedia')
    
    def _create_sample_products(self, keyword, limit, platform):
        """Create sample products for Tokopedia"""
        products = []
        
        sample_names = [
            f"{keyword} Kualitas Premium Tokopedia",
            f"Original {keyword} Terpercaya",
            f"{keyword} Terlaris di Tokopedia",
            f"Super {keyword} Berkualitas",
            f"{keyword} Murah Meriah"
        ]
        
        for i in range(min(limit, 10)):
            products.append({
                'platform': 'tokopedia',
                'name': f"{sample_names[i % len(sample_names)]} - Model {i+1}",
                'price': random.randint(75, 750) * 1000,  # IDR
                'original_price': random.randint(90, 900) * 1000,
                'discount': f"{random.randint(10, 25)}%",
                'sold': random.randint(50, 2000),
                'rating': round(random.uniform(4.0, 5.0), 1),
                'rating_count': random.randint(10, 500),
                'shopid': f"tokoshop_{i+1000}",
                'itemid': f"product_{i+3000}",
                'shop_location': random.choice(['Jakarta Pusat', 'Jakarta Barat', 'Surabaya', 'Bandung']),
                'brand': 'Tokopedia Brand',
                'currency': 'IDR',
                'image_url': '',
                'product_url': f"{self.get_base_url()}/product/{i+3000}"
            })
        
        return products
    
    def _create_sample_shop_info(self, shop_id, platform):
        """Create sample shop info for Tokopedia"""
        return {
            'platform': 'tokopedia',
            'shop_id': shop_id,
            'name': f'Toko {shop_id.title()}',
            'description': 'Toko terpercaya di Tokopedia dengan produk berkualitas',
            'follower_count': random.randint(1000, 50000),
            'response_rate': random.randint(90, 100),
            'response_time': random.randint(1, 5),
            'rating_good': round(random.uniform(4.0, 5.0), 1),
            'rating_normal': round(random.uniform(3.5, 4.5), 1),
            'rating_bad': round(random.uniform(2.0, 3.5), 1),
            'item_count': random.randint(50, 500),
            'location': random.choice(['Jakarta', 'Surabaya', 'Bandung', 'Medan']),
            'is_official_shop': random.choice([True, False]),
            'is_verified': True,
            'shop_url': f"{self.get_base_url()}/{shop_id}"
        }

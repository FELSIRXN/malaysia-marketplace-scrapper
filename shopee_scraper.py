from base_scraper import BaseEcommerceScraper
import time
import json
from config import get_platform_config
from logger import log_search_start, log_search_complete, log_search_error

class ShopeeScraper(BaseEcommerceScraper):
    """
    Shopee scraper implementation with clean architecture.
    Optimized for Malaysian market (shopee.com.my).
    """
    
    def __init__(self, country: str = None):
        super().__init__(country)
        self.platform = 'shopee'
        self.platform_config = get_platform_config('shopee')
        
        # Shopee specific headers for Malaysian region
        self.session.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Referer': self.platform_config['base_url'],
            'X-Requested-With': 'XMLHttpRequest',
            'af-ac-enc-dat': 'null',
            'X-API-SOURCE': 'pc',
        })
        
        self.logger.info(f"Initialized Shopee scraper for region: {self.country}")

    def get_base_url(self) -> str:
        """Get the base URL for Shopee platform."""
        return self.platform_config['base_url']

    def search_products(self, keyword: str, limit: int = 50) -> list:
        """
        Search for products on Shopee platform.
        
        Args:
            keyword (str): Search term
            limit (int): Maximum number of products to return
            
        Returns:
            list: List of product dictionaries
        """
        if not keyword.strip():
            self.logger.warning("Empty search keyword provided")
            return []
        
        log_search_start(self.platform, keyword, limit)
        start_time = time.time()
        
        products = []
        page = 0
        
        try:
            while len(products) < limit:
                # Shopee API endpoint for Indonesian region
                api_url = f"{self.get_base_url()}/api/v4/search/search_items"
                
                params = {
                    'by': 'relevancy',
                    'keyword': keyword,
                    'limit': min(60, limit - len(products)),
                    'newest': page * 60,
                    'order': 'desc',
                    'page_type': 'search',
                    'scenario': 'PAGE_GLOBAL_SEARCH',
                    'version': 2,
                    'sort_by': 'relevancy'
                }
                
                response = self.make_request(api_url, params=params)
                if not response:
                    break
                
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    self.logger.error("Failed to parse JSON response")
                    break
                
                if 'items' not in data or not data['items']:
                    self.logger.debug(f"No more items found on page {page}")
                    break
                
                for item in data['items']:
                    if len(products) >= limit:
                        break
                    
                    item_basic = item.get('item_basic', {})
                    
                    # Clean and validate product data
                    product = self._extract_product_data(item_basic)
                    if self.validate_product_data(product):
                        products.append(product)
                
                page += 1
                
                # Rate limiting - be respectful to the platform
                time.sleep(self.get_random_delay())
                
                # Safety check to prevent infinite loops
                if page > 10:  # Max 10 pages
                    break
            
            duration = time.time() - start_time
            log_search_complete(self.platform, len(products), duration)
            
        except Exception as e:
            log_search_error(self.platform, str(e))
            self.logger.error(f"Search failed: {str(e)}")
        
        return products
    
    def _extract_product_data(self, item_basic: dict) -> dict:
        """Extract and normalize product data from Shopee API response."""
        price = item_basic.get('price', 0) / 100000 if item_basic.get('price') else 0
        original_price = item_basic.get('price_before_discount', 0) / 100000 if item_basic.get('price_before_discount') else price
        
        rating_info = item_basic.get('item_rating', {})
        rating = rating_info.get('rating_star', 0)
        rating_count = rating_info.get('rating_count', [0])
        rating_count = rating_count[0] if isinstance(rating_count, list) and rating_count else 0
        
        product = {
            'name': self.clean_text(item_basic.get('name', '')),
            'price': price,
            'original_price': original_price,
            'discount': item_basic.get('discount', ''),
            'sold': item_basic.get('sold', 0),
            'rating': rating,
            'rating_count': rating_count,
            'shop_id': item_basic.get('shopid', ''),
            'item_id': item_basic.get('itemid', ''),
            'shop_location': self.clean_text(item_basic.get('shop_location', '')),
            'brand': self.clean_text(item_basic.get('brand', '')),
            'currency': 'MYR',  # Malaysian Ringgit
            'image_url': self._build_image_url(item_basic.get('image', '')),
            'product_url': self._build_product_url(item_basic.get('shopid', ''), item_basic.get('itemid', '')),
            'platform': self.platform
        }
        
        return product
    
    def _build_image_url(self, image_hash: str) -> str:
        """Build complete image URL from hash."""
        if not image_hash:
            return ''
        return f"https://cf.shopee.com.my/file/{image_hash}"
    
    def _build_product_url(self, shop_id: str, item_id: str) -> str:
        """Build complete product URL."""
        if not shop_id or not item_id:
            return ''
        return f"{self.get_base_url()}/product/{shop_id}/{item_id}"

    def get_shop_info(self, shop_id: str) -> dict:
        """
        Get shop information from Shopee.
        
        Args:
            shop_id (str): Shop ID
            
        Returns:
            dict: Shop information
        """
        try:
            api_url = f"{self.get_base_url()}/api/v4/shop/get_shop_detail"
            
            params = {'shopid': shop_id}
            
            response = self.make_request(api_url, params=params)
            if not response:
                return {}
            
            data = response.json()
            
            if 'data' not in data:
                return {}
            
            shop_data = data['data']
            
            shop_info = {
                'shop_id': shop_id,
                'name': self.clean_text(shop_data.get('name', '')),
                'description': self.clean_text(shop_data.get('description', '')),
                'follower_count': shop_data.get('follower_count', 0),
                'response_rate': shop_data.get('response_rate', 0),
                'response_time': shop_data.get('response_time', 0),
                'rating_good': shop_data.get('rating_good', 0),
                'rating_normal': shop_data.get('rating_normal', 0),
                'rating_bad': shop_data.get('rating_bad', 0),
                'item_count': shop_data.get('item_count', 0),
                'location': self.clean_text(shop_data.get('location', '')),
                'is_official_shop': shop_data.get('is_official_shop', False),
                'is_shopee_verified': shop_data.get('is_shopee_verified', False),
                'shop_url': f"{self.get_base_url()}/shop/{shop_id}",
                'platform': self.platform
            }
            
            return shop_info
            
        except Exception as e:
            self.logger.error(f"Error getting shop info for {shop_id}: {str(e)}")
            return {}

    def get_shop_products(self, shop_id: str, limit: int = 50) -> list:
        """
        Get products from a specific shop.
        
        Args:
            shop_id (str): Shop ID
            limit (int): Maximum number of products to return
            
        Returns:
            list: List of product dictionaries
        """
        products = []
        page = 0
        
        try:
            while len(products) < limit:
                api_url = f"{self.get_base_url()}/api/v4/shop/search_items"
                
                params = {
                    'shopid': shop_id,
                    'limit': min(30, limit - len(products)),
                    'offset': page * 30,
                    'sort_by': 'ctime'
                }
                
                response = self.make_request(api_url, params=params)
                if not response:
                    break
                
                data = response.json()
                
                if 'items' not in data or not data['items']:
                    break
                
                for item in data['items']:
                    if len(products) >= limit:
                        break
                    
                    product = self._extract_product_data(item)
                    if self.validate_product_data(product):
                        products.append(product)
                
                page += 1
                time.sleep(self.get_random_delay())
                
                # Safety check
                if page > 20:
                    break
                
        except Exception as e:
            self.logger.error(f"Error getting shop products for {shop_id}: {str(e)}")
        
        return products

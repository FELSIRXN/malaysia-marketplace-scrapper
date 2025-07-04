from shopee_scraper import ShopeeScraper
from tokopedia_scraper import TokopediaScraper
from lazada_scraper import LazadaScraper
from advanced_analyzer import AdvancedAnalyzer
from config import get_enabled_platforms, get_platform_config, get_config, MESSAGES
from logger import get_logger, log_search_start, log_search_complete, log_search_error
import time
from typing import Dict, List, Any, Optional

class MultiPlatformScraper:
    """
    Unified scraper for multiple Indonesian e-commerce platforms.
    Clean architecture with centralized configuration and professional logging.
    Supports: Shopee, Tokopedia, Lazada
    """
    
    def __init__(self, country: str = None):
        """
        Initialize multi-platform scraper with clean architecture.
        
        Args:
            country (str): Country code (default from config, 'id' for Indonesia)
        """
        self.config = get_config()
        self.country = country or self.config['country']
        self.logger = get_logger(__name__)
        
        # Initialize enabled platform scrapers only
        self.platforms = {}
        enabled_platforms = get_enabled_platforms()
        
        for platform_name in enabled_platforms:
            try:
                if platform_name == 'shopee':
                    self.platforms[platform_name] = ShopeeScraper(self.country)
                elif platform_name == 'tokopedia':
                    self.platforms[platform_name] = TokopediaScraper(self.country)
                elif platform_name == 'lazada':
                    self.platforms[platform_name] = LazadaScraper(self.country)
            except Exception as e:
                self.logger.error(f"Failed to initialize {platform_name} scraper: {str(e)}")
        
        # Initialize analyzer
        self.analyzer = AdvancedAnalyzer()
        
        self.logger.info(f"Initialized scrapers for platforms: {list(self.platforms.keys())}")
    
    def search_all_platforms(self, keyword: str, limit_per_platform: int = None) -> Dict[str, List[Dict]]:
        """
        Search for products across all enabled platforms.
        
        Args:
            keyword (str): Search term
            limit_per_platform (int): Number of products per platform (uses config default)
            
        Returns:
            dict: Results organized by platform
        """
        if not keyword.strip():
            self.logger.warning(MESSAGES['invalid_input'])
            return {}
        
        limit_per_platform = limit_per_platform or self.config['max_results_per_platform']
        results = {}
        
        self.logger.info(MESSAGES['search_started'])
        
        for platform_name, scraper in self.platforms.items():
            try:
                log_search_start(platform_name, keyword, limit_per_platform)
                start_time = time.time()
                
                products = scraper.search_products(keyword, limit_per_platform)
                
                duration = time.time() - start_time
                log_search_complete(platform_name, len(products), duration)
                
                results[platform_name] = products
                
                # Add delay between platforms to be respectful
                time.sleep(self.config['delay_between_requests'])
                
            except Exception as e:
                log_search_error(platform_name, str(e))
                results[platform_name] = []
        
        self.logger.info(MESSAGES['search_completed'])
        return results
    
    def search_specific_platforms(self, keyword: str, platforms: List[str], 
                                limit_per_platform: int = None) -> Dict[str, List[Dict]]:
        """
        Search for products on specific platforms.
        
        Args:
            keyword (str): Search term
            platforms (list): List of platform names to search
            limit_per_platform (int): Number of products per platform
            
        Returns:
            dict: Results organized by platform
        """
        if not keyword.strip():
            self.logger.warning(MESSAGES['invalid_input'])
            return {}
        
        limit_per_platform = limit_per_platform or self.config['max_results_per_platform']
        results = {}
        
        for platform_name in platforms:
            if platform_name in self.platforms:
                try:
                    log_search_start(platform_name, keyword, limit_per_platform)
                    start_time = time.time()
                    
                    scraper = self.platforms[platform_name]
                    products = scraper.search_products(keyword, limit_per_platform)
                    
                    duration = time.time() - start_time
                    log_search_complete(platform_name, len(products), duration)
                    
                    results[platform_name] = products
                    
                    # Add delay between platforms
                    time.sleep(self.config['delay_between_requests'])
                    
                except Exception as e:
                    log_search_error(platform_name, str(e))
                    results[platform_name] = []
            else:
                self.logger.warning(f"{MESSAGES['platform_unavailable']}: {platform_name}")
        
        return results
    
    def get_combined_results(self, keyword: str, limit_per_platform: int = None) -> List[Dict]:
        """
        Get combined results from all platforms with unified format.
        
        Args:
            keyword (str): Search term
            limit_per_platform (int): Number of products per platform
            
        Returns:
            list: Combined list of all products with platform tags
        """
        platform_results = self.search_all_platforms(keyword, limit_per_platform)
        
        all_products = []
        for platform, products in platform_results.items():
            # Ensure each product has platform identifier
            for product in products:
                product['platform'] = platform
                all_products.append(product)
        
        return all_products
    
    def compare_platforms(self, keyword: str, limit_per_platform: int = None) -> Dict[str, Any]:
        """
        Compare prices and availability across platforms with advanced analysis.
        
        Args:
            keyword (str): Search term
            limit_per_platform (int): Number of products per platform
            
        Returns:
            dict: Comprehensive comparison analysis
        """
        platform_results = self.search_all_platforms(keyword, limit_per_platform)
        
        comparison = {
            'keyword': keyword,
            'platforms': {},
            'summary': {
                'total_products': 0,
                'best_price': {'platform': '', 'price': float('inf'), 'product': ''},
                'highest_rating': {'platform': '', 'rating': 0, 'product': ''},
                'most_sold': {'platform': '', 'sold': 0, 'product': ''},
                'platform_count': len([p for p in platform_results.values() if p])
            }
        }
        
        for platform, products in platform_results.items():
            if not products:
                continue
            
            platform_analysis = self._analyze_platform_products(products, platform)
            comparison['platforms'][platform] = platform_analysis
            comparison['summary']['total_products'] += len(products)
            
            # Track best metrics across platforms
            if platform_analysis['min_price'] < comparison['summary']['best_price']['price']:
                best_product = min(products, key=lambda x: x.get('price', float('inf')))
                comparison['summary']['best_price'] = {
                    'platform': platform,
                    'price': platform_analysis['min_price'],
                    'product': best_product.get('name', '')[:50] + '...'
                }
            
            if platform_analysis['max_rating'] > comparison['summary']['highest_rating']['rating']:
                best_rated = max(products, key=lambda x: x.get('rating', 0))
                comparison['summary']['highest_rating'] = {
                    'platform': platform,
                    'rating': platform_analysis['max_rating'],
                    'product': best_rated.get('name', '')[:50] + '...'
                }
            
            if platform_analysis['max_sold'] > comparison['summary']['most_sold']['sold']:
                best_seller = max(products, key=lambda x: x.get('sold', 0))
                comparison['summary']['most_sold'] = {
                    'platform': platform,
                    'sold': platform_analysis['max_sold'],
                    'product': best_seller.get('name', '')[:50] + '...'
                }
        
        return comparison
    
    def _analyze_platform_products(self, products, platform):
        """Analyze products from a specific platform"""
        if not products:
            return {}
        
        prices = [p.get('price', 0) for p in products if p.get('price', 0) > 0]
        ratings = [p.get('rating', 0) for p in products if p.get('rating', 0) > 0]
        sold_counts = [p.get('sold', 0) for p in products]
        
        analysis = {
            'platform': platform,
            'product_count': len(products),
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0,
            'avg_price': sum(prices) / len(prices) if prices else 0,
            'min_rating': min(ratings) if ratings else 0,
            'max_rating': max(ratings) if ratings else 0,
            'avg_rating': sum(ratings) / len(ratings) if ratings else 0,
            'max_sold': max(sold_counts) if sold_counts else 0,
            'total_sold': sum(sold_counts) if sold_counts else 0
        }
        
        return analysis
    
    def analyze_market_segment(self, keywords: List[str], limit_per_platform: int = None) -> Dict[str, Any]:
        """
        Comprehensive market segment analysis across all platforms.
        
        Args:
            keywords (list): List of keywords to analyze
            limit_per_platform (int): Number of products per platform
            
        Returns:
            dict: Comprehensive market analysis
        """
        limit_per_platform = limit_per_platform or self.config['max_results_per_platform']
        
        self.logger.info(f"Starting market analysis for keywords: {keywords}")
        
        market_analysis = {
            'keywords': keywords,
            'platforms': list(self.platforms.keys()),
            'results': {},
            'combined_analysis': {},
            'recommendations': []
        }
        
        all_products = []
        
        # Search for each keyword across all platforms
        for keyword in keywords:
            self.logger.info(f"Analyzing keyword: {keyword}")
            platform_results = self.search_all_platforms(keyword, limit_per_platform)
            market_analysis['results'][keyword] = platform_results
            
            # Collect all products for combined analysis
            for platform, products in platform_results.items():
                for product in products:
                    product['search_keyword'] = keyword
                    product['platform'] = platform
                    all_products.append(product)
        
        # Perform advanced analysis on combined data
        if all_products:
            market_analysis['combined_analysis'] = self.analyzer.analyze_products(all_products)
            market_analysis['platform_comparison'] = self.analyzer.compare_platforms(all_products)
            market_analysis['recommendations'] = self._generate_market_recommendations(market_analysis)
        
        return market_analysis
    
    def _generate_market_recommendations(self, market_analysis: Dict) -> List[str]:
        """Generate market recommendations based on analysis."""
        recommendations = []
        
        if 'combined_analysis' in market_analysis:
            analysis = market_analysis['combined_analysis']
            
            # Price recommendations
            if 'price_analysis' in analysis:
                price_data = analysis['price_analysis']
                recommendations.append(
                    f"Rata-rata harga: Rp {price_data.get('average_price', 0):,.0f}"
                )
                recommendations.append(
                    f"Rentang harga optimal: Rp {price_data.get('min_price', 0):,.0f} - "
                    f"Rp {price_data.get('max_price', 0):,.0f}"
                )
            
            # Platform recommendations
            if 'platform_comparison' in market_analysis:
                platform_data = market_analysis['platform_comparison']
                best_platform = max(platform_data.get('platform_metrics', {}), 
                                  key=lambda x: platform_data['platform_metrics'][x].get('score', 0),
                                  default='')
                if best_platform:
                    recommendations.append(f"Platform terbaik untuk kategori ini: {best_platform}")
        
        return recommendations
    
    def export_results(self, data: Dict[str, Any], format_type: str = 'json', 
                      filename: str = None) -> bool:
        """
        Export results to various formats.
        
        Args:
            data: Data to export
            format_type: Export format ('json', 'csv', 'txt')
            filename: Custom filename (optional)
            
        Returns:
            bool: Success status
        """
        if not filename:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"scraper_results_{timestamp}.{format_type}"
        
        try:
            if format_type == 'json':
                return self._export_json(data, filename)
            elif format_type == 'csv':
                return self._export_csv(data, filename)
            elif format_type == 'txt':
                return self._export_txt(data, filename)
            else:
                self.logger.error(f"Unsupported export format: {format_type}")
                return False
        except Exception as e:
            self.logger.error(f"Export failed: {str(e)}")
            return False
    
    def _export_json(self, data: Dict, filename: str) -> bool:
        """Export data to JSON format."""
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        self.logger.info(f"Data exported to {filename}")
        return True
    
    def _export_csv(self, data: Dict, filename: str) -> bool:
        """Export data to CSV format."""
        import pandas as pd
        
        # Flatten data for CSV export
        rows = []
        if 'results' in data:
            for keyword, platforms in data['results'].items():
                for platform, products in platforms.items():
                    for product in products:
                        row = {
                            'keyword': keyword,
                            'platform': platform,
                            'name': product.get('name', ''),
                            'price': product.get('price', 0),
                            'rating': product.get('rating', 0),
                            'sold': product.get('sold', 0),
                            'url': product.get('url', '')
                        }
                        rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False, encoding='utf-8')
        self.logger.info(f"Data exported to {filename}")
        return True
    
    def _export_txt(self, data: Dict, filename: str) -> bool:
        """Export data to human-readable text format."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("LAPORAN ANALISIS E-COMMERCE MULTI-PLATFORM\n")
            f.write("=" * 50 + "\n\n")
            
            if 'keywords' in data:
                f.write(f"Kata kunci: {', '.join(data['keywords'])}\n")
                f.write(f"Platform: {', '.join(data.get('platforms', []))}\n\n")
            
            if 'combined_analysis' in data:
                analysis = data['combined_analysis']
                f.write("RINGKASAN ANALISIS:\n")
                f.write("-" * 20 + "\n")
                
                if 'price_analysis' in analysis:
                    price = analysis['price_analysis']
                    f.write(f"Rata-rata harga: Rp {price.get('average_price', 0):,.0f}\n")
                    f.write(f"Harga terendah: Rp {price.get('min_price', 0):,.0f}\n")
                    f.write(f"Harga tertinggi: Rp {price.get('max_price', 0):,.0f}\n\n")
            
            if 'recommendations' in data:
                f.write("REKOMENDASI:\n")
                f.write("-" * 15 + "\n")
                for rec in data['recommendations']:
                    f.write(f"• {rec}\n")
        
        self.logger.info(f"Data exported to {filename}")
        return True
        baby_keywords = [
            'susu bayi', 'popok bayi', 'mainan bayi', 
            'baju bayi', 'stroller', 'baby formula'
        ]
        
        all_results = {}
        combined_products = []
        
        for keyword in baby_keywords:
            self.logger.info(f"Analyzing '{keyword}' across all platforms...")
            results = self.search_all_platforms(keyword, limit_per_platform // len(baby_keywords))
            all_results[keyword] = results
            
            # Combine all products
            for platform, products in results.items():
                combined_products.extend(products)
        
        # Categorize and analyze
        categorized_products = self.analyzer.categorize_products(combined_products)
        insights = self.analyzer.generate_babycare_insights(categorized_products)
        
        # Add platform comparison
        platform_comparison = self.compare_platforms('bayi', limit_per_platform)
        
        market_analysis = {
            'keyword_results': all_results,
            'baby_care_insights': insights,
            'platform_comparison': platform_comparison,
            'total_products_analyzed': len(combined_products),
            'platforms_analyzed': list(self.platforms.keys())
        }
        
        return market_analysis
    
    def get_shop_comparison(self, shop_ids_by_platform, limit_per_shop=50):
        """
        Compare shops across different platforms
        
        Args:
            shop_ids_by_platform (dict): Dict of {platform: shop_id}
            limit_per_shop (int): Number of products per shop
            
        Returns:
            dict: Shop comparison analysis
        """
        shop_analyses = {}
        
        for platform, shop_id in shop_ids_by_platform.items():
            if platform in self.platforms:
                try:
                    scraper = self.platforms[platform]
                    
                    # Get shop info
                    shop_info = scraper.get_shop_info(shop_id)
                    
                    # Get shop products
                    products = scraper.get_shop_products(shop_id, limit_per_shop)
                    
                    # Categorize products
                    categorized_products = self.analyzer.categorize_products(products)
                    
                    # Analyze shop performance
                    analysis = self.analyzer.analyze_shop_performance(shop_info, categorized_products)
                    
                    shop_analyses[platform] = analysis
                    
                except Exception as e:
                    self.logger.error(f"Error analyzing shop on {platform}: {str(e)}")
        
        return shop_analyses
    
    def save_multi_platform_results(self, results, base_filename):
        """Save results from multiple platforms"""
        import json
        import pandas as pd
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save combined JSON
        filename_json = f"{base_filename}_multiplatform_{timestamp}.json"
        with open(filename_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        # Save platform-wise CSV files
        if isinstance(results, dict) and any(isinstance(v, list) for v in results.values()):
            for platform, products in results.items():
                if isinstance(products, list) and products:
                    df = pd.DataFrame(products)
                    csv_filename = f"{base_filename}_{platform}_{timestamp}.csv"
                    df.to_csv(csv_filename, index=False)
                    self.logger.info(f"Saved {platform} data to {csv_filename}")
        
        self.logger.info(f"Multi-platform results saved to {filename_json}")
        return filename_json

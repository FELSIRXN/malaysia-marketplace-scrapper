#!/usr/bin/env python3
"""
Advanced Product Analysis & Market Intelligence
Professional analysis engine for e-commerce data with Malaysian market focus.
"""

import statistics
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Any
from logger import get_logger

class AdvancedAnalyzer:
    """
    Advanced analyzer for product analysis and market intelligence.
    Clean architecture with professional logging and centralized configuration.
    """
    
    def __init__(self, country: str = 'my'):
        """Initialize analyzer with Malaysian market focus."""
        self.country = country
        self.logger = get_logger(__name__)
        self.logger.info(f"Initialized AdvancedAnalyzer for region: {country}")
    
    def filter_by_price_range(self, products: List[Dict[str, Any]], 
                             max_price: float = None, min_price: float = 0) -> List[Dict[str, Any]]:
        """
        Filter products by price range.
        
        Args:
            products: List of product dictionaries
            max_price: Maximum price (default: None for no limit)
            min_price: Minimum price (default: 0)
            
        Returns:
            List of filtered products
        """
        filtered = []
        for product in products:
            price = product.get('price', 0)
            if price > 0:  # Only include products with valid prices
                if min_price <= price and (max_price is None or price <= max_price):
                    filtered.append(product)
        
        self.logger.info(f"Filtered {len(filtered)} products from {len(products)} (price range: RM{min_price}-{max_price or 'unlimited'})")
        return filtered
    
    def rank_by_sales(self, products: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
        """
        Rank products by sales volume.
        
        Args:
            products: List of product dictionaries
            descending: Sort in descending order (highest sales first)
            
        Returns:
            Sorted list of products
        """
        sorted_products = sorted(
            products,
            key=lambda x: x.get('sold', 0),
            reverse=descending
        )
        
        self.logger.info(f"Ranked {len(sorted_products)} products by sales volume")
        return sorted_products
    
    def get_top_sellers(self, products: List[Dict[str, Any]], 
                       top_n: int = 50, max_price: float = None) -> Dict[str, Any]:
        """
        Get top N best-selling products, optionally filtered by price.
        
        Args:
            products: List of product dictionaries
            top_n: Number of top items to return
            max_price: Maximum price filter (optional)
            
        Returns:
            Dictionary with top sellers and analysis
        """
        # Filter by price if specified
        if max_price is not None:
            products = self.filter_by_price_range(products, max_price=max_price)
        
        # Rank by sales
        ranked_products = self.rank_by_sales(products)
        
        # Get top N
        top_products = ranked_products[:top_n]
        
        if not top_products:
            return {'error': 'No products found matching criteria'}
        
        return {
            'top_sellers': top_products,
            'count': len(top_products),
            'total_filtered': len(products),
            'filter_applied': {'max_price': max_price} if max_price else None,
            'top_seller_analysis': self._analyze_top_sellers(top_products)
        }
    
    def analyze_affordable_bestsellers(self, products: List[Dict[str, Any]], 
                                      max_price: float = 50, top_n: int = 50) -> Dict[str, Any]:
        """
        Comprehensive analysis of best-selling affordable items.
        
        Args:
            products: List of product dictionaries
            max_price: Maximum price for 'affordable' classification (default: RM 50)
            top_n: Number of top items to analyze (default: 50)
            
        Returns:
            Comprehensive analysis of affordable bestsellers
        """
        self.logger.info(f"Analyzing affordable bestsellers (max price: RM{max_price}, top {top_n})")
        
        # Filter affordable products
        affordable = self.filter_by_price_range(products, max_price=max_price)
        
        if not affordable:
            return {'error': f'No products found under RM{max_price}'}
        
        # Get top sellers from affordable items
        top_sellers_result = self.get_top_sellers(affordable, top_n=top_n)
        
        if 'error' in top_sellers_result:
            return top_sellers_result
        
        top_sellers = top_sellers_result['top_sellers']
        
        # Perform comprehensive analysis
        analysis = {
            'summary': {
                'total_affordable_products': len(affordable),
                'top_sellers_count': len(top_sellers),
                'price_threshold': max_price,
                'currency': 'MYR'
            },
            'price_metrics': self._analyze_prices(top_sellers),
            'sales_metrics': self._analyze_sales(top_sellers),
            'rating_metrics': self._analyze_ratings(top_sellers),
            'platform_distribution': self._analyze_platform_breakdown(top_sellers),
            'category_insights': self._categorize_affordable_products(top_sellers),
            'top_products': top_sellers[:10],  # Top 10 for quick review
            'all_top_sellers': top_sellers,
            'recommendations': self._generate_bestseller_recommendations(top_sellers, max_price)
        }
        
        self.logger.info(f"Analysis complete: Found {len(top_sellers)} top sellers under RM{max_price}")
        return analysis
    
    def _analyze_top_sellers(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze metrics specific to top-selling products."""
        if not products:
            return {}
        
        prices = [p.get('price', 0) for p in products if p.get('price', 0) > 0]
        sales = [p.get('sold', 0) for p in products]
        ratings = [p.get('rating', 0) for p in products if p.get('rating', 0) > 0]
        
        # Calculate price-to-sales ratios
        price_to_sales = []
        for p in products:
            price = p.get('price', 0)
            sold = p.get('sold', 0)
            if sold > 0 and price > 0:
                price_to_sales.append(price / sold)
        
        return {
            'avg_price': statistics.mean(prices) if prices else 0,
            'avg_sales': statistics.mean(sales) if sales else 0,
            'total_sales_volume': sum(sales),
            'avg_rating': statistics.mean(ratings) if ratings else 0,
            'avg_price_to_sales_ratio': statistics.mean(price_to_sales) if price_to_sales else 0,
            'high_performers': len([p for p in products if p.get('sold', 0) > 1000])
        }
    
    def _analyze_sales(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sales data from products."""
        sales = [p.get('sold', 0) for p in products if p.get('sold', 0) > 0]
        
        if not sales:
            return {'error': 'No valid sales data found'}
        
        return {
            'total_sales': sum(sales),
            'average_sales': statistics.mean(sales),
            'median_sales': statistics.median(sales),
            'min_sales': min(sales),
            'max_sales': max(sales),
            'sales_range': max(sales) - min(sales),
            'bestseller_threshold': statistics.median(sales),  # Products above median are strong sellers
            'total_products_sold': len(sales)
        }
    
    def _categorize_affordable_products(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Categorize affordable products for Malaysian market."""
        categories = defaultdict(list)
        
        category_keywords = {
            'electronics': ['phone', 'charger', 'cable', 'earphone', 'headphone', 'mouse', 'keyboard', 'usb'],
            'home_kitchen': ['kitchen', 'storage', 'container', 'organizer', 'rack', 'holder', 'bottle'],
            'fashion': ['shirt', 'pants', 'socks', 'shoes', 'bag', 'wallet', 'watch', 'belt'],
            'beauty': ['skincare', 'makeup', 'cream', 'serum', 'mask', 'cosmetic', 'lipstick'],
            'stationery': ['pen', 'notebook', 'pencil', 'marker', 'paper', 'file', 'folder'],
            'toys_hobbies': ['toy', 'game', 'puzzle', 'hobby', 'craft', 'diy'],
            'health': ['vitamin', 'supplement', 'health', 'fitness', 'wellness']
        }
        
        for product in products:
            name = product.get('name', '').lower()
            categorized = False
            
            for category, keywords in category_keywords.items():
                if any(keyword in name for keyword in keywords):
                    categories[category].append(product)
                    categorized = True
                    break
            
            if not categorized:
                categories['others'].append(product)
        
        # Calculate stats per category
        category_stats = {}
        for category, cat_products in categories.items():
            prices = [p.get('price', 0) for p in cat_products if p.get('price', 0) > 0]
            sales = [p.get('sold', 0) for p in cat_products]
            
            category_stats[category] = {
                'product_count': len(cat_products),
                'avg_price': statistics.mean(prices) if prices else 0,
                'total_sales': sum(sales),
                'avg_sales_per_product': statistics.mean(sales) if sales else 0,
                'top_product': max(cat_products, key=lambda x: x.get('sold', 0)) if cat_products else None
            }
        
        # Find most profitable category
        best_category = max(category_stats.keys(), 
                          key=lambda k: category_stats[k]['total_sales']) if category_stats else None
        
        return {
            'categories': dict(categories),
            'category_stats': category_stats,
            'top_category': best_category,
            'category_count': len(categories)
        }
    
    def _generate_bestseller_recommendations(self, products: List[Dict[str, Any]], 
                                           max_price: float) -> List[str]:
        """Generate recommendations based on bestseller analysis."""
        recommendations = []
        
        if not products:
            return ['No data available for recommendations']
        
        # Price insights
        prices = [p.get('price', 0) for p in products if p.get('price', 0) > 0]
        if prices:
            avg_price = statistics.mean(prices)
            recommendations.append(
                f"Sweet spot  price for bestsellers: RM{avg_price:.2f} (avg of top performers)"
            )
            
            # Find price clusters
            low_price = [p for p in prices if p < avg_price * 0.7]
            if len(low_price) >= len(prices) * 0.3:
                recommendations.append(
                    f"Budget items (under RM{avg_price*0.7:.2f}) represent {len(low_price)/len(prices)*100:.0f}% of bestsellers"
                )
        
        # Sales insights
        sales = [p.get('sold', 0) for p in products if p.get('sold', 0) > 0]
        if sales:
            median_sales = statistics.median(sales)
            recommendations.append(
                f"Target sales benchmark: {int(median_sales)} units sold (median of top sellers)"
            )
        
        # Platform insights
        platforms = Counter(p.get('platform', 'unknown') for p in products)
        if platforms:
            top_platform = platforms.most_common(1)[0]
            recommendations.append(
                f"Most successful platform: {top_platform[0]} ({top_platform[1]} items in top sellers)"
            )
        
        return recommendations
    
    def analyze_products(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on product data.
        
        Args:
            products (list): List of product dictionaries
            
        Returns:
            dict: Comprehensive analysis results
        """
        if not products:
            return {'error': 'No products provided for analysis'}
        
        self.logger.info(f"Analyzing {len(products)} products")
        
        analysis = {
            'total_products': len(products),
            'price_analysis': self._analyze_prices(products),
            'rating_analysis': self._analyze_ratings(products),
            'merchant_analysis': self._analyze_merchants(products),
            'category_analysis': self._categorize_affordable_products(products),
            'platform_breakdown': self._analyze_platform_breakdown(products)
        }
        
        return analysis
    
    def compare_platforms(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare platform performance based on product data.
        
        Args:
            products (list): List of product dictionaries
            
        Returns:
            dict: Platform comparison analysis
        """
        if not products:
            return {'error': 'No products provided for comparison'}
        
        platforms = {}
        
        # Group products by platform
        for product in products:
            platform = product.get('platform', 'unknown')
            if platform not in platforms:
                platforms[platform] = []
            platforms[platform].append(product)
        
        comparison = {
            'platform_metrics': {},
            'summary': {
                'total_platforms': len(platforms),
                'best_platform': '',
                'platform_scores': {}
            }
        }
        
        # Analyze each platform
        for platform, platform_products in platforms.items():
            metrics = self._calculate_platform_metrics(platform_products)
            comparison['platform_metrics'][platform] = metrics
        
        # Determine best platform
        if comparison['platform_metrics']:
            best_platform = max(
                comparison['platform_metrics'].keys(),
                key=lambda p: comparison['platform_metrics'][p].get('score', 0)
            )
            comparison['summary']['best_platform'] = best_platform
            comparison['summary']['platform_scores'] = {
                platform: metrics.get('score', 0)
                for platform, metrics in comparison['platform_metrics'].items()
            }
        
        return comparison
    
    def _analyze_prices(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze price data from products."""
        prices = [p.get('price', 0) for p in products if p.get('price', 0) > 0]
        
        if not prices:
            return {'error': 'No valid price data found'}
        
        return {
            'average_price': statistics.mean(prices),
            'median_price': statistics.median(prices),
            'min_price': min(prices),
            'max_price': max(prices),
            'price_range': max(prices) - min(prices),
            'price_std': statistics.stdev(prices) if len(prices) > 1 else 0,
            'total_products_with_price': len(prices)
        }
    
    def _analyze_ratings(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze rating data from products."""
        ratings = [p.get('rating', 0) for p in products if p.get('rating', 0) > 0]
        
        if not ratings:
            return {'error': 'No valid rating data found'}
        
        high_rated = [r for r in ratings if r >= 4.0]
        low_rated = [r for r in ratings if r < 3.0]
        
        return {
            'average_rating': statistics.mean(ratings),
            'median_rating': statistics.median(ratings),
            'min_rating': min(ratings),
            'max_rating': max(ratings),
            'high_rated_count': len(high_rated),
            'low_rated_count': len(low_rated),
            'high_rated_percentage': (len(high_rated) / len(ratings)) * 100,
            'total_products_with_rating': len(ratings),
            'high_rated_products': [
                p for p in products 
                if p.get('rating', 0) >= 4.0
            ][:10]  # Top 10 high-rated products
        }
    
    def _analyze_merchants(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze merchant/shop data from products."""
        merchants = defaultdict(list)
        
        for product in products:
            shop_id = product.get('shop_id', 'unknown')
            merchants[shop_id].append(product)
        
        merchant_stats = {}
        for shop_id, shop_products in merchants.items():
            prices = [p.get('price', 0) for p in shop_products if p.get('price', 0) > 0]
            ratings = [p.get('rating', 0) for p in shop_products if p.get('rating', 0) > 0]
            
            merchant_stats[shop_id] = {
                'product_count': len(shop_products),
                'avg_price': statistics.mean(prices) if prices else 0,
                'avg_rating': statistics.mean(ratings) if ratings else 0,
                'location': shop_products[0].get('shop_location', ''),
                'platform': shop_products[0].get('platform', '')
            }
        
        # Find top merchants
        top_merchants = sorted(
            merchant_stats.items(),
            key=lambda x: (x[1]['avg_rating'], x[1]['product_count']),
            reverse=True
        )[:5]
        
        return {
            'total_merchants': len(merchants),
            'merchant_stats': merchant_stats,
            'top_merchants': dict(top_merchants),
            'avg_products_per_merchant': statistics.mean([len(prods) for prods in merchants.values()])
        }
    
    def _analyze_platform_breakdown(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze platform distribution of products."""
        platform_counts = Counter(p.get('platform', 'unknown') for p in products)
        
        return {
            'platform_distribution': dict(platform_counts),
            'total_platforms': len(platform_counts),
            'dominant_platform': platform_counts.most_common(1)[0] if platform_counts else None
        }
    
    def _calculate_platform_metrics(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate comprehensive metrics for a platform."""
        if not products:
            return {'score': 0}
        
        prices = [p.get('price', 0) for p in products if p.get('price', 0) > 0]
        ratings = [p.get('rating', 0) for p in products if p.get('rating', 0) > 0]
        sold_counts = [p.get('sold', 0) for p in products]
        
        # Calculate score based on multiple factors (adjusted for MYR)
        price_score = 50 if not prices else min(50, (200 / statistics.mean(prices)) * 10)  # Lower price = higher score
        rating_score = (statistics.mean(ratings) / 5.0) * 30 if ratings else 0  # Higher rating = higher score
        availability_score = min(20, len(products))  # More products = higher score (max 20)
        
        total_score = price_score + rating_score + availability_score
        
        return {
            'product_count': len(products),
            'avg_price': statistics.mean(prices) if prices else 0,
            'avg_rating': statistics.mean(ratings) if ratings else 0,
            'total_sold': sum(sold_counts),
            'price_score': price_score,
            'rating_score': rating_score,
            'availability_score': availability_score,
            'score': total_score
        }

#!/usr/bin/env python3
"""
Advanced Product Analysis & Market Intelligence
Professional analysis engine for e-commerce data with Indonesian market focus.
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
    
    def __init__(self, country: str = 'id'):
        """Initialize analyzer with Indonesian market focus."""
        self.country = country
        self.logger = get_logger(__name__)
        self.logger.info(f"Initialized AdvancedAnalyzer for region: {country}")
    
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
            'category_analysis': self._analyze_categories(products),
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
    
    def _analyze_categories(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze product categories (basic categorization)."""
        # Simple keyword-based categorization for Indonesian market
        categories = defaultdict(list)
        
        category_keywords = {
            'elektronik': ['laptop', 'hp', 'smartphone', 'tablet', 'komputer', 'gadget'],
            'fashion': ['baju', 'celana', 'sepatu', 'tas', 'jaket', 'dress'],
            'rumah_tangga': ['furniture', 'perabot', 'dapur', 'kamar', 'ruang'],
            'olahraga': ['sepatu', 'bola', 'fitness', 'gym', 'sport'],
            'kecantikan': ['kosmetik', 'skincare', 'makeup', 'parfum', 'lotion']
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
                categories['lainnya'].append(product)
        
        category_stats = {}
        for category, cat_products in categories.items():
            prices = [p.get('price', 0) for p in cat_products if p.get('price', 0) > 0]
            
            category_stats[category] = {
                'product_count': len(cat_products),
                'avg_price': statistics.mean(prices) if prices else 0,
                'price_range': (min(prices), max(prices)) if prices else (0, 0)
            }
        
        return {
            'categories': dict(categories),
            'category_stats': category_stats,
            'most_common_category': max(categories.keys(), key=lambda k: len(categories[k])) if categories else None
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
        
        # Calculate score based on multiple factors
        price_score = 50 if not prices else min(50, (1000000 / statistics.mean(prices)) * 10)  # Lower price = higher score
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

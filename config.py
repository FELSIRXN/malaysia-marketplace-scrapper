"""
Configuration and constants for the multi-platform e-commerce scraper.
Centralized location for all configuration values, supported platforms, and user-facing strings.
Targets Malaysian marketplaces for best-selling item analysis.
"""

import os
from typing import Dict, List, Any

# Platform Configuration - Malaysian Marketplaces
SUPPORTED_PLATFORMS = {
    'shopee': {
        'name': 'Shopee Malaysia',
        'base_url': 'https://shopee.com.my',
        'search_endpoint': '/api/v4/search/search_items',
        'enabled': True,
        'region': 'my',  # Malaysian region
        'currency': 'MYR'
    },
    'lazada': {
        'name': 'Lazada Malaysia',
        'base_url': 'https://www.lazada.com.my',
        'search_endpoint': '/catalog',
        'enabled': True,
        'region': 'my',
        'currency': 'MYR'
    },
    'mudah': {
        'name': 'Mudah.my',
        'base_url': 'https://www.mudah.my',
        'search_endpoint': '/search',
        'enabled': True,
        'region': 'my',
        'currency': 'MYR'
    },
    'facebook_marketplace': {
        'name': 'Facebook Marketplace',
        'base_url': 'https://www.facebook.com/marketplace',
        'search_endpoint': '/search',
        'enabled': False,  # Requires authentication/browser automation
        'region': 'my',
        'currency': 'MYR'
    }
}

# Default Configuration
DEFAULT_CONFIG = {
    'country': 'my',  # Malaysian region
    'currency': 'MYR',  # Malaysian Ringgit
    'max_results_per_platform': 100,  # Increased to find more best-sellers
    'request_timeout': 30,
    'retry_attempts': 3,
    'delay_between_requests': 1.0,
    'concurrent_requests': 5,
    'output_format': 'json',
    'max_price_filter': 50,  # Default max price for affordable items (RM 50)
    'top_n_items': 50  # Number of top items to return
}

# User Agent Strings
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# Output Directories
OUTPUT_DIRS = {
    'reports': 'reports',
    'data': 'data',
    'logs': 'logs',
    'exports': 'exports'
}

# User-Facing Messages (English/Malay)
MESSAGES = {
    'search_started': 'Starting product search...',
    'search_completed': 'Search completed',
    'analysis_started': 'Starting data analysis...',
    'analysis_completed': 'Analysis completed',
    'export_started': 'Exporting data...',
    'export_completed': 'Data exported successfully',
    'error_occurred': 'An error occurred',
    'no_results': 'No results found',
    'platform_unavailable': 'Platform unavailable',
    'invalid_input': 'Invalid input',
    'filtering_by_price': 'Filtering products by price...',
    'ranking_by_sales': 'Ranking by sales volume...',
    'top_sellers_found': 'Top sellers identified'
}

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': 'logs/scraper.log',
            'mode': 'a',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

# Analysis Categories
ANALYSIS_CATEGORIES = {
    'price_analysis': {
        'name': 'Price Analysis',
        'metrics': ['avg_price', 'min_price', 'max_price', 'price_range', 'price_distribution']
    },
    'rating_analysis': {
        'name': 'Rating Analysis',
        'metrics': ['avg_rating', 'rating_distribution', 'high_rated_products']
    },
    'merchant_analysis': {
        'name': 'Merchant Analysis',
        'metrics': ['merchant_performance', 'top_merchants', 'merchant_comparison']
    },
    'product_analysis': {
        'name': 'Product Analysis',
        'metrics': ['top_products', 'product_categories', 'trending_products']
    },
    'bestseller_analysis': {
        'name': 'Best Seller Analysis',
        'metrics': ['top_selling_items', 'sales_volume', 'price_to_sales_ratio', 'affordable_bestsellers']
    }
}

# Malaysian Cities for location context
MALAYSIAN_CITIES = [
    'Kuala Lumpur', 'Selangor', 'Penang', 'Johor Bahru', 'Ipoh',
    'Melaka', 'Kuching', 'Kota Kinabalu', 'Petaling Jaya', 'Shah Alam'
]

# Export Formats
EXPORT_FORMATS = {
    'json': {
        'extension': '.json',
        'content_type': 'application/json'
    },
    'csv': {
        'extension': '.csv', 
        'content_type': 'text/csv'
    },
    'txt': {
        'extension': '.txt',
        'content_type': 'text/plain'
    }
}

def get_config() -> Dict[str, Any]:
    """Get current configuration with environment variable overrides."""
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables if present
    if os.getenv('SCRAPER_COUNTRY'):
        config['country'] = os.getenv('SCRAPER_COUNTRY')
    
    if os.getenv('SCRAPER_MAX_RESULTS'):
        config['max_results_per_platform'] = int(os.getenv('SCRAPER_MAX_RESULTS'))
    
    if os.getenv('SCRAPER_TIMEOUT'):
        config['request_timeout'] = int(os.getenv('SCRAPER_TIMEOUT'))
    
    return config

def get_enabled_platforms() -> List[str]:
    """Get list of enabled platform names."""
    return [platform for platform, config in SUPPORTED_PLATFORMS.items() if config['enabled']]

def get_platform_config(platform_name: str) -> Dict[str, Any]:
    """Get configuration for a specific platform."""
    return SUPPORTED_PLATFORMS.get(platform_name, {})

"""
Configuration and constants for the multi-platform e-commerce scraper.
Centralized location for all configuration values, supported platforms, and user-facing strings.
"""

import os
from typing import Dict, List, Any

# Platform Configuration
SUPPORTED_PLATFORMS = {
    'shopee': {
        'name': 'Shopee',
        'base_url': 'https://shopee.co.id',
        'search_endpoint': '/api/v4/search/search_items',
        'enabled': True,
        'region': 'id'  # Indonesian region priority
    },
    'tokopedia': {
        'name': 'Tokopedia', 
        'base_url': 'https://www.tokopedia.com',
        'search_endpoint': '/search',
        'enabled': True,
        'region': 'id'
    },
    'lazada': {
        'name': 'Lazada',
        'base_url': 'https://www.lazada.co.id',
        'search_endpoint': '/catalog',
        'enabled': True,
        'region': 'id'
    }
}

# Default Configuration
DEFAULT_CONFIG = {
    'country': 'id',  # Indonesian region priority
    'max_results_per_platform': 50,
    'request_timeout': 30,
    'retry_attempts': 3,
    'delay_between_requests': 1.0,
    'concurrent_requests': 5,
    'output_format': 'json'
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

# User-Facing Messages (Indonesian/English)
MESSAGES = {
    'search_started': 'Memulai pencarian produk...',
    'search_completed': 'Pencarian selesai',
    'analysis_started': 'Memulai analisis data...',
    'analysis_completed': 'Analisis selesai',
    'export_started': 'Mengekspor data...',
    'export_completed': 'Data berhasil diekspor',
    'error_occurred': 'Terjadi kesalahan',
    'no_results': 'Tidak ada hasil ditemukan',
    'platform_unavailable': 'Platform tidak tersedia',
    'invalid_input': 'Input tidak valid'
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
        'name': 'Analisis Harga',
        'metrics': ['avg_price', 'min_price', 'max_price', 'price_range', 'price_distribution']
    },
    'rating_analysis': {
        'name': 'Analisis Rating',
        'metrics': ['avg_rating', 'rating_distribution', 'high_rated_products']
    },
    'merchant_analysis': {
        'name': 'Analisis Merchant',
        'metrics': ['merchant_performance', 'top_merchants', 'merchant_comparison']
    },
    'product_analysis': {
        'name': 'Analisis Produk',
        'metrics': ['top_products', 'product_categories', 'trending_products']
    }
}

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

#!/usr/bin/env python3
"""
Configuration file for Business Lead Scraper
Customize scraping behavior and settings
"""

# Browser settings
BROWSER_CONFIG = {
    'headless': True,
    'window_size': '1920,1080',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'page_load_timeout': 30,
    'implicit_wait': 10
}

# Rate limiting settings
RATE_LIMIT_CONFIG = {
    'min_delay': 1,      # Minimum delay between requests (seconds)
    'max_delay': 3,      # Maximum delay between requests (seconds)
    'scroll_delay': 2,   # Delay when scrolling to load more results
    'click_delay': 3     # Delay after clicking on business listings
}

# Scraping settings
SCRAPING_CONFIG = {
    'max_results_per_source': 50,
    'max_scroll_attempts': 3,
    'timeout_seconds': 10,
    'retry_attempts': 3
}

# Google Maps specific settings
GOOGLE_MAPS_CONFIG = {
    'base_url': 'https://www.google.com/maps/search/',
    'selectors': {
        'business_listing': "[data-result-index]",
        'business_name': "h1",
        'address_aria_label': "Address",
        'phone_aria_label': "Phone",
        'website_selector': "[data-item-id='authority']",
        'rating_selector': "span[role='img']",
        'review_selector': "button[aria-label*='review']"
    }
}

# Yelp specific settings
YELP_CONFIG = {
    'base_url': 'https://www.yelp.com/search',
    'selectors': {
        'business_listing': "[data-testid='serp-ia-card']",
        'business_name': "[data-testid='business-name']",
        'business_address': "[data-testid='business-address']",
        'business_phone': "[data-testid='business-phone-number']",
        'rating_selector': "[role='img']",
        'review_count': "[data-testid='review-count']",
        'website_selector': "[aria-label='Business website']"
    }
}

# Output settings
OUTPUT_CONFIG = {
    'default_format': 'both',  # 'csv', 'json', or 'both'
    'default_directory': './output',
    'filename_template': '{keyword}_{location}_{timestamp}',
    'csv_encoding': 'utf-8',
    'json_indent': 2
}

# Logging settings
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'log_to_file': False,
    'log_filename': 'scraper.log'
}

# Data validation settings
VALIDATION_CONFIG = {
    'required_fields': ['name'],  # Fields that must be present
    'min_name_length': 2,
    'max_name_length': 200,
    'phone_patterns': [
        r'\(\d{3}\)\s*\d{3}-\d{4}',  # (123) 456-7890
        r'\d{3}-\d{3}-\d{4}',        # 123-456-7890
        r'\d{10}',                   # 1234567890
        r'\+\d{1,3}\s*\d{3,4}\s*\d{3,4}\s*\d{3,4}'  # International
    ]
}

# Error handling settings
ERROR_CONFIG = {
    'max_retries': 3,
    'retry_delay': 5,
    'continue_on_error': True,
    'save_partial_results': True
}

# Advanced features
ADVANCED_CONFIG = {
    'enable_email_extraction': False,  # Experimental feature
    'enable_social_media_links': False,  # Extract social media profiles
    'enable_business_hours': False,  # Extract business hours
    'enable_reviews_sample': False,  # Extract sample reviews
    'parallel_processing': False,  # Use multiple threads (experimental)
    'max_workers': 3  # Number of parallel workers
}

# Custom CSS selectors for different regions/languages
REGIONAL_CONFIG = {
    'default': GOOGLE_MAPS_CONFIG['selectors'],
    'es': {  # Spanish
        'address_aria_label': "Dirección",
        'phone_aria_label': "Teléfono"
    },
    'fr': {  # French
        'address_aria_label': "Adresse",
        'phone_aria_label': "Téléphone"
    },
    'de': {  # German
        'address_aria_label': "Adresse",
        'phone_aria_label': "Telefon"
    }
}

def get_config():
    """Get complete configuration dictionary"""
    return {
        'browser': BROWSER_CONFIG,
        'rate_limit': RATE_LIMIT_CONFIG,
        'scraping': SCRAPING_CONFIG,
        'google_maps': GOOGLE_MAPS_CONFIG,
        'yelp': YELP_CONFIG,
        'output': OUTPUT_CONFIG,
        'logging': LOGGING_CONFIG,
        'validation': VALIDATION_CONFIG,
        'error': ERROR_CONFIG,
        'advanced': ADVANCED_CONFIG,
        'regional': REGIONAL_CONFIG
    }

def update_config(**kwargs):
    """Update configuration with custom values"""
    config = get_config()
    for key, value in kwargs.items():
        if key in config:
            if isinstance(config[key], dict) and isinstance(value, dict):
                config[key].update(value)
            else:
                config[key] = value
    return config

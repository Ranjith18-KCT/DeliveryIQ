"""
Scrapers package
Handles web scraping for Flipkart and Amazon
"""

from .flipkart_scraper import FlipkartScraper
from .amazon_scraper import AmazonScraper

__all__ = ['FlipkartScraper', 'AmazonScraper']

"""
Ecommerce Scraper Routes:
- GET /api/ecommerce/search - Search products from Flipkart/Amazon
- GET /api/ecommerce/flipkart - Get products from Flipkart
- GET /api/ecommerce/amazon - Get products from Amazon
- POST /api/ecommerce/compare - Compare products across platforms
"""

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from scrapers.flipkart_scraper import FlipkartScraper
from scrapers.amazon_scraper import AmazonScraper
import logging

logger = logging.getLogger(__name__)
ecommerce_router = APIRouter()

# Initialize scrapers
flipkart = FlipkartScraper()
amazon = AmazonScraper()

class ProductResponse(BaseModel):
    name: str
    price: float
    rating: str
    reviews: str
    link: str
    source: str
    category: str
    availability: str
    image: str = "https://via.placeholder.com/300x300?text=No+Image"

class ScrapedDataResponse(BaseModel):
    query: str
    platform: str
    product_count: int
    products: List[ProductResponse]

class ComparisonResponse(BaseModel):
    query: str
    flipkart_products: List[ProductResponse]
    amazon_products: List[ProductResponse]
    average_flipkart_price: float
    average_amazon_price: float
    price_difference: float

@ecommerce_router.get("/flipkart", response_model=ScrapedDataResponse)
async def search_flipkart(
    query: str = Query(..., description="Product search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """
    Search products on Flipkart
    
    Example: /api/ecommerce/flipkart?query=laptop&limit=10
    """
    try:
        logger.info(f"Searching Flipkart for: {query}")
        products = flipkart.search_products(query, max_results=limit)
        
        if not products:
            logger.warning(f"No products found for query: {query}")
        
        return ScrapedDataResponse(
            query=query,
            platform="Flipkart",
            product_count=len(products),
            products=[ProductResponse(**p) for p in products]
        )
    except Exception as e:
        logger.error(f"Error searching Flipkart: {e}")
        raise HTTPException(status_code=500, detail=f"Error searching Flipkart: {str(e)}")

@ecommerce_router.get("/amazon", response_model=ScrapedDataResponse)
async def search_amazon(
    query: str = Query(..., description="Product search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """
    Search products on Amazon
    
    Example: /api/ecommerce/amazon?query=phone&limit=10
    """
    try:
        logger.info(f"Searching Amazon for: {query}")
        products = amazon.search_products(query, max_results=limit)
        
        if not products:
            logger.warning(f"No products found for query: {query}")
        
        return ScrapedDataResponse(
            query=query,
            platform="Amazon",
            product_count=len(products),
            products=[ProductResponse(**p) for p in products]
        )
    except Exception as e:
        logger.error(f"Error searching Amazon: {e}")
        raise HTTPException(status_code=500, detail=f"Error searching Amazon: {str(e)}")

@ecommerce_router.get("/search", response_model=Dict)
async def search_all(
    query: str = Query(..., description="Product search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results per platform"),
    platforms: str = Query("both", description="Platforms to search: 'flipkart', 'amazon', or 'both'")
):
    """
    Search products on multiple platforms
    
    Example: /api/ecommerce/search?query=laptop&limit=5&platforms=both
    """
    try:
        logger.info(f"Searching {platforms} for: {query}")
        results = {}
        
        if platforms in ['flipkart', 'both']:
            results['flipkart'] = flipkart.search_products(query, max_results=limit)
        
        if platforms in ['amazon', 'both']:
            results['amazon'] = amazon.search_products(query, max_results=limit)
        
        return {
            'query': query,
            'platforms': platforms,
            'results': results
        }
    except Exception as e:
        logger.error(f"Error searching platforms: {e}")
        raise HTTPException(status_code=500, detail=f"Error searching: {str(e)}")

@ecommerce_router.get("/compare", response_model=ComparisonResponse)
async def compare_prices(
    query: str = Query(..., description="Product search query"),
    limit: int = Query(5, ge=1, le=25, description="Maximum number of results per platform")
):
    """
    Compare prices between Flipkart and Amazon
    
    Example: /api/ecommerce/compare?query=laptop&limit=5
    """
    try:
        logger.info(f"Comparing prices for: {query}")
        
        flipkart_products = flipkart.search_products(query, max_results=limit)
        amazon_products = amazon.search_products(query, max_results=limit)
        
        # Calculate average prices
        flipkart_prices = [p['price'] for p in flipkart_products if p['price'] > 0]
        amazon_prices = [p['price'] for p in amazon_products if p['price'] > 0]
        
        avg_flipkart = sum(flipkart_prices) / len(flipkart_prices) if flipkart_prices else 0
        avg_amazon = sum(amazon_prices) / len(amazon_prices) if amazon_prices else 0
        
        price_diff = avg_flipkart - avg_amazon
        
        return ComparisonResponse(
            query=query,
            flipkart_products=[ProductResponse(**p) for p in flipkart_products],
            amazon_products=[ProductResponse(**p) for p in amazon_products],
            average_flipkart_price=round(avg_flipkart, 2),
            average_amazon_price=round(avg_amazon, 2),
            price_difference=round(price_diff, 2)
        )
    except Exception as e:
        logger.error(f"Error comparing prices: {e}")
        raise HTTPException(status_code=500, detail=f"Error comparing prices: {str(e)}")

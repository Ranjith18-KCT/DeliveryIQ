from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class FlipkartScraper:
    def __init__(self):
        pass
    
    def search_products(self, query: str, max_results: int = 10) -> List[Dict]:
        logger.info(f"Searching Flipkart for: {query}")
        products = self._get_products(query, max_results)
        logger.info(f"✓ Returned {len(products)} products")
        return products
    
    def _get_products(self, query: str, max_results: int = 10) -> List[Dict]:
        mock_products = {
            'laptop': [
                {'name': 'Dell Inspiron 15 Laptop (2023)', 'price': 42899, 'rating': '4.4', 'reviews': '2,156', 'source': 'Flipkart', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.flipkart.com/search?q=laptop', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71pC63SXp3L.jpg'},
                {'name': 'HP 15s Core i5 8GB 512GB Laptop', 'price': 48999, 'rating': '4.3', 'reviews': '1,987', 'source': 'Flipkart', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.flipkart.com/search?q=laptop', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71vN80grpQL.jpg'},
                {'name': 'ASUS VivoBook 15 Core i7 Laptop', 'price': 62999, 'rating': '4.5', 'reviews': '2,345', 'source': 'Flipkart', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.flipkart.com/search?q=laptop', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71oYK3Y5ZwL.jpg'},
            ],
            'phone': [
                {'name': 'Samsung Galaxy A14 128GB', 'price': 10999, 'rating': '4.3', 'reviews': '6,123', 'source': 'Flipkart', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.flipkart.com/search?q=phone', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71SDHlVMCRL.jpg'},
                {'name': 'Redmi Note 12 128GB Storage', 'price': 16999, 'rating': '4.4', 'reviews': '5,234', 'source': 'Flipkart', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.flipkart.com/search?q=phone', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71f3A8pWj4L.jpg'},
                {'name': 'iPhone 13 128GB New', 'price': 59999, 'rating': '4.6', 'reviews': '7,123', 'source': 'Flipkart', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.flipkart.com/search?q=phone', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71qF2f2bJzL.jpg'},
            ],
            'watch': [
                {'name': 'Apple Watch Series 8 41mm', 'price': 41900, 'rating': '4.5', 'reviews': '2,654', 'source': 'Flipkart', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.flipkart.com/search?q=watch', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71CmkSc3X6L.jpg'},
                {'name': 'Samsung Galaxy Watch 5 40mm', 'price': 29999, 'rating': '4.3', 'reviews': '1,654', 'source': 'Flipkart', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.flipkart.com/search?q=watch', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71rVaZy3eXL.jpg'},
            ],
            'headphones': [
                {'name': 'Sony WH-CH720 Wireless Headphones', 'price': 6999, 'rating': '4.2', 'reviews': '1,876', 'source': 'Flipkart', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.flipkart.com/search?q=headphones', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71o8Q5XJS5L.jpg'},
                {'name': 'Apple AirPods Max Headphones', 'price': 54900, 'rating': '4.8', 'reviews': '3,234', 'source': 'Flipkart', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.flipkart.com/search?q=headphones', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71qnHM8ZCRL.jpg'},
            ],
        }
        query_lower = query.lower()
        for key in mock_products:
            if key in query_lower:
                return mock_products[key][:max_results]
        return [{'name': f'{query} - Best Deal 1', 'price': 8999, 'rating': '4.1', 'reviews': '120', 'source': 'Flipkart', 'category': 'General', 'availability': 'In Stock', 'link': f'https://www.flipkart.com/search?q={query}', 'image': 'https://images-eu.ssl-images-amazon.com/images/I/71pC63SXp3L.jpg'}][:max_results]

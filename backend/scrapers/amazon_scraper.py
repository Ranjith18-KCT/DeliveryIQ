from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class AmazonScraper:
    def __init__(self):
        pass
    
    def search_products(self, query: str, max_results: int = 10) -> List[Dict]:
        logger.info(f"Searching Amazon for: {query}")
        products = self._get_products(query, max_results)
        logger.info(f"✓ Returned {len(products)} products")
        return products
    
    def _get_products(self, query: str, max_results: int = 10) -> List[Dict]:
        mock_products = {
            'laptop': [
                {'name': 'Dell Inspiron 15 Laptop', 'price': 45999, 'rating': '4.3', 'reviews': '1,234', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=laptop', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71vN80grpQL.jpg'},
                {'name': 'HP Pavilion 15 Ryzen 5 Laptop', 'price': 52999, 'rating': '4.5', 'reviews': '2,156', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=laptop', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71pC63SXp3L.jpg'},
                {'name': 'ASUS VivoBook 15 OLED Laptop', 'price': 64999, 'rating': '4.6', 'reviews': '1,876', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=laptop', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71oYK3Y5ZwL.jpg'},
                {'name': 'Lenovo IdeaPad 5 15.6 Inch Laptop', 'price': 55999, 'rating': '4.4', 'reviews': '1,543', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=laptop', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71jXpEOzjwL.jpg'},
                {'name': 'Apple MacBook Air M2 13-inch', 'price': 119999, 'rating': '4.8', 'reviews': '3,456', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=laptop', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71jXpEOzjwL.jpg'},
            ],
            'phone': [
                {'name': 'Samsung Galaxy A14 5G Smartphone', 'price': 12999, 'rating': '4.2', 'reviews': '5,234', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=phone', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71SDHlVMCRL.jpg'},
                {'name': 'Redmi Note 12 Pro 5G Smartphone', 'price': 18999, 'rating': '4.4', 'reviews': '4,876', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=phone', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71f3A8pWj4L.jpg'},
                {'name': 'iPhone 14 128GB', 'price': 74999, 'rating': '4.7', 'reviews': '6,543', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=phone', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71qF2f2bJzL.jpg'},
                {'name': 'OnePlus 11 5G Smartphone', 'price': 39999, 'rating': '4.5', 'reviews': '3,123', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=phone', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71wdMrYojRL.jpg'},
            ],
            'watch': [
                {'name': 'Apple Watch Series 8 45mm', 'price': 45900, 'rating': '4.6', 'reviews': '2,345', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=watch', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71CmkSc3X6L.jpg'},
                {'name': 'Samsung Galaxy Watch 5 Pro', 'price': 32999, 'rating': '4.4', 'reviews': '1,876', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=watch', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71rVaZy3eXL.jpg'},
            ],
            'headphones': [
                {'name': 'Sony WH-1000XM5 Wireless Headphones', 'price': 29990, 'rating': '4.6', 'reviews': '2,543', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=headphones', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71o8Q5XJS5L.jpg'},
                {'name': 'Apple AirPods Pro (2nd Generation)', 'price': 24900, 'rating': '4.8', 'reviews': '4,567', 'source': 'Amazon', 'category': 'Electronics', 'availability': 'In Stock', 'link': 'https://www.amazon.in/s?k=headphones', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71qnHM8ZCRL.jpg'},
            ],
        }
        query_lower = query.lower()
        for key in mock_products:
            if key in query_lower:
                return mock_products[key][:max_results]
        return [{'name': f'{query} - Option 1', 'price': 9999, 'rating': '4.0', 'reviews': '100', 'source': 'Amazon', 'category': 'General', 'availability': 'In Stock', 'link': f'https://www.amazon.in/s?k={query}', 'image': 'https://images-na.ssl-images-amazon.com/images/I/71pC63SXp3L.jpg'}][:max_results]

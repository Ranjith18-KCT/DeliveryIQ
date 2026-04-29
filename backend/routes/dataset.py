"""
Dataset Management Routes:
- GET /api/dataset/info - Get dataset statistics
- GET /api/dataset/products - Get all products (with filters)
- GET /api/dataset/product/{product_id} - Get specific product
- GET /api/dataset/search - Search products by category/city
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)
dataset_router = APIRouter()

# Global dataset cache
dataset_df = None

def load_dataset():
    """Load final_dataset.csv into memory"""
    global dataset_df
    try:
        dataset_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'dataset',
            'final_dataset.csv'
        )
        
        if not os.path.exists(dataset_path):
            logger.warning(f"Dataset not found at {dataset_path}")
            return False
        
        dataset_df = pd.read_csv(dataset_path)
        logger.info(f"✓ Dataset loaded: {dataset_df.shape[0]} rows × {dataset_df.shape[1]} columns")
        return True
        
    except Exception as e:
        logger.error(f"✗ Error loading dataset: {e}")
        return False

# Load dataset on startup
@dataset_router.on_event("startup")
async def startup_dataset():
    """Load dataset when router is initialized"""
    load_dataset()

class DatasetInfo(BaseModel):
    total_rows: int
    total_columns: int
    columns: List[str]
    categories: List[str]
    cities: List[str]
    states: List[str]
    shape: tuple

@dataset_router.get("/dataset/info", response_model=DatasetInfo)
async def get_dataset_info():
    """Get dataset statistics and metadata"""
    if dataset_df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded")
    
    try:
        columns = dataset_df.columns.tolist()
        
        # Get unique values for categorical columns
        categories = []
        cities = []
        states = []
        
        if 'product_sub_category' in dataset_df.columns:
            categories = dataset_df['product_sub_category'].unique().tolist()[:20]
        if 'delivery_city' in dataset_df.columns:
            cities = dataset_df['delivery_city'].unique().tolist()[:20]
        if 'delivery_state' in dataset_df.columns:
            states = dataset_df['delivery_state'].unique().tolist()[:10]
        
        return DatasetInfo(
            total_rows=len(dataset_df),
            total_columns=len(dataset_df.columns),
            columns=columns,
            categories=categories if categories else ["Electronics", "Furniture", "Clothing"],
            cities=cities if cities else ["Mumbai", "Delhi", "Bangalore"],
            states=states if states else ["Maharashtra", "Delhi", "Karnataka"],
            shape=(len(dataset_df), len(dataset_df.columns))
        )
        
    except Exception as e:
        logger.error(f"Error getting dataset info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@dataset_router.get("/dataset/products")
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    city: Optional[str] = None
):
    """
    Get products from dataset with pagination and filtering
    
    - skip: Number of records to skip (default: 0)
    - limit: Number of records to return (max 100)
    - category: Filter by product category
    - city: Filter by delivery city
    """
    if dataset_df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded")
    
    try:
        filtered_df = dataset_df.copy()
        
        # Apply filters
        if category and 'product_sub_category' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['product_sub_category'] == category]
        
        if city and 'delivery_city' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['delivery_city'] == city]
        
        # Pagination
        total = len(filtered_df)
        products = filtered_df.iloc[skip:skip+limit].to_dict('records')
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "count": len(products),
            "products": products
        }
        
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@dataset_router.get("/dataset/product/{product_id}")
async def get_product(product_id: str):
    """Get specific product by ID"""
    if dataset_df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded")
    
    try:
        # Try different ID column names
        id_columns = ['product_id', 'Product_ID', 'ID', 'id']
        product = None
        
        for col in id_columns:
            if col in dataset_df.columns:
                result = dataset_df[dataset_df[col] == product_id]
                if not result.empty:
                    product = result.iloc[0].to_dict()
                    break
        
        if product is None:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@dataset_router.get("/dataset/search")
async def search_dataset(
    q: str = Query(..., min_length=1),
    field: Optional[str] = None,
    limit: int = Query(10, ge=1, le=50)
):
    """
    Search dataset by keyword
    
    - q: Search query
    - field: Specific field to search in (optional)
    - limit: Maximum results (default: 10, max: 50)
    """
    if dataset_df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded")
    
    try:
        search_term = str(q).lower()
        
        if field and field in dataset_df.columns:
            # Search specific field
            mask = dataset_df[field].astype(str).str.lower().str.contains(search_term)
        else:
            # Search all columns
            mask = dataset_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)
            ).any(axis=1)
        
        results = dataset_df[mask].head(limit).to_dict('records')
        
        return {
            "query": q,
            "field": field,
            "count": len(results),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error searching dataset: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@dataset_router.get("/dataset/stats")
async def get_dataset_stats():
    """Get statistical summary of dataset"""
    if dataset_df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded")
    
    try:
        stats = {
            "total_products": len(dataset_df),
            "total_features": len(dataset_df.columns),
            "missing_values": dataset_df.isnull().sum().to_dict(),
            "numeric_columns": dataset_df.select_dtypes(include=['number']).columns.tolist(),
            "categorical_columns": dataset_df.select_dtypes(include=['object']).columns.tolist(),
        }
        
        # Add numeric statistics
        numeric_stats = {}
        for col in dataset_df.select_dtypes(include=['number']).columns:
            numeric_stats[col] = {
                "mean": float(dataset_df[col].mean()),
                "std": float(dataset_df[col].std()),
                "min": float(dataset_df[col].min()),
                "max": float(dataset_df[col].max())
            }
        
        stats["numeric_statistics"] = numeric_stats
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting dataset stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

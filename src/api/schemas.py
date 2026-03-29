from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class ProductInput(BaseModel):
    """Input schema for single product"""
    product_name: str = Field(..., min_length=3, max_length=200, description="Product name")
    category: str = Field(..., min_length=2, max_length=100, description="Product category")
    description: str = Field(..., min_length=20, max_length=1000, description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    
    @validator('price')
    def validate_price(cls, v):
        if v > 1000000:
            raise ValueError('Price too high')
        return round(v, 2)
    
    class Config:
        schema_extra = {
            "example": {
                "product_name": "Wireless Bluetooth Headphones",
                "category": "Electronics",
                "description": "Premium noise-cancelling headphones with 30-hour battery life and superior sound quality",
                "price": 79.99
            }
        }

class BatchProductInput(BaseModel):
    """Input schema for batch prediction"""
    products: List[ProductInput] = Field(..., min_items=1, max_items=50)
    
    class Config:
        schema_extra = {
            "example": {
                "products": [
                    {
                        "product_name": "Wireless Bluetooth Headphones",
                        "category": "Electronics",
                        "description": "Premium noise-cancelling headphones",
                        "price": 79.99
                    },
                    {
                        "product_name": "Organic Cotton T-Shirt",
                        "category": "Clothing",
                        "description": "Comfortable 100% organic cotton t-shirt",
                        "price": 24.99
                    }
                ]
            }
        }

class AdCreativeOutput(BaseModel):
    """Output schema for generated ad"""
    product_name: str
    generated_ad: str
    category: str
    price: float
    generation_time_ms: float
    model_version: str = "1.0"
    timestamp: str

class BatchAdCreativeOutput(BaseModel):
    """Output schema for batch predictions"""
    results: List[AdCreativeOutput]
    total_products: int
    total_time_ms: float
    successful: int
    failed: int

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_name: str
    device: str
    timestamp: str
    uptime_seconds: float

class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: Optional[str] = None
    timestamp: str
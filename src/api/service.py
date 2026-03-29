import torch
from pathlib import Path
import time
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger
from utils.config_loader import load_config

logger = get_logger(__name__)

class AdGenerationService:
    """Service for ad generation with caching and monitoring"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        logger.info("Initializing Ad Generation Service...")
        
        try:
            self.config = load_config()
        except Exception as e:
            logger.warning(f"Could not load config: {e}")
            self.config = {'model': {'name': 't5-base'}}
        
        model_path = "models/checkpoints/final_model"
        
        # Check if model exists and has files
        model_exists = Path(model_path).exists() and any(Path(model_path).iterdir())
        
        if not model_exists:
            logger.warning(f"Model not found at {model_path}")
            logger.warning("Service will run in mock mode for health checks")
            self.generator = None
            self.model_name = "mock-model"
            self.device = "cpu"
            self.model_loaded = False
        else:
            try:
                from model.inference import AdCreativeGenerator
                self.generator = AdCreativeGenerator(model_path)
                self.model_name = self.config['model'].get('name', 't5-base')
                self.device = str(self.generator.device)
                self.model_loaded = True
                logger.info(f"✅ Model loaded: {self.model_name}")
                logger.info(f"✅ Device: {self.device}")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                logger.info("✅ Falling back to MOCK MODE")
                self.generator = None
                self.model_name = "mock-model"
                self.device = "cpu"
                self.model_loaded = False
        
        self.start_time = time.time()
        self.request_count = 0
        self.total_generation_time = 0.0
        
        self._initialized = True
        logger.info("✅ Service initialized successfully")
    
    def generate_ad(self, product_name: str, category: str, 
                   description: str, price: float) -> dict:
        """Generate single ad creative"""
        start_time = time.time()
        
        try:
            if self.generator is None:
                # Mock response for testing without model
                ad_text = f"🌟 {product_name} 🌟\n\n{description}\n\n💰 Only ${price:.2f}! Shop now!"
            else:
                ads = self.generator.generate(
                    product_name=product_name,
                    category=category,
                    description=description,
                    price=price,
                    num_variants=1
                )
                ad_text = ads[0]
            
            generation_time = (time.time() - start_time) * 1000
            
            self.request_count += 1
            self.total_generation_time += generation_time
            
            return {
                "product_name": product_name,
                "generated_ad": ad_text,
                "category": category,
                "price": price,
                "generation_time_ms": round(generation_time, 2),
                "model_version": "1.0"
            }
        
        except Exception as e: 
            logger.error(f"Generation failed: {str(e)}")
            raise
    
    def generate_batch(self, products: list) -> dict:
        """Generate ads for multiple products"""
        start_time = time.time()
        results = []
        successful = 0
        failed = 0
        
        for product in products:
            try:
                result = self.generate_ad(
                    product['product_name'],
                    product['category'],
                    product['description'],
                    product['price']
                )
                results.append(result)
                successful += 1
            except Exception as e:
                logger.error(f"Failed to generate ad for {product.get('product_name', 'unknown')}: {str(e)}")
                failed += 1
        
        total_time = (time.time() - start_time) * 1000
        
        return {
            "results": results,
            "total_products": len(products),
            "total_time_ms": round(total_time, 2),
            "successful": successful,
            "failed": failed
        }
    
    def get_health(self) -> dict:
        """Get service health status"""
        uptime = time.time() - self.start_time
        return {
            "status": "healthy" if self.model_loaded else "degraded",
            "model_loaded": self.model_loaded,
            "model_name": self.model_name,
            "device": self.device,
            "uptime_seconds": round(uptime, 2)
        }
    
    def get_stats(self) -> dict:
        """Get service statistics"""
        avg_time = (self.total_generation_time / self.request_count 
                   if self.request_count > 0 else 0)
        return {
            "total_requests": self.request_count,
            "average_generation_time_ms": round(avg_time, 2),
            "total_generation_time_ms": round(self.total_generation_time, 2),
            "uptime_seconds": round(time.time() - self.start_time, 2)
        }
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import sys
from pathlib import Path
import time as time_module
import asyncio

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Prometheus imports
from prometheus_client import make_asgi_app, REGISTRY
from src.api.metrics import (
    track_request, track_generation, track_error, 
    set_model_info, active_requests, service_uptime,
    request_duration, track_drift
)
from src.api.schemas import (
    ProductInput, BatchProductInput, AdCreativeOutput,
    BatchAdCreativeOutput, HealthResponse, ErrorResponse
)
from src.api.service import AdGenerationService
from src.utils.logger import get_logger
from src.monitoring.drift_detector import drift_detector

logger = get_logger(__name__)

app = FastAPI(
    title="E-Commerce Ad Creative Generator API",
    description="Generate marketing ad creatives for e-commerce products using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instance
service = None
service_start_time = None

# Background task to update uptime
async def update_uptime_task():
    """Background task to update service uptime metric"""
    while True:
        try:
            if service_start_time is not None:
                uptime = time_module.time() - service_start_time
                service_uptime.set(uptime)
            await asyncio.sleep(10)
        except Exception as e:
            logger.error(f"Error updating uptime: {e}")
            await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    global service, service_start_time
    
    logger.info("="*70)
    logger.info("🚀 Starting E-Commerce Ad Generator API")
    logger.info("="*70)
    
    try:
        service = AdGenerationService()
        service_start_time = time_module.time()
        
        # Set model info for Prometheus
        set_model_info(
            name=service.model_name,
            device=service.device,
            version="1.0"
        )
        
        # Start background tasks
        asyncio.create_task(update_uptime_task())
        
        if service.model_loaded:
            logger.info("✅ Service initialized with model loaded")
        else:
            logger.warning("⚠️ Service initialized in MOCK mode (no model)")
    except Exception as e:
        logger.error(f"❌ Failed to load service: {e}")
        service = None

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down API server...")

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "E-Commerce Ad Creative Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }

@app.get("/metrics", tags=["Metrics"])
async def metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response
    
    return Response(
        content=generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/drift/report", tags=["Monitoring"])
async def drift_report():
    """Get drift detection report"""
    try:
        report = drift_detector.get_drift_report()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=report
        )
    except Exception as e:
        logger.error(f"Error getting drift report: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    start_time = time_module.time()
    
    try:
        if service is None:
            track_request("health", "error")
            track_error("service_not_initialized")
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": "unavailable",
                    "model_loaded": False,
                    "detail": "Service not initialized",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        health_data = service.get_health()
        health_data["timestamp"] = datetime.now().isoformat()
        
        # Track metrics
        track_request("health", "success")
        request_duration.labels(endpoint="health").observe(time_module.time() - start_time)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=health_data
        )
    
    except Exception as e:
        track_error("health_check_exception")
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "detail": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/stats", tags=["Monitoring"])
async def get_statistics():
    """Get API statistics"""
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not initialized"
        )
    
    return service.get_stats()

@app.post("/generate", response_model=AdCreativeOutput, tags=["Generation"])
async def generate_ad(product: ProductInput):
    """Generate ad creative for a single product"""
    start_time = time_module.time()
    
    # Track active requests
    active_requests.inc()
    
    try:
        if service is None:
            track_request("generate", "error")
            track_error("service_not_initialized")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service not initialized"
            )
        
        logger.info(f"Generating ad for: {product.product_name}")
        
        # Drift detection on incoming data
        try:
            drift_result = drift_detector.detect_drift([product.dict()])
            track_drift(drift_result)  # Track drift metrics
            if drift_result.get('drift_detected'):
                logger.warning(f"⚠️ Data drift detected: {drift_result.get('alert_level')}")
        except Exception as drift_e:
            logger.error(f"Drift detection failed: {drift_e}")
        
        # Generate ad
        result = service.generate_ad(
            product_name=product.product_name,
            category=product.category,
            description=product.description,
            price=product.price
        )
        
        result["timestamp"] = datetime.now().isoformat()
        
        # Track metrics
        generation_duration = time_module.time() - start_time
        track_generation(
            category=product.category,
            text=result["generated_ad"],
            duration=generation_duration,
            price=product.price
        )
        track_request("generate", "success")
        request_duration.labels(endpoint="generate").observe(generation_duration)
        
        logger.info(f"✅ Ad generated successfully")
        return result
    
    except HTTPException:
        raise
    
    except Exception as e:
        track_request("generate", "error")
        track_error(type(e).__name__)
        logger.error(f"❌ Generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {str(e)}"
        )
    
    finally:
        active_requests.dec()

@app.post("/generate/batch", response_model=BatchAdCreativeOutput, tags=["Generation"])
async def generate_batch(batch: BatchProductInput):
    """Generate ad creatives for multiple products"""
    start_time = time_module.time()
    
    # Track active requests
    active_requests.inc()
    
    try:
        if service is None:
            track_request("batch", "error")
            track_error("service_not_initialized")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service not initialized"
            )
        
        logger.info(f"Batch generation for {len(batch.products)} products")
        
        products_list = [p.dict() for p in batch.products]
        result = service.generate_batch(products_list)
        
        for r in result["results"]:
            r["timestamp"] = datetime.now().isoformat()
        
        # Track metrics for each successful generation
        for product, res in zip(batch.products, result["results"]):
            if res.get("generated_ad"):
                track_generation(
                    category=product.category,
                    text=res["generated_ad"],
                    duration=res.get("generation_time_ms", 0) / 1000.0,
                    price=product.price
                )
        
        track_request("batch", "success")
        request_duration.labels(endpoint="batch").observe(time_module.time() - start_time)
        
        logger.info(f"✅ Batch generation completed: {result['successful']}/{result['total_products']}")
        return result
    
    except HTTPException:
        raise
    
    except Exception as e:
        track_request("batch", "error")
        track_error(type(e).__name__)
        logger.error(f"❌ Batch generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch generation failed: {str(e)}"
        )
    
    finally:
        active_requests.dec()

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    track_error("unhandled_exception")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
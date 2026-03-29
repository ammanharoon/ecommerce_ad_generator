"""
Prometheus metrics for ML model monitoring
"""
from prometheus_client import Counter, Histogram, Gauge, Info
import time

# ============================================================================
# Request Metrics
# ============================================================================

request_count = Counter(
    'ad_generator_requests_total',
    'Total number of ad generation requests',
    ['endpoint', 'status']
)

request_duration = Histogram(
    'ad_generator_request_duration_seconds',
    'Request duration in seconds',
    ['endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

# ============================================================================
# Model Performance Metrics
# ============================================================================

generation_time = Histogram(
    'ad_generator_generation_time_seconds',
    'Time taken to generate ad text',
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0]
)

model_latency = Histogram(
    'ad_generator_model_latency_seconds',
    'Model inference latency',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# ============================================================================
# Throughput Metrics
# ============================================================================

ads_generated_total = Counter(
    'ad_generator_ads_generated_total',
    'Total number of ads generated',
    ['category']
)

# ============================================================================
# Quality Metrics
# ============================================================================

ad_length = Histogram(
    'ad_generator_ad_length_characters',
    'Length of generated ad in characters',
    buckets=[50, 100, 200, 300, 500, 1000]
)

ad_word_count = Histogram(
    'ad_generator_ad_word_count',
    'Word count of generated ads',
    buckets=[10, 20, 30, 50, 75, 100, 150]
)

# ============================================================================
# System Metrics
# ============================================================================

model_info = Info(
    'ad_generator_model',
    'Information about the ML model'
)

active_requests = Gauge(
    'ad_generator_active_requests',
    'Number of requests currently being processed'
)

service_uptime = Gauge(
    'ad_generator_uptime_seconds',
    'Service uptime in seconds'
)

# ============================================================================
# Error Metrics
# ============================================================================

errors_total = Counter(
    'ad_generator_errors_total',
    'Total number of errors',
    ['error_type']
)

# ============================================================================
# Drift Detection Metrics (BONUS FEATURE)
# ============================================================================

drift_detections_total = Counter(
    'ad_generator_drift_detections_total',
    'Total number of drift detections',
    ['severity', 'test_type']
)

drift_checks_total = Counter(
    'ad_generator_drift_checks_total',
    'Total number of drift checks performed'
)

drift_p_value = Histogram(
    'ad_generator_drift_p_value',
    'P-values from drift detection tests',
    ['test_type'],
    buckets=[0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
)

# ============================================================================
# Price Metrics (Business)
# ============================================================================

product_price = Histogram(
    'ad_generator_product_price',
    'Distribution of product prices',
    ['category'],
    buckets=[10, 25, 50, 100, 200, 500, 1000]
)

# ============================================================================
# Helper Functions
# ============================================================================

def track_request(endpoint, status):
    """Track request count by endpoint and status"""
    request_count.labels(endpoint=endpoint, status=status).inc()

def track_generation(category, text, duration, price):
    """Track ad generation metrics"""
    ads_generated_total.labels(category=category).inc()
    generation_time.observe(duration)
    ad_length.observe(len(text))
    ad_word_count.observe(len(text.split()))
    product_price.labels(category=category).observe(price)

def track_error(error_type):
    """Track errors by type"""
    errors_total.labels(error_type=error_type).inc()

def set_model_info(name, device, version):
    """Set model information"""
    model_info.info({
        'name': name,
        'device': device,
        'version': version
    })

def track_drift(drift_result):
    """Track drift detection metrics"""
    drift_checks_total.inc()
    
    if drift_result.get('drift_detected'):
        # Track by severity and test type
        for test_name, test_data in drift_result.get('tests', {}).items():
            if test_data.get('drift_detected'):
                severity = test_data.get('severity', 'unknown')
                drift_detections_total.labels(
                    severity=severity,
                    test_type=test_name
                ).inc()
            
            # Track p-values if available
            if 'p_value' in test_data:
                drift_p_value.labels(test_type=test_name).observe(test_data['p_value'])
import requests
import json
import time

API_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*70)
    print("TEST 1: Health Check")
    print("="*70)
    
    response = requests.get(f"{API_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ Health check passed")

def test_single_generation():
    """Test single ad generation"""
    print("\n" + "="*70)
    print("TEST 2: Single Ad Generation")
    print("="*70)
    
    payload = {
        "product_name": "Wireless Bluetooth Headphones",
        "category": "Electronics",
        "description": "Premium noise-cancelling headphones with 30-hour battery life",
        "price": 79.99
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    
    start = time.time()
    response = requests.post(f"{API_URL}/generate", json=payload)
    elapsed = time.time() - start
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {elapsed:.2f}s")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert "generated_ad" in response.json()
    print("✅ Single generation passed")

def test_batch_generation():
    """Test batch ad generation"""
    print("\n" + "="*70)
    print("TEST 3: Batch Ad Generation")
    print("="*70)
    
    payload = {
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
            },
            {
                "product_name": "Yoga Mat",
                "category": "Sports",
                "description": "Non-slip exercise mat for yoga and pilates",
                "price": 34.99
            }
        ]
    }
    
    print(f"Request: {len(payload['products'])} products")
    
    start = time.time()
    response = requests.post(f"{API_URL}/generate/batch", json=payload)
    elapsed = time.time() - start
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {elapsed:.2f}s")
    print(f"Response Summary:")
    result = response.json()
    print(f"  Total Products: {result['total_products']}")
    print(f"  Successful: {result['successful']}")
    print(f"  Failed: {result['failed']}")
    print(f"  Total Time: {result['total_time_ms']}ms")
    
    assert response.status_code == 200
    assert result['successful'] == 3
    print("✅ Batch generation passed")

def test_stats():
    """Test statistics endpoint"""
    print("\n" + "="*70)
    print("TEST 4: Statistics")
    print("="*70)
    
    response = requests.get(f"{API_URL}/stats")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ Statistics check passed")

def test_validation():
    """Test input validation"""
    print("\n" + "="*70)
    print("TEST 5: Input Validation (Error Handling)")
    print("="*70)
    
    invalid_payload = {
        "product_name": "AB",
        "category": "Electronics",
        "description": "Too short",
        "price": -10
    }
    
    response = requests.post(f"{API_URL}/generate", json=invalid_payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 422
    print("✅ Validation test passed")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 TESTING E-COMMERCE AD GENERATOR API")
    print("="*70)
    
    try:
        test_health()
        test_single_generation()
        test_batch_generation()
        test_stats()
        test_validation()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70 + "\n")
    
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}\n")
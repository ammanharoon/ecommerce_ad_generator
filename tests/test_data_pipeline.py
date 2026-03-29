import pytest
import pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from data_pipeline.validator import DataValidator
from data_pipeline.preprocessor import DataPreprocessor

def test_validator():
    """Test data validator"""
    validator = DataValidator()
    test_data = pd.DataFrame({
        'product_id': [1, 2, 3],
        'product_name': ['Test Product 1', 'Test Product 2', 'Test Product 3'],
        'category': ['Electronics', 'Clothing', 'Sports'],
        'description': ['This is a test product description', 'Another test description here', 'Third test product description'],
        'price': [29.99, 49.99, 19.99]
    })
    result = validator.validate(test_data)
    assert result['passed'] == True
    assert result['total_records'] == 3
    print("✅ Validator test passed")

def test_preprocessor():
    """Test data preprocessor"""
    preprocessor = DataPreprocessor()
    test_text = "  This   is    a  test   "
    cleaned = preprocessor.clean_text(test_text)
    assert cleaned == "This is a test"
    print("✅ Preprocessor test passed")

if __name__ == "__main__":
    test_validator()
    test_preprocessor()
    print("✅ All tests passed!")
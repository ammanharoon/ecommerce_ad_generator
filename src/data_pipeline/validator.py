import pandas as pd
from typing import Dict, List, Tuple
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger

logger = get_logger(__name__)

class DataValidator:
    """Validate product data quality"""
    def __init__(self):
        self.required_columns = ['product_id', 'product_name', 'category', 'description', 'price']
        self.valid_categories = [
            "Electronics", "Clothing", "Home & Kitchen", "Sports",
            "Accessories", "Food & Beverage", "Beauty", "Books",
            "Toys", "Automotive"
        ]
    def validate_schema(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Check if required columns exist"""
        errors = []
        missing_cols = set(self.required_columns) - set(df.columns)
        if missing_cols:
            errors.append(f"Missing columns: {missing_cols}")
        return len(errors) == 0, errors
    def validate_data_types(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate data types"""
        errors = []
        if not pd.api.types.is_numeric_dtype(df['product_id']):
            errors.append("product_id must be numeric")
        if not pd.api.types.is_numeric_dtype(df['price']):
            errors.append("price must be numeric")
        return len(errors) == 0, errors
    def validate_values(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate data values"""
        errors = []
        if df['product_id'].duplicated().any():
            errors.append(f"Duplicate product_ids found: {df['product_id'].duplicated().sum()}")
        if df['product_name'].isnull().any():
            errors.append(f"Null product names: {df['product_name'].isnull().sum()}")
        if df['description'].isnull().any():
            errors.append(f"Null descriptions: {df['description'].isnull().sum()}")
        if (df['price'] <= 0).any():
            errors.append(f"Invalid prices (<=0): {(df['price'] <= 0).sum()}")
        invalid_categories = ~df['category'].isin(self.valid_categories)
        if invalid_categories.any():
            errors.append(f"Invalid categories: {df[invalid_categories]['category'].unique()}")
        if (df['description'].str.len() < 20).any():
            errors.append(f"Descriptions too short (<20 chars): {(df['description'].str.len() < 20).sum()}")
        return len(errors) == 0, errors
    def validate(self, df: pd.DataFrame) -> Dict:
        """Run all validations"""
        logger.info("Starting data validation...")
        results = {
            'total_records': len(df),
            'passed': True,
            'errors': []
        }
        schema_valid, schema_errors = self.validate_schema(df)
        if not schema_valid:
            results['passed'] = False
            results['errors'].extend(schema_errors)
            return results
        dtype_valid, dtype_errors = self.validate_data_types(df)
        if not dtype_valid:
            results['passed'] = False
            results['errors'].extend(dtype_errors)
        value_valid, value_errors = self.validate_values(df)
        if not value_valid:
            results['passed'] = False
            results['errors'].extend(value_errors)
        if results['passed']:
            logger.info(f"✅ Validation passed for {results['total_records']} records")
        else:
            logger.error(f"❌ Validation failed with {len(results['errors'])} errors")
            for error in results['errors']:
                logger.error(f"  - {error}")
        return results
import pandas as pd
import re
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger

logger = get_logger(__name__)

class DataPreprocessor:
    """Preprocess and clean product data"""
    def __init__(self):
        self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'])
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if pd.isna(text):
            return ""
        text = str(text).strip()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\-\.,!?]', '', text)
        return text
    def create_ad_template(self, row: pd.Series) -> str:
        """Create structured template for ad generation"""
        template = f"Product: {row['product_name']}\n"
        template += f"Category: {row['category']}\n"
        template += f"Description: {row['description']}\n"
        template += f"Price: ${row['price']:.2f}"
        return template
    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract additional features for training"""
        logger.info("Extracting features...")
        df['product_name_clean'] = df['product_name'].apply(self.clean_text)
        df['description_clean'] = df['description'].apply(self.clean_text)
        df['description_length'] = df['description_clean'].str.len()
        df['word_count'] = df['description_clean'].str.split().str.len()
        df['price_category'] = pd.cut(
            df['price'],
            bins=[0, 25, 50, 100, 500, float('inf')],
            labels=['budget', 'affordable', 'moderate', 'premium', 'luxury']
        )
        df['ad_input_template'] = df.apply(self.create_ad_template, axis=1)
        logger.info(f"✅ Feature extraction complete. Total features: {len(df.columns)}")
        return df
    def preprocess(self, input_path: str, output_path: str) -> pd.DataFrame:
        """Main preprocessing pipeline"""
        logger.info(f"Loading data from: {input_path}")
        df = pd.read_csv(input_path)
        logger.info(f"Loaded {len(df)} records")
        df = df.drop_duplicates(subset=['product_id'])
        df = df.dropna(subset=['product_name', 'description'])
        df = self.extract_features(df)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"✅ Preprocessed data saved to: {output_path}")
        return df
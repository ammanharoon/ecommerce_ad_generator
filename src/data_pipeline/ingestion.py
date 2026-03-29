import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger
from utils.config_loader import get_data_config
from data_pipeline.validator import DataValidator
from data_pipeline.preprocessor import DataPreprocessor

logger = get_logger(__name__)

class DataIngestionPipeline:
    """Complete data ingestion pipeline"""
    def __init__(self):
        self.config = get_data_config()
        self.validator = DataValidator()
        self.preprocessor = DataPreprocessor()
    def ingest_from_csv(self, csv_path: str) -> pd.DataFrame:
        """Ingest data from CSV file"""
        logger.info(f"Ingesting data from CSV: {csv_path}")
        df = pd.read_csv(csv_path)
        logger.info(f"✅ Loaded {len(df)} records from CSV")
        return df
    def run_pipeline(self, input_path: str = None, output_path: str = None) -> bool:
        """Execute complete ingestion pipeline"""
        try:
            if input_path is None:
                input_path = self.config.get('raw_data_path', 'data/raw/products.csv')
            if output_path is None:
                output_path = self.config.get('processed_data_path', 'data/processed/products_processed.csv')
            logger.info("="*50)
            logger.info("Starting Data Ingestion Pipeline")
            logger.info("="*50)
            df = self.ingest_from_csv(input_path)
            validation_result = self.validator.validate(df)
            if not validation_result['passed']:
                logger.error("❌ Data validation failed!")
                return False
            df_processed = self.preprocessor.preprocess(input_path, output_path)
            logger.info("="*50)
            logger.info("✅ Data Ingestion Pipeline Completed Successfully")
            logger.info(f"Total records processed: {len(df_processed)}")
            logger.info(f"Output saved to: {output_path}")
            logger.info("="*50)
            return True
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {str(e)}")
            return False

if __name__ == "__main__":
    pipeline = DataIngestionPipeline()
    success = pipeline.run_pipeline()
    sys.exit(0 if success else 1)
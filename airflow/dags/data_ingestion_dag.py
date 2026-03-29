from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.data_pipeline.ingestion import DataIngestionPipeline
from src.utils.logger import get_logger

logger = get_logger(__name__)

default_args = {
    'owner': 'amman',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_ingestion_pipeline',
    default_args=default_args,
    description='Ingest and preprocess product data for ad generation',
    schedule_interval='0 2 * * *',
    catchup=False,
    tags=['data', 'ingestion', 'preprocessing'],
)

def run_ingestion_task():
    """Task to run data ingestion"""
    logger.info("Starting Airflow data ingestion task")
    pipeline = DataIngestionPipeline()
    success = pipeline.run_pipeline()
    if not success:
        raise Exception("Data ingestion pipeline failed")
    logger.info("✅ Airflow task completed successfully")

def validate_output_task():
    """Task to validate processed data exists"""
    import pandas as pd
    output_path = "data/processed/products_processed.csv"
    if not Path(output_path).exists():
        raise FileNotFoundError(f"Processed data not found: {output_path}")
    df = pd.read_csv(output_path)
    logger.info(f"✅ Validation passed: {len(df)} records found")
    if len(df) < 10:
        raise ValueError(f"Insufficient data: only {len(df)} records")

def generate_summary_task():
    """Task to generate data summary"""
    import pandas as pd
    df = pd.read_csv("data/processed/products_processed.csv")
    summary = {
        'total_products': len(df),
        'categories': df['category'].nunique(),
        'avg_price': df['price'].mean(),
        'price_range': f"${df['price'].min():.2f} - ${df['price'].max():.2f}"
    }
    logger.info("="*50)
    logger.info("DATA SUMMARY")
    logger.info("="*50)
    for key, value in summary.items():
        logger.info(f"{key}: {value}")
    logger.info("="*50)

t1_ingest = PythonOperator(
    task_id='ingest_and_preprocess_data',
    python_callable=run_ingestion_task,
    dag=dag,
)

t2_validate = PythonOperator(
    task_id='validate_processed_data',
    python_callable=validate_output_task,
    dag=dag,
)

t3_summary = PythonOperator(
    task_id='generate_data_summary',
    python_callable=generate_summary_task,
    dag=dag,
)

t1_ingest >> t2_validate >> t3_summary
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
from pathlib import Path

default_args = {
    'owner': 'amman',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}

dag = DAG(
    'model_training_pipeline',
    default_args=default_args,
    description='Train and evaluate ad creative generation model',
    schedule_interval='0 3 * * 0',
    catchup=False,
    tags=['model', 'training', 'mlflow'],
)

def check_data_task():
    """Check if processed data exists"""
    data_path = Path("data/processed/products_processed.csv")
    if not data_path.exists():
        raise FileNotFoundError(f"Processed data not found: {data_path}")
    import pandas as pd
    df = pd.read_csv(data_path)
    if len(df) < 100:
        raise ValueError(f"Insufficient data for training: {len(df)} samples")
    print(f"✅ Data check passed: {len(df)} samples available")

def train_model_task():
    """Train the model"""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from src.model.train import main
    main()

def evaluate_model_task():
    """Evaluate trained model"""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from src.model.evaluate import evaluate_model
    evaluate_model(
        "models/checkpoints/final_model",
        "data/processed/val.csv",
        num_samples=5
    )

t1_check = PythonOperator(
    task_id='check_data_availability',
    python_callable=check_data_task,
    dag=dag,
)

t2_train = PythonOperator(
    task_id='train_model',
    python_callable=train_model_task,
    dag=dag,
)

t3_evaluate = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model_task,
    dag=dag,
)

t1_check >> t2_train >> t3_evaluate
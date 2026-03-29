import yaml
from pathlib import Path
from typing import Dict, Any

def load_config(config_path:  str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file"""
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found:  {config_path}")
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

def get_data_config() -> Dict[str, Any]: 
    """Get data-specific configuration"""
    config = load_config()
    return config.get('data', {})

def get_model_config() -> Dict[str, Any]:
    """Get model-specific configuration"""
    config = load_config()
    return config.get('model', {})

def get_airflow_config() -> Dict[str, Any]:
    """Get Airflow-specific configuration"""
    config = load_config()
    return config.get('airflow', {})
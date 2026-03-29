import mlflow
import torch
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger
from utils.config_loader import load_config
from model.config import ModelConfig
from model.dataset import prepare_datasets
from model.trainer import AdCreativeTrainer
from transformers import AutoTokenizer

logger = get_logger(__name__)

def main():
    """Main training function"""
    logger.info("="*70)
    logger.info("E-COMMERCE AD CREATIVE GENERATOR - MODEL TRAINING")
    logger.info("="*70)
    config_dict = load_config()
    model_config = ModelConfig()
    mlflow_config = config_dict.get('mlflow', {})
    mlflow.set_tracking_uri(mlflow_config.get('tracking_uri', 'http://localhost:5000'))
    mlflow.set_experiment(mlflow_config.get('experiment_name', 'ad-creative-generation'))
    logger.info(f"MLflow tracking URI: {mlflow.get_tracking_uri()}")
    logger.info(f"Experiment: {mlflow_config.get('experiment_name')}")
    with mlflow.start_run(run_name="t5-small-finetuning"):
        mlflow.log_params({
            "model_name": model_config.model_name,
            "max_input_length": model_config.max_input_length,
            "max_target_length": model_config.max_target_length,
            "train_batch_size": model_config.train_batch_size,
            "learning_rate": model_config.learning_rate,
            "num_epochs": model_config.num_epochs,
            "warmup_steps": model_config.warmup_steps,
            "weight_decay": model_config.weight_decay,
            "device": model_config.device,
            "gradient_accumulation_steps": model_config.gradient_accumulation_steps,
        })
        logger.info("\n📦 Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_config.model_name)
        logger.info("✅ Tokenizer loaded")
        logger.info("\n📊 Preparing datasets...")
        data_path = config_dict['data']['processed_data_path']
        train_dataset, val_dataset = prepare_datasets(
            data_path,
            tokenizer,
            train_split=0.8,
            max_input_length=model_config.max_input_length,
            max_target_length=model_config.max_target_length
        )
        logger.info(f"✅ Train dataset size: {len(train_dataset)}")
        logger.info(f"✅ Val dataset size: {len(val_dataset)}")
        logger.info("\n🤖 Initializing trainer...")
        trainer = AdCreativeTrainer(model_config)
        logger.info("✅ Trainer initialized")
        logger.info("\n🚀 Starting training...")
        best_val_loss = trainer.train(train_dataset, val_dataset)
        mlflow.log_metric("final_best_val_loss", best_val_loss)
        logger.info("\n💾 Saving final model...")
        trainer.save_model("final_model")
        model_uri = f"runs:/{mlflow.active_run().info.run_id}/final_model"
        model_details = mlflow.register_model(model_uri, "ad-creative-generator")
        logger.info(f"✅ Model registered: {model_details.name} version {model_details.version}")
        logger.info("\n" + "="*70)
        logger.info("✅ TRAINING COMPLETED SUCCESSFULLY!")
        logger.info("="*70)
        logger.info(f"Best Validation Loss: {best_val_loss:.4f}")
        logger.info(f"Model saved to: models/checkpoints/final_model")
        logger.info(f"MLflow Run ID: {mlflow.active_run().info.run_id}")
        logger.info("="*70)

if __name__ == "__main__":
    torch.manual_seed(42)
    main()
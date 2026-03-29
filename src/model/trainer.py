import torch
from torch.utils.data import DataLoader
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AdamW, get_linear_schedule_with_warmup
from tqdm import tqdm
import mlflow
import mlflow.pytorch
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger
from model.config import ModelConfig, GenerationConfig
from model.dataset import AdCreativeDataset

logger = get_logger(__name__)

class AdCreativeTrainer:
    """Trainer for T5 model fine-tuning"""
    def __init__(self, config: ModelConfig):
        self.config = config
        self.device = torch.device(config.device)
        logger.info(f"Using device: {self.device}")
        
        logger.info(f"Loading model: {config.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(config.model_name)
        self.model.to(self.device)
        
        logger.info(f"Model loaded successfully")
        logger.info(f"Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")
    
    def create_optimizer_and_scheduler(self, train_dataset):
        """Create optimizer and learning rate scheduler"""
        no_decay = ['bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {
                'params': [p for n, p in self.model.named_parameters() if not any(nd in n for nd in no_decay)],
                'weight_decay': self.config.weight_decay
            },
            {
                'params': [p for n, p in self.model.named_parameters() if any(nd in n for nd in no_decay)],
                'weight_decay': 0.0
            }
        ]
        optimizer = AdamW(optimizer_grouped_parameters, lr=self.config.learning_rate)
        total_steps = (len(train_dataset) // self.config.train_batch_size) * self.config.num_epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=self.config.warmup_steps,
            num_training_steps=total_steps
        )
        return optimizer, scheduler
    
    def train_epoch(self, train_loader, optimizer, scheduler, epoch):
        """Train for one epoch"""
        self.model.train()
        total_loss = 0
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{self.config.num_epochs}")
        
        for step, batch in enumerate(progress_bar):
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['labels'].to(self.device)
            
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            loss = loss / self.config.gradient_accumulation_steps
            loss.backward()
            
            if (step + 1) % self.config.gradient_accumulation_steps == 0:
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.max_grad_norm)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
            
            total_loss += loss.item() * self.config.gradient_accumulation_steps
            progress_bar.set_postfix({'loss': loss.item() * self.config.gradient_accumulation_steps})
            
            if (step + 1) % self.config.logging_steps == 0:
                avg_loss = total_loss / (step + 1)
                mlflow.log_metric("train_loss", avg_loss, step=epoch * len(train_loader) + step)
        
        return total_loss / len(train_loader)
    
    def evaluate(self, val_loader, epoch):
        """Evaluate on validation set"""
        self.model.eval()
        total_loss = 0
        
        with torch.no_grad():
            for batch in tqdm(val_loader, desc="Evaluating"):
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                total_loss += outputs.loss.item()
        
        avg_loss = total_loss / len(val_loader)
        mlflow.log_metric("val_loss", avg_loss, step=epoch)
        logger.info(f"Validation Loss: {avg_loss:.4f}")
        return avg_loss
    
    def train(self, train_dataset, val_dataset):
        """Complete training loop"""
        logger.info("Starting training...")
        
        train_loader = DataLoader(
            train_dataset,
            batch_size=self.config.train_batch_size,
            shuffle=True,
            num_workers=2
        )
        
        val_loader = DataLoader(
            val_dataset,
            batch_size=self.config.eval_batch_size,
            shuffle=False,
            num_workers=2
        )
        
        optimizer, scheduler = self.create_optimizer_and_scheduler(train_dataset)
        best_val_loss = float('inf')
        
        for epoch in range(self.config.num_epochs):
            logger.info(f"\n{'='*50}")
            logger.info(f"Epoch {epoch+1}/{self.config.num_epochs}")
            logger.info(f"{'='*50}")
            
            train_loss = self.train_epoch(train_loader, optimizer, scheduler, epoch)
            logger.info(f"Average Training Loss: {train_loss:.4f}")
            
            val_loss = self.evaluate(val_loader, epoch)
            
            mlflow.log_metrics({
                "epoch": epoch + 1,
                "train_loss_epoch": train_loss,
                "val_loss_epoch": val_loss
            }, step=epoch)
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                self.save_model(f"best_model_epoch_{epoch+1}")
                mlflow.log_metric("best_val_loss", best_val_loss)
                logger.info(f"✅ New best model saved! Val Loss: {val_loss:.4f}")
        
        logger.info(f"\n{'='*50}")
        logger.info(f"Training completed!")
        logger.info(f"Best Validation Loss: {best_val_loss:.4f}")
        logger.info(f"{'='*50}")
        
        return best_val_loss
    
    def save_model(self, checkpoint_name: str):
        """Save model checkpoint"""
        output_dir = Path(self.config.output_dir) / checkpoint_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        logger.info(f"Model saved to: {output_dir}")
        mlflow.pytorch.log_model(self.model, checkpoint_name)
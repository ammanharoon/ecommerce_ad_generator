import pandas as pd
import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer
from typing import Dict, List
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger

logger = get_logger(__name__)

class AdCreativeDataset(Dataset):
    """Dataset for ad creative generation"""
    def __init__(
        self,
        data_path: str,
        tokenizer: AutoTokenizer,
        max_input_length: int = 256,
        max_target_length: int = 128,
        is_training: bool = True
    ):
        self.tokenizer = tokenizer
        self.max_input_length = max_input_length
        self.max_target_length = max_target_length
        self.is_training = is_training
        logger.info(f"Loading dataset from: {data_path}")
        self.df = pd.read_csv(data_path)
        logger.info(f"Loaded {len(self.df)} samples")
        self.prepare_data()
    def prepare_data(self):
        """Prepare input and target texts"""
        self.inputs = []
        self.targets = []
        for idx, row in self.df.iterrows():
            input_text = self.create_input_prompt(row)
            target_text = self.create_target_ad(row)
            self.inputs.append(input_text)
            self.targets.append(target_text)
        logger.info(f"Prepared {len(self.inputs)} training samples")
    def create_input_prompt(self, row: pd.Series) -> str:
        """Create structured input prompt for T5"""
        prompt = f"Generate an engaging advertisement for this product:\n"
        prompt += f"Product Name: {row['product_name']}\n"
        prompt += f"Category: {row['category']}\n"
        prompt += f"Description: {row['description']}\n"
        prompt += f"Price: ${row['price']:.2f}\n"
        prompt += f"Create a compelling ad:"
        return prompt
    def create_target_ad(self, row: pd.Series) -> str:
        """Create target ad creative text"""
        templates = [
            f"🎯 {row['product_name']} - {row['category']} 💫\n\n{row['description']}\n\n✨ Only ${row['price']:.2f}! Order now and transform your {row['category'].lower()} experience! 🛒",
            f"✨ Discover {row['product_name']}! ✨\n\n{row['description']}\n\n🔥 Special Price: ${row['price']:.2f}\n\n💯 {row['category']} that exceeds expectations. Shop today!",
            f"🌟 {row['product_name']} 🌟\n\nCategory: {row['category']}\n\n{row['description']}\n\n💰 Amazing value at ${row['price']:.2f}!\n\n🚀 Elevate your lifestyle. Buy now!",
            f"💎 Premium {row['category']}: {row['product_name']}\n\n{row['description']}\n\n🎁 Yours for just ${row['price']:.2f}!\n\n⭐ Don't miss out on this incredible offer!",
            f"🔥 HOT DEAL: {row['product_name']} 🔥\n\n{row['description']}\n\n💵 Price: ${row['price']:.2f}\n\n✅ Best {row['category']} in its class. Limited stock!",
        ]
        import random
        return random.choice(templates)
    def __len__(self) -> int:
        return len(self.inputs)
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        input_text = self.inputs[idx]
        target_text = self.targets[idx]
        input_encoding = self.tokenizer(
            input_text,
            max_length=self.max_input_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        target_encoding = self.tokenizer(
            target_text,
            max_length=self.max_target_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        labels = target_encoding['input_ids'].squeeze()
        labels[labels == self.tokenizer.pad_token_id] = -100
        return {
            'input_ids': input_encoding['input_ids'].squeeze(),
            'attention_mask': input_encoding['attention_mask'].squeeze(),
            'labels': labels
        }

def prepare_datasets(
    data_path: str,
    tokenizer: AutoTokenizer,
    train_split: float = 0.8,
    max_input_length: int = 256,
    max_target_length: int = 128
):
    """Prepare train and validation datasets"""
    logger.info("Preparing train/val datasets...")
    df = pd.read_csv(data_path)
    train_size = int(len(df) * train_split)
    train_df = df[:train_size]
    val_df = df[train_size:]
    train_path = "data/processed/train.csv"
    val_path = "data/processed/val.csv"
    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    logger.info(f"Train samples: {len(train_df)}")
    logger.info(f"Val samples: {len(val_df)}")
    train_dataset = AdCreativeDataset(
        train_path, tokenizer, max_input_length, max_target_length, is_training=True
    )
    val_dataset = AdCreativeDataset(
        val_path, tokenizer, max_input_length, max_target_length, is_training=False
    )
    return train_dataset, val_dataset
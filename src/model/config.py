from dataclasses import dataclass
from typing import Optional
import torch

@dataclass
class ModelConfig: 
    """Model training configuration"""
    model_name:  str = "google/flan-t5-base"
    max_input_length: int = 256
    max_target_length:  int = 128
    train_batch_size: int = 4
    eval_batch_size:  int = 4
    learning_rate: float = 3e-5
    num_epochs: int = 5
    warmup_steps: int = 100
    weight_decay: float = 0.01
    gradient_accumulation_steps: int = 4
    max_grad_norm: float = 1.0
    seed: int = 42
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    output_dir: str = "models/checkpoints"
    logging_steps: int = 50
    save_steps: int = 500
    eval_steps:  int = 500
    fp16: bool = True

@dataclass
class GenerationConfig:
    """Text generation configuration"""
    max_length: int = 150
    min_length: int = 40
    temperature: float = 0.8
    top_p: float = 0.92
    top_k: int = 50
    num_beams: int = 5
    do_sample: bool = True
    no_repeat_ngram_size:  int = 3
    early_stopping: bool = True
    repetition_penalty: float = 1.2
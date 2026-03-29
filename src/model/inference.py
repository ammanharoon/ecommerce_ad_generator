import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from pathlib import Path
import sys
import os
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger
from model.config import GenerationConfig

logger = get_logger(__name__)

class AdCreativeGenerator:
    """Generate ad creatives using trained model"""
    def __init__(self, model_path: str, device: str = None):
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        
        logger.info(f"Loading model from: {model_path}")
        
        # Check if local model exists and has files
        model_exists = Path(model_path).exists() and any(Path(model_path).iterdir())
        
        if not model_exists:
            logger.warning(f"Model not found at {model_path}")
            logger.info("Downloading t5-base as fallback...")
            
            # Download t5-base
            self.model = AutoModelForSeq2SeqLM.from_pretrained('t5-base')
            self.tokenizer = AutoTokenizer.from_pretrained('t5-base')
            
            # Save it for next time
            try:
                os.makedirs(model_path, exist_ok=True)
                self.model.save_pretrained(model_path)
                self.tokenizer.save_pretrained(model_path)
                logger.info(f"✅ Model saved to {model_path}")
            except Exception as e:
                logger.warning(f"Could not save model: {e}")
        else:
            # Load from local path
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        self.model.to(self.device)
        self.model.eval()
        logger.info(f"✅ Model loaded on {self.device}")
        
        self.gen_config = GenerationConfig()
    
    def create_prompt(self, product_name: str, category: str, description: str, price: float) -> str:
        """Create input prompt"""
        prompt = f"Generate an engaging advertisement for this product:\n"
        prompt += f"Product Name: {product_name}\n"
        prompt += f"Category: {category}\n"
        prompt += f"Description: {description}\n"
        prompt += f"Price: ${price:.2f}\n"
        prompt += f"Create a compelling ad:"
        return prompt
    
    def generate(
        self,
        product_name: str,
        category: str,
        description: str,
        price: float,
        num_variants: int = 1
    ) -> list:
        """Generate ad creative(s)"""
        prompt = self.create_prompt(product_name, category, description, price)
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=256,
            truncation=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=self.gen_config.max_length,
                min_length=self.gen_config.min_length,
                do_sample=self.gen_config.do_sample,
                temperature=self.gen_config.temperature,
                top_p=self.gen_config.top_p,
                top_k=self.gen_config.top_k,
                num_beams=self.gen_config.num_beams,
                no_repeat_ngram_size=self.gen_config.no_repeat_ngram_size,
                repetition_penalty=self.gen_config.repetition_penalty,
                early_stopping=self.gen_config.early_stopping,
                num_return_sequences=num_variants
            )
        
        generated_ads = [
            self.tokenizer.decode(output, skip_special_tokens=True)
            for output in outputs
        ]
        
        return generated_ads
    
    def generate_batch(self, products: list) -> list:
        """Generate ads for multiple products"""
        results = []
        for product in products:
            ads = self.generate(
                product['product_name'],
                product['category'],
                product['description'],
                product['price']
            )
            results.append({
                'product': product,
                'generated_ads': ads
            })
        return results

if __name__ == "__main__":
    model_path = "models/checkpoints/final_model"
    
    generator = AdCreativeGenerator(model_path)
    
    test_product = {
        "product_name": "Wireless Bluetooth Headphones",
        "category": "Electronics",
        "description": "Premium noise-cancelling headphones with 30-hour battery life",
        "price": 79.99
    }
    
    logger.info("\n" + "="*70)
    logger.info("GENERATING AD CREATIVE")
    logger.info("="*70)
    logger.info(f"Product: {test_product['product_name']}")
    logger.info(f"Category: {test_product['category']}")
    logger.info(f"Price: ${test_product['price']}")
    
    ads = generator.generate(
        test_product['product_name'],
        test_product['category'],
        test_product['description'],
        test_product['price'],
        num_variants=3
    )
    
    logger.info("\n📝 Generated Ad Creatives:")
    for i, ad in enumerate(ads, 1):
        logger.info(f"\n--- Variant {i} ---")
        logger.info(ad)
    
    logger.info("\n" + "="*70)
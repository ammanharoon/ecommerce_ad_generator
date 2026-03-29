import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger
from model.inference import AdCreativeGenerator

logger = get_logger(__name__)

def evaluate_model(model_path: str, test_data_path: str, num_samples: int = 10):
    """Evaluate model on test samples"""
    logger.info("="*70)
    logger.info("MODEL EVALUATION")
    logger.info("="*70)
    generator = AdCreativeGenerator(model_path)
    df = pd.read_csv(test_data_path)
    test_samples = df.sample(n=min(num_samples, len(df)))
    results = []
    for idx, row in test_samples.iterrows():
        logger.info(f"\n{'='*70}")
        logger.info(f"Sample {idx+1}/{num_samples}")
        logger.info(f"{'='*70}")
        logger.info(f"Product: {row['product_name']}")
        logger.info(f"Category: {row['category']}")
        logger.info(f"Price: ${row['price']:.2f}")
        logger.info(f"\nOriginal Description:")
        logger.info(row['description'])
        ads = generator.generate(
            row['product_name'],
            row['category'],
            row['description'],
            row['price'],
            num_variants=2
        )
        logger.info(f"\n📝 Generated Ads:")
        for i, ad in enumerate(ads, 1):
            logger.info(f"\n--- Variant {i} ---")
            logger.info(ad)
        results.append({
            'product_id': row['product_id'],
            'product_name': row['product_name'],
            'category': row['category'],
            'price': row['price'],
            'generated_ad_1': ads[0] if len(ads) > 0 else "",
            'generated_ad_2': ads[1] if len(ads) > 1 else ""
        })
    results_df = pd.DataFrame(results)
    output_path = "data/processed/evaluation_results.csv"
    results_df.to_csv(output_path, index=False)
    logger.info(f"\n✅ Evaluation results saved to: {output_path}")
    logger.info("="*70)

if __name__ == "__main__":
    model_path = "models/checkpoints/final_model"
    test_data_path = "data/processed/val.csv"
    if not Path(model_path).exists():
        logger.error(f"Model not found: {model_path}")
        sys.exit(1)
    if not Path(test_data_path).exists():
        logger.error(f"Test data not found: {test_data_path}")
        sys.exit(1)
    evaluate_model(model_path, test_data_path, num_samples=10)
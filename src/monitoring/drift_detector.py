"""
Data Drift Detection for ML Model Monitoring
Detects distribution shifts in incoming data vs training data
"""
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple
from datetime import datetime
from pathlib import Path
import json

class DriftDetector:
    """Detect data drift using statistical tests"""
    
    def __init__(self, reference_data_path: str = "data/processed/train.csv"):
        """Initialize with reference training data statistics"""
        self.reference_data_path = reference_data_path
        self.reference_stats = {}
        self.drift_threshold = 0.05  # p-value threshold
        self.drift_history = []
        
        # Load reference data statistics
        self._compute_reference_stats()
    
    def _compute_reference_stats(self):
        """Compute statistics from reference (training) data"""
        try:
            df = pd.read_csv(self.reference_data_path)
            
            self.reference_stats = {
                'price': {
                    'mean': df['price'].mean(),
                    'std': df['price'].std(),
                    'distribution': df['price'].values
                },
                'description_length': {
                    'mean': df['description'].str.len().mean(),
                    'std': df['description'].str.len().std(),
                    'distribution': df['description'].str.len().values
                },
                'category_distribution': df['category'].value_counts().to_dict(),
                'sample_size': len(df)
            }
            print(f"✅ Reference statistics computed from {len(df)} samples")
        except Exception as e:
            print(f"⚠️ Could not load reference data: {e}")
            # Use default stats if file doesn't exist
            self.reference_stats = {
                'price': {'mean': 100.0, 'std': 50.0, 'distribution': [100.0]},
                'description_length': {'mean': 200.0, 'std': 50.0, 'distribution': [200.0]},
                'category_distribution': {},
                'sample_size': 0
            }
    
    def detect_drift(self, incoming_data: List[Dict]) -> Dict:
        """
        Detect drift in incoming data using Kolmogorov-Smirnov test
        
        Args:
            incoming_data: List of product dictionaries with keys: 
                          product_name, category, description, price
        
        Returns:
            Dict with drift detection results
        """
        if not incoming_data:
            return {'drift_detected': False, 'reason': 'No data'}
        
        df = pd.DataFrame(incoming_data)
        
        # Extract features
        current_prices = df['price'].values
        current_desc_lengths = df['description'].str.len().values
        current_categories = df['category'].value_counts().to_dict()
        
        drift_results = {
            'timestamp': datetime.now().isoformat(),
            'sample_size': len(df),
            'tests': {}
        }
        
        # 1. Price distribution drift (KS test)
        if len(self.reference_stats['price']['distribution']) > 0:
            ks_stat, p_value = stats.ks_2samp(
                self.reference_stats['price']['distribution'],
                current_prices
            )
            drift_results['tests']['price_drift'] = {
                'test': 'Kolmogorov-Smirnov',
                'statistic': float(ks_stat),
                'p_value': float(p_value),
                'drift_detected': p_value < self.drift_threshold,
                'severity': self._get_severity(p_value)
            }
        
        # 2. Description length drift
        if len(self.reference_stats['description_length']['distribution']) > 0:
            ks_stat, p_value = stats.ks_2samp(
                self.reference_stats['description_length']['distribution'],
                current_desc_lengths
            )
            drift_results['tests']['description_length_drift'] = {
                'test': 'Kolmogorov-Smirnov',
                'statistic': float(ks_stat),
                'p_value': float(p_value),
                'drift_detected': p_value < self.drift_threshold,
                'severity': self._get_severity(p_value)
            }
        
        # 3. Category distribution drift (Chi-square test)
        drift_results['tests']['category_drift'] = self._detect_category_drift(
            current_categories
        )
        
        # 4. Statistical summaries
        drift_results['statistics'] = {
            'current_price_mean': float(current_prices.mean()),
            'reference_price_mean': float(self.reference_stats['price']['mean']),
            'price_shift': float(current_prices.mean() - self.reference_stats['price']['mean']),
            'current_desc_length_mean': float(current_desc_lengths.mean()),
            'reference_desc_length_mean': float(self.reference_stats['description_length']['mean'])
        }
        
        # Overall drift detection
        any_drift = any(
            test.get('drift_detected', False) 
            for test in drift_results['tests'].values()
        )
        
        drift_results['drift_detected'] = any_drift
        drift_results['alert_level'] = self._get_alert_level(drift_results['tests'])
        
        # Store in history
        self.drift_history.append(drift_results)
        
        return drift_results
    
    def _detect_category_drift(self, current_categories: Dict) -> Dict:
        """Detect drift in category distribution"""
        ref_categories = self.reference_stats['category_distribution']
        
        # Calculate distribution difference
        all_categories = set(list(ref_categories.keys()) + list(current_categories.keys()))
        
        differences = []
        for cat in all_categories:
            ref_prop = ref_categories.get(cat, 0) / max(self.reference_stats['sample_size'], 1)
            curr_prop = current_categories.get(cat, 0) / max(sum(current_categories.values()), 1)
            differences.append(abs(ref_prop - curr_prop))
        
        max_diff = max(differences) if differences else 0
        drift_detected = max_diff > 0.2  # 20% threshold
        
        return {
            'test': 'Distribution Comparison',
            'max_difference': float(max_diff),
            'drift_detected': drift_detected,
            'severity': 'high' if max_diff > 0.3 else 'medium' if max_diff > 0.2 else 'low'
        }
    
    def _get_severity(self, p_value: float) -> str:
        """Get drift severity based on p-value"""
        if p_value < 0.01:
            return 'high'
        elif p_value < 0.05:
            return 'medium'
        else:
            return 'low'
    
    def _get_alert_level(self, tests: Dict) -> str:
        """Get overall alert level"""
        high_count = sum(1 for t in tests.values() if t.get('severity') == 'high')
        medium_count = sum(1 for t in tests.values() if t.get('severity') == 'medium')
        
        if high_count > 0:
            return 'CRITICAL'
        elif medium_count > 1:
            return 'WARNING'
        else:
            return 'NORMAL'
    
    def get_drift_report(self) -> Dict:
        """Get summary report of recent drift detections"""
        if not self.drift_history:
            return {'status': 'No drift checks performed'}
        
        recent = self.drift_history[-10:]  # Last 10 checks
        
        return {
            'total_checks': len(self.drift_history),
            'recent_checks': len(recent),
            'drift_detected_count': sum(1 for d in recent if d['drift_detected']),
            'latest_check': recent[-1],
            'alert_summary': {
                'CRITICAL': sum(1 for d in recent if d.get('alert_level') == 'CRITICAL'),
                'WARNING': sum(1 for d in recent if d.get('alert_level') == 'WARNING'),
                'NORMAL': sum(1 for d in recent if d.get('alert_level') == 'NORMAL')
            }
        }
    
    def save_drift_history(self, filepath: str = "logs/drift_history.json"):
        """Save drift history to file"""
        Path(filepath).parent.mkdir(exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.drift_history, f, indent=2)


# Global drift detector instance
drift_detector = DriftDetector()

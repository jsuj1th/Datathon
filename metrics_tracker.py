"""
Metrics Tracker for Document Classification System
Tracks precision, recall, confidence, throughput, and safety validation
"""

import time
from datetime import datetime
from typing import Dict, List

class MetricsTracker:
    def __init__(self):
        self.test_results = []
        self.start_time = None
        self.end_time = None
        
    def start_test(self):
        """Start timing for throughput measurement"""
        self.start_time = time.time()
    
    def end_test(self):
        """End timing for throughput measurement"""
        self.end_time = time.time()
    
    def add_result(self, test_case: str, expected: str, actual: str, 
                   confidence: float, processing_time: float, 
                   safety_check: bool, needs_review: bool):
        """Add a test result"""
        self.test_results.append({
            'test_case': test_case,
            'expected': expected.lower().replace(' ', '_'),
            'actual': actual.lower().replace(' ', '_'),
            'confidence': confidence,
            'processing_time': processing_time,
            'safety_check': safety_check,
            'needs_review': needs_review,
            'timestamp': datetime.now().isoformat()
        })
    
    def calculate_precision_recall(self) -> Dict:
        """Calculate precision and recall for each category"""
        if not self.test_results:
            return {}
        
        categories = ['public', 'confidential', 'highly_sensitive', 'unsafe']
        metrics = {}
        
        for category in categories:
            # True Positives: correctly classified as this category
            tp = sum(1 for r in self.test_results 
                    if r['expected'] == category and r['actual'] == category)
            
            # False Positives: incorrectly classified as this category
            fp = sum(1 for r in self.test_results 
                    if r['expected'] != category and r['actual'] == category)
            
            # False Negatives: should be this category but classified as something else
            fn = sum(1 for r in self.test_results 
                    if r['expected'] == category and r['actual'] != category)
            
            # Calculate precision and recall
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            metrics[category] = {
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score,
                'true_positives': tp,
                'false_positives': fp,
                'false_negatives': fn
            }
        
        return metrics
    
    def calculate_overall_accuracy(self) -> float:
        """Calculate overall classification accuracy"""
        if not self.test_results:
            return 0.0
        
        correct = sum(1 for r in self.test_results if r['expected'] == r['actual'])
        return correct / len(self.test_results)
    
    def calculate_average_confidence(self) -> float:
        """Calculate average confidence score"""
        if not self.test_results:
            return 0.0
        
        return sum(r['confidence'] for r in self.test_results) / len(self.test_results)
    
    def calculate_throughput(self) -> Dict:
        """Calculate throughput metrics"""
        if not self.test_results:
            return {'avg_time': 0, 'total_time': 0, 'docs_per_minute': 0}
        
        total_time = sum(r['processing_time'] for r in self.test_results)
        avg_time = total_time / len(self.test_results)
        docs_per_minute = 60 / avg_time if avg_time > 0 else 0
        
        return {
            'avg_time_seconds': round(avg_time, 2),
            'total_time_seconds': round(total_time, 2),
            'docs_per_minute': round(docs_per_minute, 2),
            'total_documents': len(self.test_results)
        }
    
    def calculate_review_metrics(self) -> Dict:
        """Calculate HITL review metrics"""
        if not self.test_results:
            return {'needs_review': 0, 'auto_classified': 0, 'review_rate': 0}
        
        needs_review = sum(1 for r in self.test_results if r['needs_review'])
        auto_classified = len(self.test_results) - needs_review
        review_rate = needs_review / len(self.test_results)
        
        # Calculate time saved (assuming manual review takes 5 minutes per doc)
        manual_review_time = len(self.test_results) * 5  # minutes
        actual_review_time = needs_review * 5  # minutes
        time_saved = manual_review_time - actual_review_time
        
        return {
            'needs_review': needs_review,
            'auto_classified': auto_classified,
            'review_rate': round(review_rate, 3),
            'time_saved_minutes': time_saved,
            'reduction_percentage': round((1 - review_rate) * 100, 1)
        }
    
    def validate_safety(self) -> Dict:
        """Validate all content for child safety"""
        if not self.test_results:
            return {'all_safe': True, 'unsafe_count': 0, 'safety_rate': 1.0}
        
        unsafe_count = sum(1 for r in self.test_results if not r['safety_check'])
        all_safe = unsafe_count == 0
        safety_rate = (len(self.test_results) - unsafe_count) / len(self.test_results)
        
        return {
            'all_safe': all_safe,
            'unsafe_count': unsafe_count,
            'safe_count': len(self.test_results) - unsafe_count,
            'safety_rate': round(safety_rate, 3),
            'validation_passed': all_safe or unsafe_count == sum(1 for r in self.test_results if r['expected'] == 'unsafe')
        }
    
    def get_model_info(self) -> Dict:
        """Get information about the model being used"""
        return {
            'primary_model': 'openai/gpt-4o',
            'model_type': 'Large Language Model (LLM)',
            'provider': 'OpenRouter',
            'capabilities': ['Multi-modal (text + images)', 'JSON output', 'Vision analysis'],
            'context_window': '128K tokens',
            'supports_vision': True
        }
    
    def generate_report(self) -> Dict:
        """Generate comprehensive metrics report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'model_info': self.get_model_info(),
            'accuracy': self.calculate_overall_accuracy(),
            'precision_recall': self.calculate_precision_recall(),
            'confidence': {
                'average': self.calculate_average_confidence(),
                'by_test': [{'test': r['test_case'], 'confidence': r['confidence']} 
                           for r in self.test_results]
            },
            'throughput': self.calculate_throughput(),
            'review_metrics': self.calculate_review_metrics(),
            'safety_validation': self.validate_safety(),
            'test_results': self.test_results
        }
    
    def print_summary(self):
        """Print a formatted summary of metrics"""
        report = self.generate_report()
        
        print("\n" + "="*80)
        print("COMPREHENSIVE METRICS REPORT")
        print("="*80)
        
        print(f"\n📊 MODEL INFORMATION:")
        model = report['model_info']
        print(f"   Primary Model: {model['primary_model']}")
        print(f"   Type: {model['model_type']}")
        print(f"   Provider: {model['provider']}")
        print(f"   Capabilities: {', '.join(model['capabilities'])}")
        
        print(f"\n🎯 ACCURACY METRICS:")
        print(f"   Overall Accuracy: {report['accuracy']:.1%}")
        print(f"   Average Confidence: {report['confidence']['average']:.1%}")
        
        print(f"\n📈 PRECISION & RECALL:")
        for category, metrics in report['precision_recall'].items():
            if metrics['true_positives'] > 0 or metrics['false_positives'] > 0 or metrics['false_negatives'] > 0:
                print(f"   {category.upper()}:")
                print(f"      Precision: {metrics['precision']:.1%}")
                print(f"      Recall: {metrics['recall']:.1%}")
                print(f"      F1 Score: {metrics['f1_score']:.3f}")
        
        print(f"\n⚡ THROUGHPUT & RESPONSIVENESS:")
        throughput = report['throughput']
        print(f"   Average Processing Time: {throughput['avg_time_seconds']}s per document")
        print(f"   Throughput: {throughput['docs_per_minute']} documents/minute")
        print(f"   Total Documents: {throughput['total_documents']}")
        
        print(f"\n👥 HITL REVIEW METRICS:")
        review = report['review_metrics']
        print(f"   Auto-classified: {review['auto_classified']} documents")
        print(f"   Needs Review: {review['needs_review']} documents")
        print(f"   Manual Review Reduction: {review['reduction_percentage']}%")
        print(f"   Time Saved: {review['time_saved_minutes']} minutes")
        
        print(f"\n🛡️ SAFETY VALIDATION:")
        safety = report['safety_validation']
        print(f"   All Content Safe: {'✓ YES' if safety['all_safe'] else '✗ NO'}")
        print(f"   Safe Documents: {safety['safe_count']}/{len(self.test_results)}")
        print(f"   Safety Rate: {safety['safety_rate']:.1%}")
        print(f"   Validation: {'✓ PASSED' if safety['validation_passed'] else '✗ FAILED'}")
        
        print("\n" + "="*80)

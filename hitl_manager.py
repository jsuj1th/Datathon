import json
import os
from datetime import datetime

class HITLManager:
    """
    Human-in-the-Loop feedback manager
    """
    
    def __init__(self, feedback_file='hitl_feedback.json'):
        self.feedback_file = feedback_file
        self.feedback_data = self._load_feedback()
    
    def _load_feedback(self):
        """Load existing feedback data"""
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        return {'feedback_entries': [], 'statistics': {}}
    
    def _save_feedback(self):
        """Save feedback data"""
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
    
    def submit_feedback(self, document_id, classification_result, human_feedback):
        """
        Submit human feedback for a classification
        
        Args:
            document_id: Unique identifier for the document
            classification_result: Original AI classification
            human_feedback: Dict with corrected_category, notes, etc.
        """
        feedback_entry = {
            'document_id': document_id,
            'timestamp': datetime.now().isoformat(),
            'ai_classification': classification_result.get('category'),
            'ai_confidence': classification_result.get('confidence'),
            'human_classification': human_feedback.get('corrected_category'),
            'human_notes': human_feedback.get('notes', ''),
            'agreement': classification_result.get('category') == human_feedback.get('corrected_category'),
            'evidence_quality': human_feedback.get('evidence_quality', 'good')
        }
        
        self.feedback_data['feedback_entries'].append(feedback_entry)
        self._update_statistics()
        self._save_feedback()
        
        return feedback_entry
    
    def _update_statistics(self):
        """Update feedback statistics"""
        entries = self.feedback_data['feedback_entries']
        
        if not entries:
            return
        
        total = len(entries)
        agreements = sum(1 for e in entries if e.get('agreement', False))
        
        self.feedback_data['statistics'] = {
            'total_feedback': total,
            'agreement_rate': agreements / total if total > 0 else 0,
            'disagreement_rate': (total - agreements) / total if total > 0 else 0,
            'last_updated': datetime.now().isoformat()
        }
    
    def get_feedback_for_training(self):
        """
        Get feedback data formatted for model fine-tuning or prompt improvement
        """
        training_data = []
        
        for entry in self.feedback_data['feedback_entries']:
            if not entry.get('agreement', False):
                # Focus on disagreements for learning
                training_data.append({
                    'document_id': entry['document_id'],
                    'incorrect_prediction': entry['ai_classification'],
                    'correct_label': entry['human_classification'],
                    'notes': entry['human_notes']
                })
        
        return training_data
    
    def get_statistics(self):
        """Get current HITL statistics"""
        return self.feedback_data.get('statistics', {})
    
    def should_flag_for_review(self, classification_result):
        """
        Determine if a classification should be flagged for human review
        """
        # Flag if confidence is low
        if classification_result.get('confidence', 1.0) < 0.7:
            return True, 'Low confidence score'
        
        # Flag if dual-LLM disagreement
        if classification_result.get('requires_hitl', False):
            return True, classification_result.get('hitl_reason', 'Flagged for review')
        
        # Flag if unsafe content detected
        if classification_result.get('category') == 'unsafe':
            return True, 'Unsafe content requires human verification'
        
        # Flag if highly sensitive with multiple evidence types
        if classification_result.get('category') == 'highly_sensitive':
            evidence_types = len(classification_result.get('evidence', []))
            if evidence_types > 2:
                return True, 'Multiple sensitive elements detected'
        
        return False, None

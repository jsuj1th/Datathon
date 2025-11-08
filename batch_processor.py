import os
import json
from datetime import datetime
from threading import Thread, Lock
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from hitl_manager import HITLManager

class BatchProcessor:
    """
    Batch processing with real-time status updates
    """
    
    def __init__(self):
        self.preprocessor = DocumentPreprocessor()
        self.classifier = DocumentClassifier()
        self.hitl_manager = HITLManager()
        self.jobs = {}
        self.jobs_lock = Lock()
    
    def create_batch_job(self, file_paths, job_id=None):
        """
        Create a new batch processing job
        """
        if job_id is None:
            job_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        job = {
            'job_id': job_id,
            'status': 'pending',
            'total_files': len(file_paths),
            'processed_files': 0,
            'failed_files': 0,
            'results': [],
            'started_at': None,
            'completed_at': None,
            'current_file': None
        }
        
        with self.jobs_lock:
            self.jobs[job_id] = job
        
        # Start processing in background thread
        thread = Thread(target=self._process_batch, args=(job_id, file_paths))
        thread.daemon = True
        thread.start()
        
        return job_id
    
    def _process_batch(self, job_id, file_paths):
        """
        Process batch of files
        """
        with self.jobs_lock:
            self.jobs[job_id]['status'] = 'processing'
            self.jobs[job_id]['started_at'] = datetime.now().isoformat()
        
        for idx, file_path in enumerate(file_paths):
            try:
                # Update current file
                with self.jobs_lock:
                    self.jobs[job_id]['current_file'] = os.path.basename(file_path)
                
                # Pre-process
                preprocess_result = self.preprocessor.check_file_validity(file_path)
                
                if not preprocess_result['valid']:
                    result = {
                        'file': file_path,
                        'status': 'failed',
                        'error': preprocess_result['errors']
                    }
                    with self.jobs_lock:
                        self.jobs[job_id]['results'].append(result)
                        self.jobs[job_id]['failed_files'] += 1
                    continue
                
                # Extract content
                metadata = preprocess_result['metadata']
                content = self.preprocessor.extract_content_for_analysis(file_path, metadata)
                
                # Classify
                classification = self.classifier.classify_document(content, metadata)
                
                # Check if HITL needed
                needs_review, review_reason = self.hitl_manager.should_flag_for_review(classification)
                
                result = {
                    'file': file_path,
                    'status': 'success',
                    'classification': classification,
                    'needs_review': needs_review,
                    'review_reason': review_reason
                }
                
                with self.jobs_lock:
                    self.jobs[job_id]['results'].append(result)
                    self.jobs[job_id]['processed_files'] += 1
                
            except Exception as e:
                result = {
                    'file': file_path,
                    'status': 'failed',
                    'error': str(e)
                }
                with self.jobs_lock:
                    self.jobs[job_id]['results'].append(result)
                    self.jobs[job_id]['failed_files'] += 1
        
        # Mark job as complete
        with self.jobs_lock:
            self.jobs[job_id]['status'] = 'completed'
            self.jobs[job_id]['completed_at'] = datetime.now().isoformat()
            self.jobs[job_id]['current_file'] = None
    
    def get_job_status(self, job_id):
        """
        Get real-time status of a batch job
        """
        with self.jobs_lock:
            if job_id not in self.jobs:
                return None
            
            job = self.jobs[job_id].copy()
            
            # Calculate progress percentage
            if job['total_files'] > 0:
                job['progress_percent'] = (job['processed_files'] + job['failed_files']) / job['total_files'] * 100
            else:
                job['progress_percent'] = 0
            
            return job
    
    def get_job_results(self, job_id):
        """
        Get results of a completed batch job
        """
        with self.jobs_lock:
            if job_id not in self.jobs:
                return None
            return self.jobs[job_id]['results']
    
    def export_results(self, job_id, output_path):
        """
        Export batch results to JSON file
        """
        results = self.get_job_results(job_id)
        if results is None:
            return False
        
        with open(output_path, 'w') as f:
            json.dump({
                'job_id': job_id,
                'results': results,
                'exported_at': datetime.now().isoformat()
            }, f, indent=2)
        
        return True

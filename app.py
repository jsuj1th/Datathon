import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime

from config import Config
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from hitl_manager import HITLManager
from batch_processor import BatchProcessor

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Initialize components
preprocessor = DocumentPreprocessor()
classifier = DocumentClassifier()
hitl_manager = HITLManager()
batch_processor = BatchProcessor()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/classify', methods=['POST'])
def classify_document():
    """
    Interactive single document classification
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Pre-process
        preprocess_result = preprocessor.check_file_validity(filepath)
        
        if not preprocess_result['valid']:
            return jsonify({
                'error': 'Pre-processing failed',
                'details': preprocess_result['errors']
            }), 400
        
        # Extract content
        metadata = preprocess_result['metadata']
        content = preprocessor.extract_content_for_analysis(filepath, metadata)
        
        # Classify
        classification = classifier.classify_document(content, metadata)
        
        # Check if HITL needed
        needs_review, review_reason = hitl_manager.should_flag_for_review(classification)
        
        result = {
            'filename': file.filename,
            'document_id': filename,
            'classification': classification,
            'needs_review': needs_review,
            'review_reason': review_reason,
            'preprocess_checks': {
                'valid': preprocess_result['valid'],
                'warnings': preprocess_result.get('warnings', [])
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch', methods=['POST'])
def create_batch_job():
    """
    Create batch processing job
    """
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    
    if not files:
        return jsonify({'error': 'No files selected'}), 400
    
    try:
        # Save all files
        file_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                file_paths.append(filepath)
        
        # Create batch job
        job_id = batch_processor.create_batch_job(file_paths)
        
        return jsonify({
            'job_id': job_id,
            'total_files': len(file_paths),
            'status': 'processing'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch/<job_id>/status', methods=['GET'])
def get_batch_status(job_id):
    """
    Get batch job status
    """
    status = batch_processor.get_job_status(job_id)
    
    if status is None:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(status)

@app.route('/api/batch/<job_id>/results', methods=['GET'])
def get_batch_results(job_id):
    """
    Get batch job results
    """
    results = batch_processor.get_job_results(job_id)
    
    if results is None:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify({'results': results})

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit HITL feedback
    """
    data = request.json
    
    document_id = data.get('document_id')
    classification_result = data.get('classification_result')
    human_feedback = data.get('human_feedback')
    
    if not all([document_id, classification_result, human_feedback]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        feedback_entry = hitl_manager.submit_feedback(
            document_id,
            classification_result,
            human_feedback
        )
        
        return jsonify({
            'success': True,
            'feedback_entry': feedback_entry
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get HITL statistics
    """
    stats = hitl_manager.get_statistics()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

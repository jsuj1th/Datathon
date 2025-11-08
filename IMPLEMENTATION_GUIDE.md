# Implementation Guide

## Setup Instructions

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies (for PDF and OCR processing)
# macOS:
brew install poppler tesseract

# Ubuntu/Debian:
sudo apt-get install poppler-utils tesseract-ocr
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here  # Optional
ENABLE_DUAL_LLM=false  # Set to true for dual-LLM verification
```

### 3. Create Required Directories

```bash
mkdir -p uploads test_documents
```

### 4. Test the System

```bash
python test_system.py
```

### 5. Run the Application

```bash
python app.py
```

Access the UI at: http://localhost:5000

## Architecture Overview

### Components

1. **Preprocessor** (`preprocessor.py`)
   - File validation and quality checks
   - Page/image counting
   - Text extraction (OCR for images)
   - Legibility assessment

2. **Prompt Library** (`prompt_library.py`)
   - Configurable prompt templates
   - Dynamic prompt tree generation
   - Stage-specific prompts (PII, safety, proprietary)

3. **Classifier** (`classifier.py`)
   - Multi-stage classification pipeline
   - Vision model support for images
   - Result aggregation
   - Optional dual-LLM verification

4. **HITL Manager** (`hitl_manager.py`)
   - Feedback collection and storage
   - Statistics tracking
   - Training data generation
   - Review flagging logic

5. **Batch Processor** (`batch_processor.py`)
   - Asynchronous batch processing
   - Real-time status updates
   - Result aggregation

6. **Web Application** (`app.py`)
   - Flask REST API
   - Interactive and batch modes
   - Feedback submission
   - Statistics dashboard

## Test Cases

### TC1: Public Marketing Document

**Input**: Multi-page brochure (public content)
**Expected**: Public classification
**Evidence**: Citations to marketing content, no PII

### TC2: Employment Application with PII

**Input**: Form with SSN, address, personal details
**Expected**: Highly Sensitive classification
**Evidence**: Specific PII field citations

### TC3: Internal Memo

**Input**: Internal project documentation
**Expected**: Confidential classification
**Evidence**: Internal-only operational details

### TC4: Stealth Fighter Image

**Input**: Military equipment image
**Expected**: Confidential/Highly Sensitive
**Evidence**: Image region citations

### TC5: Mixed Content

**Input**: Document with multiple classification triggers
**Expected**: Highest priority classification + Unsafe flag
**Evidence**: Multiple citations for different issues

## Customization

### Adding New Classification Categories

Edit `config.py`:

```python
CATEGORIES = {
    'highly_sensitive': 'Highly Sensitive',
    'confidential': 'Confidential',
    'public': 'Public',
    'unsafe': 'Unsafe',
    'your_new_category': 'Your New Category'
}
```

### Modifying Prompts

Edit `prompt_library.py` to customize classification logic:

```python
@staticmethod
def get_custom_prompt():
    return """Your custom prompt here..."""
```

### Adjusting HITL Thresholds

Edit `hitl_manager.py`:

```python
def should_flag_for_review(self, classification_result):
    # Adjust confidence threshold
    if classification_result.get('confidence', 1.0) < 0.8:  # Changed from 0.7
        return True, 'Low confidence score'
```

## API Endpoints

### POST /api/classify
Classify a single document

**Request**: multipart/form-data with 'file'
**Response**: Classification result with evidence

### POST /api/batch
Create batch processing job

**Request**: multipart/form-data with 'files[]'
**Response**: Job ID and status

### GET /api/batch/{job_id}/status
Get batch job status

**Response**: Progress and current status

### GET /api/batch/{job_id}/results
Get batch job results

**Response**: Array of classification results

### POST /api/feedback
Submit HITL feedback

**Request**: JSON with document_id, classification_result, human_feedback
**Response**: Feedback entry confirmation

### GET /api/statistics
Get HITL statistics

**Response**: Agreement rates and feedback counts

## Security Considerations

1. **File Upload Limits**: Configured in `config.py` (default 50MB)
2. **Allowed File Types**: PDF, PNG, JPG, JPEG, TIFF, BMP only
3. **API Key Security**: Store in `.env`, never commit to version control
4. **Data Privacy**: Uploaded files stored in `uploads/` directory
5. **HITL Data**: Feedback stored in `hitl_feedback.json`

## Performance Optimization

1. **Batch Processing**: Use batch mode for multiple documents
2. **Image Limits**: First 10 pages converted to images for analysis
3. **Text Truncation**: Text limited to 10,000 characters per analysis
4. **Dual-LLM**: Enable only when high accuracy is critical (slower)

## Troubleshooting

### "OpenAI API key not configured"
- Ensure `.env` file exists with valid `OPENAI_API_KEY`

### "Pre-processing failed"
- Check file format is supported
- Verify file is not corrupted
- Check file size is under limit

### "Classification timeout"
- Large files may take longer
- Check API rate limits
- Consider batch processing for multiple files

### OCR not working
- Install tesseract: `brew install tesseract` (macOS)
- Verify tesseract is in PATH

## Production Deployment

1. Set `FLASK_ENV=production` in `.env`
2. Use production WSGI server (gunicorn, uwsgi)
3. Configure reverse proxy (nginx, Apache)
4. Set up SSL/TLS certificates
5. Implement rate limiting
6. Configure logging and monitoring
7. Set up backup for feedback data
8. Implement user authentication if needed

## Future Enhancements

- Video content analysis
- Multi-language support
- Custom classification rules engine
- Advanced audit trail with blockchain
- Integration with document management systems
- Real-time collaboration features
- Model fine-tuning based on HITL feedback

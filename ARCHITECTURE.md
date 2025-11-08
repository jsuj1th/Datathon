# AI Document Classification System - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                               │
├─────────────────────────────────────────────────────────────────────┤
│  Streamlit UI (demo_ui.py)  │  Flask API (app.py)  │  CLI Scripts   │
│  • Interactive classification │  • REST endpoints    │  • Test cases  │
│  • File upload               │  • Batch jobs        │  • Automation  │
│  • Metrics dashboard         │  • Status queries    │                │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────┐      ┌──────────────────────┐              │
│  │  Batch Processor   │      │  Single Document     │              │
│  │  (batch_processor) │      │  Processor           │              │
│  │                    │      │                      │              │
│  │  • Job queue       │      │  • Real-time         │              │
│  │  • Threading       │      │  • Interactive       │              │
│  │  • Status tracking │      │  • Immediate results │              │
│  └────────────────────┘      └──────────────────────┘              │
│            ↓                            ↓                            │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    DOCUMENT PREPROCESSING                            │
├─────────────────────────────────────────────────────────────────────┤
│                   DocumentPreprocessor (preprocessor.py)             │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Validation  │  │   Content    │  │    Image     │             │
│  │              │  │  Extraction  │  │  Processing  │             │
│  │ • File size  │  │ • PDF text   │  │ • PDF→Images │             │
│  │ • File type  │  │ • OCR text   │  │ • Quality    │             │
│  │ • Legibility │  │ • Metadata   │  │ • Conversion │             │
│  │ • Page count │  │              │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                       │
│  Output: {text, images[], metadata}                                  │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   CLASSIFICATION ENGINE                              │
├─────────────────────────────────────────────────────────────────────┤
│                 DocumentClassifier (classifier.py)                   │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │              Dynamic Prompt Tree (prompt_library.py)          │ │
│  │                                                                │ │
│  │  Stage 1: Base Classification                                 │ │
│  │  ├─ Analyze full document                                     │ │
│  │  ├─ Multi-modal (text + images)                               │ │
│  │  ├─ Category breakdown (%, pages)                             │ │
│  │  └─ Evidence with citations                                   │ │
│  │                                                                │ │
│  │  Stage 2: Safety Check                                        │ │
│  │  ├─ Child safety violations                                   │ │
│  │  ├─ Hate speech detection                                     │ │
│  │  ├─ Violent content                                           │ │
│  │  └─ Flag unsafe content                                       │ │
│  │                                                                │ │
│  │  Stage 3: PII Detection (if has_text)                         │ │
│  │  ├─ SSN, credit cards, IDs                                    │ │
│  │  ├─ Names + addresses                                         │ │
│  │  ├─ Contact information                                       │ │
│  │  └─ Upgrade to highly_sensitive                               │ │
│  │                                                                │ │
│  │  Stage 4: Proprietary Detection (if has_images)               │ │
│  │  ├─ Technical schematics                                      │ │
│  │  ├─ Product designs                                           │ │
│  │  ├─ Military equipment                                        │ │
│  │  └─ Upgrade to confidential                                   │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │              Result Aggregation                                │ │
│  │                                                                │ │
│  │  • Priority-based category selection                          │ │
│  │  • Evidence consolidation                                     │ │
│  │  • Confidence scoring                                         │ │
│  │  • Mixed content detection                                    │ │
│  │  • Category breakdown calculation                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │         Dual-LLM Verification (Optional)                       │ │
│  │                                                                │ │
│  │  Primary Model: GPT-4o                                        │ │
│  │  ├─ Full analysis with images                                 │ │
│  │  └─ Primary classification                                    │ │
│  │                                                                │ │
│  │  Verification Model: GPT-4o-mini                              │ │
│  │  ├─ Independent second opinion                                │ │
│  │  ├─ Text-only (cost optimization)                             │ │
│  │  └─ Verification classification                               │ │
│  │                                                                │ │
│  │  Agreement Check:                                             │ │
│  │  ├─ Match → Auto-classify                                     │ │
│  │  └─ Mismatch → Flag for HITL                                  │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                  HUMAN-IN-THE-LOOP (HITL)                            │
├─────────────────────────────────────────────────────────────────────┤
│                    HITLManager (hitl_manager.py)                     │
│                                                                       │
│  Auto-flagging Triggers:                                             │
│  ├─ Confidence < 70%                                                 │
│  ├─ Dual-LLM disagreement                                            │
│  ├─ Unsafe content detected                                          │
│  └─ Multiple sensitive elements                                      │
│                                                                       │
│  Feedback Loop:                                                      │
│  ├─ Human corrections                                                │
│  ├─ Agreement rate tracking                                          │
│  ├─ Training data extraction                                         │
│  └─ Prompt refinement                                                │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    METRICS & MONITORING                              │
├─────────────────────────────────────────────────────────────────────┤
│                 MetricsTracker (metrics_tracker.py)                  │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Accuracy   │  │  Throughput  │  │    Safety    │             │
│  │              │  │              │  │              │             │
│  │ • Precision  │  │ • Docs/min   │  │ • Safe count │             │
│  │ • Recall     │  │ • Avg time   │  │ • Unsafe %   │             │
│  │ • F1 score   │  │ • Total time │  │ • Validation │             │
│  │ • By category│  │              │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐                                │
│  │  Confidence  │  │     HITL     │                                │
│  │              │  │              │                                │
│  │ • Average    │  │ • Auto-class │                                │
│  │ • Min/Max    │  │ • Needs rev  │                                │
│  │ • By test    │  │ • Time saved │                                │
│  └──────────────┘  └──────────────┘                                │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA STORAGE                                    │
├─────────────────────────────────────────────────────────────────────┤
│  • Classification results (JSON)                                     │
│  • HITL feedback (hitl_feedback.json)                                │
│  • Batch job status (in-memory)                                      │
│  • Uploaded documents (test_documents/)                              │
│  • Metrics history (session state)                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interfaces

#### Streamlit UI (`demo_ui.py`)
- **Purpose**: Interactive web interface for document classification
- **Features**:
  - File upload (PDF, images)
  - Test case selection (TC1-TC5)
  - Real-time classification
  - Evidence display with citations
  - Category breakdown visualization
  - Dual-LLM verification status
  - Metrics dashboard
  - File management
- **Port**: 8501 (default)

#### Flask API (`app.py`)
- **Purpose**: REST API for programmatic access
- **Endpoints**:
  - `/classify` - Single document classification
  - `/batch` - Batch job creation
  - `/status/<job_id>` - Job status query
  - `/results/<job_id>` - Job results retrieval
- **Port**: 5000 (default)

### 2. Processing Layer

#### Batch Processor (`batch_processor.py`)
- **Purpose**: Asynchronous batch processing
- **Features**:
  - Background threading
  - Job queue management
  - Real-time progress tracking
  - Error handling per document
  - Results export to JSON
  - HITL integration

#### Single Document Processor
- **Purpose**: Real-time interactive classification
- **Flow**: Upload → Preprocess → Classify → Display

### 3. Document Preprocessing (`preprocessor.py`)

#### Validation
- File existence check
- File size limits (50MB default)
- File type validation (PDF, PNG, JPG, TIFF, BMP)
- Page count limits (1000 pages max)

#### Content Extraction
- **PDF Processing**:
  - Text extraction via PyPDF2
  - Page-to-image conversion via pdf2image
  - Image extraction (up to 10 pages)
- **Image Processing**:
  - Quality assessment (Laplacian variance)
  - OCR text extraction via Tesseract
  - Format conversion

#### Output Format
```python
{
  'text': 'Extracted text content...',
  'images': [
    {'page': 1, 'data': bytes},
    {'page': 2, 'data': bytes}
  ],
  'metadata': {
    'type': 'pdf',
    'page_count': 4,
    'image_count': 3,
    'has_text': True,
    'is_legible': True
  }
}
```

### 4. Classification Engine (`classifier.py`)

#### Multi-Stage Pipeline

**Stage 1: Base Classification**
- Analyzes full document (text + images)
- Generates category breakdown (% and pages)
- Provides evidence with citations
- Calculates confidence score

**Stage 2: Safety Check**
- Scans for unsafe content
- Detects hate speech, violence
- Flags child safety violations
- Overrides to "unsafe" if found

**Stage 3: PII Detection** (if document has text)
- Identifies SSN, credit cards, IDs
- Detects names + addresses
- Finds contact information
- Upgrades to "highly_sensitive"

**Stage 4: Proprietary Detection** (if document has images)
- Identifies technical schematics
- Detects product designs
- Finds military equipment
- Upgrades to "confidential"

#### Result Aggregation
- Priority order: unsafe > highly_sensitive > confidential > public
- Evidence consolidation from all stages
- Confidence scoring
- Mixed content detection
- Category breakdown calculation

#### Dual-LLM Verification (Optional)
- **Primary Model**: GPT-4o (full analysis)
- **Verification Model**: GPT-4o-mini (second opinion)
- **Agreement Check**: Match → auto-classify, Mismatch → flag for HITL
- **Cost**: ~50% increase (verification uses cheaper model)
- **Time**: ~2x processing time

### 5. Prompt Library (`prompt_library.py`)

#### Dynamic Prompt Tree
- Builds prompts based on document characteristics
- Configurable classification rules
- Policy-aware reasoning
- Citation requirements

#### Prompt Types
1. **Base Classification**: Full document analysis
2. **PII Detection**: Specific PII scanning
3. **Safety Check**: Content safety validation
4. **Proprietary Detection**: Technical content identification
5. **Verification**: Second-opinion classification

### 6. HITL Manager (`hitl_manager.py`)

#### Auto-flagging Logic
```python
Flag for review if:
- Confidence < 70%
- Dual-LLM disagreement
- Unsafe content detected
- Multiple sensitive elements (>2)
```

#### Feedback Loop
- Human corrections storage
- Agreement rate tracking
- Disagreement analysis
- Training data extraction
- Prompt refinement suggestions

### 7. Metrics Tracker (`metrics_tracker.py`)

#### Tracked Metrics
- **Accuracy**: Precision, recall, F1 score by category
- **Confidence**: Average, min, max per test
- **Throughput**: Docs/min, avg time, total time
- **Safety**: Safe count, unsafe percentage
- **HITL**: Auto-classified, needs review, time saved

#### Report Generation
```python
{
  'model_info': {...},
  'accuracy': 0.95,
  'precision_recall': {...},
  'confidence': {...},
  'throughput': {...},
  'review_metrics': {...},
  'safety_validation': {...}
}
```

## Data Flow

### Single Document Classification

```
1. User uploads document
   ↓
2. Preprocessor validates and extracts content
   ↓
3. Classifier runs multi-stage pipeline
   ├─ Base classification
   ├─ Safety check
   ├─ PII detection
   └─ Proprietary detection
   ↓
4. Results aggregated with priority logic
   ↓
5. [Optional] Dual-LLM verification
   ↓
6. HITL manager checks flagging criteria
   ↓
7. Metrics tracker records results
   ↓
8. UI displays classification + evidence
```

### Batch Processing

```
1. User submits batch job (multiple files)
   ↓
2. Batch processor creates job with unique ID
   ↓
3. Background thread processes each file:
   ├─ Preprocess
   ├─ Classify
   ├─ Check HITL
   └─ Store result
   ↓
4. Real-time status updates available
   ↓
5. Job completes with all results
   ↓
6. Results exportable to JSON
```

## Classification Categories

### Priority Order (Highest to Lowest)
1. **Unsafe** - Violates safety policies
2. **Highly Sensitive** - Contains PII or critical data
3. **Confidential** - Internal/proprietary content
4. **Public** - Publicly available content

### Category Breakdown
Every document gets a breakdown showing:
- Percentage of each category (0-100%)
- Page count per category
- Reason for each category presence

Example:
```python
{
  'primary_category': 'highly_sensitive',
  'category_breakdown': {
    'highly_sensitive': {
      'percentage': 75,
      'page_count': 3,
      'reason': 'Contains PII (SSN, address, phone)'
    },
    'public': {
      'percentage': 25,
      'page_count': 1,
      'reason': 'General employment information'
    },
    'confidential': {'percentage': 0, 'page_count': 0},
    'unsafe': {'percentage': 0, 'page_count': 0}
  }
}
```

## External Dependencies

### AI/ML Services
- **OpenRouter API**: Primary LLM provider
  - GPT-4o: Primary classification model
  - GPT-4o-mini: Verification model (optional)

### Python Libraries
- **Document Processing**: PyPDF2, pdf2image, Pillow
- **OCR**: pytesseract, opencv-python
- **Web Frameworks**: Streamlit, Flask
- **API Client**: openai (OpenRouter-compatible)
- **Utilities**: python-dotenv, numpy

### System Requirements
- **Poppler**: PDF rendering (for pdf2image)
- **Tesseract**: OCR engine
- **Python**: 3.8+

## Configuration

### Environment Variables (`.env`)
```bash
# API Keys
OPENROUTER_API_KEY=sk-or-v1-...

# Application Settings
FLASK_ENV=development
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=50000000

# Dual-LLM Verification
ENABLE_DUAL_LLM=false
VERIFICATION_MODEL=openai/gpt-4o-mini
```

### Config Class (`config.py`)
- Loads environment variables
- Defines constants and limits
- Manages feature flags
- Provides category mappings

## Security Considerations

### Input Validation
- File size limits (50MB default)
- File type whitelist
- Page count limits (1000 pages)
- Image count limits (500 images)

### Data Handling
- Temporary file storage
- Automatic cleanup
- No persistent storage of sensitive content
- API key protection

### API Security
- Rate limiting (via OpenRouter)
- Error handling without data leakage
- Secure credential management

## Performance Characteristics

### Single Document
- **Processing Time**: 8-10 seconds (single-LLM)
- **Processing Time**: 15-20 seconds (dual-LLM)
- **Cost**: ~$0.01 per document (single-LLM)
- **Cost**: ~$0.015 per document (dual-LLM)

### Batch Processing
- **Throughput**: 6-8 docs/minute (single-LLM)
- **Throughput**: 3-4 docs/minute (dual-LLM)
- **Scalability**: Linear with threading

### Accuracy
- **Single-LLM**: ~95% accuracy
- **Dual-LLM**: ~98% accuracy
- **HITL Review Rate**: 5-10% (dual-LLM), 15-20% (single-LLM)

## Deployment Options

### Local Development
```bash
# Streamlit UI
streamlit run demo_ui.py

# Flask API
python app.py
```

### Production Deployment
- Docker containerization
- Cloud hosting (AWS, GCP, Azure)
- Load balancing for API
- Database for persistent storage
- Queue system for batch processing

## Testing

### Test Cases (TC1-TC5)
- TC1: Public marketing document
- TC2: Employment application (PII)
- TC3: Internal memo
- TC4: Technical manual
- TC5: Mixed content

### Test Scripts
- `test_dual_llm.py` - Dual-LLM verification
- `test_mixed_content.py` - Mixed content handling
- `run_test_cases.py` - All test cases
- `final_comprehensive_test.py` - Evidence validation

## Monitoring & Observability

### Metrics Dashboard
- Real-time accuracy tracking
- Confidence score monitoring
- Throughput measurement
- HITL queue status
- Cost tracking

### Logging
- Classification decisions
- Error tracking
- Performance metrics
- API usage

## Future Enhancements

### Planned Features
- Video input support
- Multi-language support
- Custom category definitions
- Advanced redaction tools
- Audit trail export

### Optimization Opportunities
- Caching for repeated documents
- Parallel image processing
- Model fine-tuning
- Cost optimization strategies

---

**Architecture Version**: 2.0
**Last Updated**: November 8, 2025
**Feature Completion**: 11/12 (92%)

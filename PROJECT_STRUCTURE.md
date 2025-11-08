# Project Structure

```
ai-document-classifier/
│
├── app.py                      # Flask web application (main entry point)
├── config.py                   # Configuration and settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your API keys (create this, not in git)
├── run.sh                     # Quick start script
│
├── Core Components/
│   ├── preprocessor.py        # Document preprocessing and validation
│   ├── classifier.py          # AI classification engine
│   ├── prompt_library.py      # Configurable prompt templates
│   ├── hitl_manager.py        # Human-in-the-Loop feedback system
│   └── batch_processor.py     # Batch processing with real-time updates
│
├── Web Interface/
│   ├── templates/
│   │   └── index.html         # Main UI template
│   └── static/
│       ├── style.css          # Styling
│       └── script.js          # Frontend logic
│
├── Documentation/
│   ├── README.md              # Project overview
│   ├── IMPLEMENTATION_GUIDE.md # Setup and deployment guide
│   ├── TEST_CASES.md          # Test case specifications
│   └── PROJECT_STRUCTURE.md   # This file
│
├── Testing/
│   └── test_system.py         # System test suite
│
├── Data Directories/
│   ├── uploads/               # Uploaded documents (created at runtime)
│   ├── test_documents/        # Test case documents
│   └── hitl_feedback.json     # HITL feedback storage (created at runtime)
│
└── .gitignore                 # Git ignore rules
```

## Component Details

### Core Components

#### preprocessor.py
- File validation and format checking
- Page and image counting
- Text extraction (OCR for images)
- Legibility assessment using computer vision
- Content extraction for LLM analysis

#### classifier.py
- Multi-stage classification pipeline
- OpenAI GPT-4 Vision integration
- Anthropic Claude integration (optional)
- Dynamic prompt tree execution
- Result aggregation and prioritization
- Dual-LLM verification support

#### prompt_library.py
- Base classification prompts
- PII detection prompts
- Safety check prompts
- Proprietary content detection prompts
- Verification prompts for dual-LLM
- Dynamic prompt tree builder

#### hitl_manager.py
- Feedback collection and storage
- Agreement rate tracking
- Statistics calculation
- Review flagging logic
- Training data generation

#### batch_processor.py
- Asynchronous batch processing
- Thread-safe job management
- Real-time status updates
- Progress tracking
- Result aggregation and export

### Web Application

#### app.py
- Flask REST API endpoints
- File upload handling
- Interactive classification
- Batch job management
- Feedback submission
- Statistics dashboard

#### templates/index.html
- Responsive web interface
- Tab-based navigation
- Drag-and-drop file upload
- Real-time progress visualization
- Results display with evidence
- Feedback form
- Statistics dashboard

#### static/style.css
- Modern, gradient-based design
- Responsive layout
- Category-specific color coding
- Confidence badge styling
- Progress bar animations

#### static/script.js
- File upload handling
- API communication
- Real-time batch monitoring
- Results rendering
- Feedback submission
- Statistics visualization

## Data Flow

### Interactive Mode
```
User Upload → Preprocessor → Classifier → HITL Check → Display Results
                                              ↓
                                         Feedback Loop
```

### Batch Mode
```
Multiple Files → Batch Processor → [For Each File]
                                        ↓
                                   Preprocessor → Classifier → HITL Check
                                        ↓
                                   Aggregate Results → Display Progress
```

### HITL Feedback Loop
```
Classification Result → HITL Manager → Check Thresholds
                            ↓
                    Flag for Review (if needed)
                            ↓
                    Human Feedback → Store → Update Statistics
                            ↓
                    Training Data Generation
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serve web interface |
| `/api/classify` | POST | Classify single document |
| `/api/batch` | POST | Create batch job |
| `/api/batch/<id>/status` | GET | Get batch status |
| `/api/batch/<id>/results` | GET | Get batch results |
| `/api/feedback` | POST | Submit HITL feedback |
| `/api/statistics` | GET | Get HITL statistics |

## Configuration

### Environment Variables (.env)
- `OPENAI_API_KEY`: OpenAI API key (required)
- `ANTHROPIC_API_KEY`: Anthropic API key (optional)
- `FLASK_ENV`: development/production
- `UPLOAD_FOLDER`: Upload directory path
- `MAX_FILE_SIZE`: Maximum file size in bytes
- `ENABLE_DUAL_LLM`: Enable dual-LLM verification

### Config.py Settings
- `CATEGORIES`: Classification categories
- `ALLOWED_EXTENSIONS`: Supported file types
- `MIN_IMAGE_QUALITY`: Minimum image quality threshold
- `MAX_PAGES`: Maximum pages per document
- `MAX_IMAGES`: Maximum images per document

## Security Features

1. **File Validation**: Type and size checking
2. **Secure Filenames**: Werkzeug secure_filename
3. **API Key Protection**: Environment variables
4. **CORS Configuration**: Controlled cross-origin access
5. **Upload Limits**: Configurable size restrictions

## Extensibility

### Adding New Classification Categories
1. Update `config.py` CATEGORIES
2. Modify `prompt_library.py` prompts
3. Update `classifier.py` aggregation logic
4. Add CSS styling in `style.css`

### Adding New Prompt Stages
1. Create new prompt method in `prompt_library.py`
2. Add stage to `build_dynamic_prompt_tree()`
3. Update `_aggregate_results()` in `classifier.py`

### Custom HITL Logic
1. Modify `should_flag_for_review()` in `hitl_manager.py`
2. Add custom thresholds
3. Implement custom review criteria

## Performance Considerations

- **Async Processing**: Batch jobs run in background threads
- **Image Limits**: First 10 pages converted for analysis
- **Text Truncation**: 10,000 character limit per analysis
- **Caching**: Consider adding Redis for production
- **Rate Limiting**: Implement for production deployment

## Deployment Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Configure production WSGI server
- [ ] Set up reverse proxy (nginx)
- [ ] Enable SSL/TLS
- [ ] Implement rate limiting
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Backup HITL feedback data
- [ ] Implement authentication
- [ ] Review security settings

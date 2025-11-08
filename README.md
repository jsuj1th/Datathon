# AI-Powered Document Classification System

Multi-modal document analyzer that classifies documents into Public, Confidential, Highly Sensitive, or Unsafe categories with citation-based evidence.

## Features

- Multi-modal input support (text, images, PDFs)
- Pre-processing checks (legibility, page/image counts)
- Dynamic prompt tree generation
- Citation-based evidence with page/image references
- HITL feedback loop for continuous improvement
- Batch and interactive processing modes
- Real-time status updates
- Safety content monitoring
- Optional dual-LLM verification
- Business-friendly UI with visualizations

## Categories

- **Highly Sensitive**: PII (SSNs, account numbers), proprietary schematics
- **Confidential**: Internal communications, customer details, non-public operations
- **Public**: Marketing materials, public website content
- **Unsafe**: Child safety violations, hate speech, violent/criminal content

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Access the UI at http://localhost:5000

## Test Cases

The system includes 5 comprehensive test cases:

1. **TC1**: Public Marketing Document (Hitachi EverFlex brochure) - Expected: Public
2. **TC2**: Employment Application with PII - Expected: Highly Sensitive
3. **TC3**: Internal Research Memo - Expected: Confidential
4. **TC4**: Flight Operations Manual (18 pages) - Expected: Confidential
5. **TC5**: Mixed Content Document - Expected: Unsafe/Multiple Categories

Run all test cases:
```bash
python run_test_cases.py
```

This will generate a detailed report with evidence citations for each classification.

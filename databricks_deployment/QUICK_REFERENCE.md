# Databricks Deployment - Quick Reference

## One-Time Setup (5 minutes)

```bash
# 1. Install CLI
pip install databricks-cli

# 2. Configure
databricks configure --token
# Enter: https://<workspace>.cloud.databricks.com
# Enter: <your-token>

# 3. Upload files
cd databricks_deployment
./upload_to_databricks.sh

# 4. Set up secrets
databricks secrets create-scope --scope document-classifier
databricks secrets put --scope document-classifier --key openrouter-api-key
# Paste your OpenRouter API key when prompted
```

## Daily Usage

### Upload Documents

```bash
# Upload a single document
databricks fs cp document.pdf dbfs:/FileStore/documents/input/

# Upload multiple documents
databricks fs cp *.pdf dbfs:/FileStore/documents/input/
```

### Run Classification

**Option 1: Interactive Notebook**
1. Open `databricks_interactive_notebook` in Databricks
2. Run all cells
3. View results inline

**Option 2: Batch Job**
1. Go to Workflows → Jobs → Document Classification Batch
2. Click "Run Now"
3. Check results in `/FileStore/documents/output/`

### View Results

```bash
# List results
databricks fs ls dbfs:/FileStore/documents/output/

# Download result
databricks fs cp dbfs:/FileStore/documents/output/results.json ./
```

## Common Commands

```bash
# List files
databricks fs ls dbfs:/FileStore/documents/input/

# Upload file
databricks fs cp local.pdf dbfs:/FileStore/documents/input/

# Download file
databricks fs cp dbfs:/FileStore/documents/output/results.json ./

# Delete file
databricks fs rm dbfs:/FileStore/documents/input/old.pdf

# View file content
databricks fs cat dbfs:/FileStore/documents/output/results.json
```

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | Add `sys.path.append('/dbfs/FileStore/document_classifier/')` |
| API key error | Run `databricks secrets put --scope document-classifier --key openrouter-api-key` |
| File not found | Run `./upload_to_databricks.sh` again |
| Import error | Run `%pip install openai PyPDF2 pdf2image` in notebook |

## File Paths

| Purpose | Path |
|---------|------|
| Python modules | `/FileStore/document_classifier/` |
| Input documents | `/FileStore/documents/input/` |
| Output results | `/FileStore/documents/output/` |
| Test documents | `/FileStore/documents/test_documents/` |

## Job Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| input_path | `/FileStore/documents/input/` | Where to find PDFs |
| output_path | `/FileStore/documents/output/` | Where to save results |
| enable_dual_llm | `false` | Enable dual-LLM verification |

## Quick Test

```python
# In Databricks notebook
import sys
sys.path.append('/dbfs/FileStore/document_classifier/')

from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier

preprocessor = DocumentPreprocessor()
classifier = DocumentClassifier()

# Test with a document
filepath = "/dbfs/FileStore/documents/test_documents/TC1_Sample_Public_Marketing_Document.pdf"
preprocess_result = preprocessor.check_file_validity(filepath)
metadata = preprocess_result['metadata']
content = preprocessor.extract_content_for_analysis(filepath, metadata)
classification = classifier.classify_document(content, metadata)

print(f"✓ Category: {classification['category']}")
print(f"✓ Confidence: {classification['confidence']:.0%}")
```

## Support

- Full guide: `README_DATABRICKS.md`
- Detailed deployment: `DATABRICKS_DEPLOYMENT.md`
- Interactive notebook: `databricks_interactive_notebook.py`
- Batch job: `databricks_batch_job.py`

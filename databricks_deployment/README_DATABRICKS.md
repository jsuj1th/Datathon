# Databricks Deployment Guide

## Quick Start

Follow these steps to deploy the AI Document Classification System to Databricks.

## Prerequisites

1. **Databricks Workspace** - Access to a Databricks workspace
2. **Databricks CLI** - Install with: `pip install databricks-cli`
3. **OpenRouter API Key** - Get from https://openrouter.ai/

## Deployment Steps

### Step 1: Install Databricks CLI

```bash
pip install databricks-cli
```

### Step 2: Configure Databricks CLI

```bash
databricks configure --token
```

You'll be prompted for:
- **Databricks Host**: `https://<your-workspace>.cloud.databricks.com`
- **Token**: Generate from User Settings → Access Tokens

### Step 3: Upload Files to Databricks

```bash
cd databricks_deployment
./upload_to_databricks.sh
```

This will:
- Create necessary DBFS directories
- Upload all Python files
- Upload test documents
- Upload Databricks scripts

### Step 4: Set Up Secrets

```bash
# Create secrets scope
databricks secrets create-scope --scope document-classifier

# Add your OpenRouter API key
databricks secrets put --scope document-classifier --key openrouter-api-key
```

When prompted, paste your OpenRouter API key.

### Step 5: Import Notebooks

1. Go to your Databricks Workspace
2. Click **Workspace** → **Users** → **Your Name**
3. Click **Import**
4. Select **File** and upload:
   - `databricks_interactive_notebook.py`
   - `databricks_batch_job.py`

### Step 6: Test the System

1. Open `databricks_interactive_notebook` in Databricks
2. Run all cells
3. Verify the system works correctly

## Usage Options

### Option A: Interactive Notebook

Use `databricks_interactive_notebook` for:
- Testing and development
- Classifying individual documents
- Exploring results interactively

**How to use:**
1. Open the notebook
2. Run cells sequentially
3. Modify document paths as needed
4. View results inline

### Option B: Batch Job

Use `databricks_batch_job` for:
- Scheduled batch processing
- Processing large volumes
- Automated workflows

**How to create a job:**

1. Go to **Workflows** → **Jobs** → **Create Job**
2. Configure:
   - **Name**: Document Classification Batch
   - **Task Type**: Notebook
   - **Notebook Path**: `/Users/<your-email>/databricks_batch_job`
   - **Cluster**: Select or create cluster
3. Add parameters:
   - `input_path`: `/FileStore/documents/input/`
   - `output_path`: `/FileStore/documents/output/`
   - `enable_dual_llm`: `false` (or `true` for higher accuracy)
4. Set schedule (optional)
5. Click **Create**

### Option C: Databricks Apps (Streamlit UI)

**Requirements**: Databricks ML Runtime 13.0+

1. Create app directory with required files
2. Upload `demo_ui.py` and dependencies
3. Deploy as Databricks App
4. Access via web URL

See `DATABRICKS_DEPLOYMENT.md` for detailed instructions.

## File Structure on DBFS

```
/FileStore/
├── document_classifier/
│   ├── config.py
│   ├── preprocessor.py
│   ├── classifier.py
│   ├── prompt_library.py
│   ├── hitl_manager.py
│   ├── metrics_tracker.py
│   ├── batch_processor.py
│   └── databricks_batch_job.py
│
└── documents/
    ├── input/          # Upload PDFs here
    ├── output/         # Results saved here
    └── test_documents/ # Test PDFs
```

## Uploading Documents

### Via Databricks UI

1. Go to **Data** → **DBFS**
2. Navigate to `/FileStore/documents/input/`
3. Click **Upload**
4. Select PDF files

### Via CLI

```bash
databricks fs cp local_file.pdf dbfs:/FileStore/documents/input/
```

### Via Notebook

```python
# Upload from local file
dbutils.fs.cp("file:/path/to/local/file.pdf", "/FileStore/documents/input/file.pdf")
```

## Running Classifications

### Interactive (Notebook)

```python
# In databricks_interactive_notebook
document_path = "/dbfs/FileStore/documents/input/sample.pdf"

# Run classification cells
# Results displayed inline
```

### Batch (Job)

1. Upload PDFs to `/FileStore/documents/input/`
2. Run the job (manually or scheduled)
3. Check results in `/FileStore/documents/output/`

### Programmatic (API)

```python
import sys
sys.path.append('/dbfs/FileStore/document_classifier/')

from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier

preprocessor = DocumentPreprocessor()
classifier = DocumentClassifier()

# Classify
filepath = "/dbfs/FileStore/documents/input/sample.pdf"
preprocess_result = preprocessor.check_file_validity(filepath)
metadata = preprocess_result['metadata']
content = preprocessor.extract_content_for_analysis(filepath, metadata)
classification = classifier.classify_document(content, metadata)

print(f"Category: {classification['category']}")
```

## Viewing Results

### From Notebook

Results are displayed inline in the notebook.

### From DBFS

```bash
# List results
databricks fs ls dbfs:/FileStore/documents/output/

# Download result
databricks fs cp dbfs:/FileStore/documents/output/results.json ./results.json
```

### From Delta Lake (if saved)

```python
# Read from Delta
df = spark.read.format("delta").load("/FileStore/delta/classification_results")
display(df)
```

## Monitoring

### Job Runs

1. Go to **Workflows** → **Jobs**
2. Click on your job
3. View **Runs** tab
4. Check logs and outputs

### Cluster Metrics

1. Go to **Compute** → **Clusters**
2. Click on your cluster
3. View **Metrics** tab

## Troubleshooting

### "Module not found" Error

```python
# Add path in notebook
import sys
sys.path.append('/dbfs/FileStore/document_classifier/')
```

### "API key not configured" Error

```bash
# Verify secret exists
databricks secrets list --scope document-classifier

# Re-add if needed
databricks secrets put --scope document-classifier --key openrouter-api-key
```

### "File not found" Error

```bash
# Check if files exist
databricks fs ls dbfs:/FileStore/document_classifier/

# Re-upload if needed
./upload_to_databricks.sh
```

### Import Errors

```python
# In notebook, install dependencies
%pip install openai PyPDF2 pdf2image pytesseract opencv-python pillow
dbutils.library.restartPython()
```

## Cost Optimization

1. **Use Job Clusters**: Auto-terminate after job completion
2. **Enable Auto-scaling**: Scale down when idle
3. **Use Spot Instances**: For non-critical workloads
4. **Disable Dual-LLM**: Unless high accuracy is critical
5. **Batch Processing**: Process multiple documents together

## Security Best Practices

1. **Use Secrets**: Never hardcode API keys
2. **Access Control**: Use Unity Catalog for permissions
3. **Audit Logging**: Enable workspace audit logs
4. **Network Security**: Use private endpoints if available
5. **Data Encryption**: Enable encryption at rest and in transit

## Next Steps

1. ✅ Deploy to Databricks
2. ✅ Test with sample documents
3. ✅ Set up batch job for production
4. ✅ Configure monitoring and alerts
5. ✅ Train users on the system

## Support

For issues or questions:
1. Check `DATABRICKS_DEPLOYMENT.md` for detailed documentation
2. Review Databricks logs for error messages
3. Verify all files are uploaded correctly
4. Ensure API key is configured in secrets

## Summary

You now have:
- ✅ All files uploaded to DBFS
- ✅ Secrets configured
- ✅ Interactive notebook for testing
- ✅ Batch job for production
- ✅ Complete deployment guide

Your AI Document Classification System is ready to use on Databricks! 🚀

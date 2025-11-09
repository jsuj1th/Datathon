# Deploying to Databricks

## Overview

Yes, this AI Document Classification System can be deployed to Databricks! Here are multiple deployment options:

## Deployment Options

### Option 1: Databricks Notebook (Recommended for Testing)
Run the system directly in Databricks notebooks for interactive use.

### Option 2: Databricks Jobs (Recommended for Batch Processing)
Schedule batch classification jobs to run on a schedule.

### Option 3: Databricks Apps (Recommended for Production UI)
Deploy the Streamlit UI as a Databricks App (requires Databricks ML Runtime).

### Option 4: MLflow Model Serving
Deploy the classifier as an MLflow model endpoint for REST API access.

---

## Option 1: Databricks Notebook Deployment

### Step 1: Upload Files to DBFS

```python
# In a Databricks notebook
# Upload your files to DBFS
dbutils.fs.mkdirs("/FileStore/document_classifier/")

# Upload Python files
dbutils.fs.put("/FileStore/document_classifier/config.py", """
# Paste config.py content here
""", overwrite=True)

# Repeat for all Python files:
# - preprocessor.py
# - classifier.py
# - prompt_library.py
# - hitl_manager.py
# - metrics_tracker.py
# - batch_processor.py
```

### Step 2: Install Dependencies

```python
# In a Databricks notebook cell
%pip install openai python-dotenv PyPDF2 pdf2image pytesseract opencv-python pillow streamlit

# Restart Python kernel
dbutils.library.restartPython()
```

### Step 3: Set Environment Variables

```python
# In a Databricks notebook
import os
os.environ['OPENROUTER_API_KEY'] = 'your-api-key-here'
```

Or use Databricks Secrets:

```python
# Store secret
dbutils.secrets.put(scope="document-classifier", key="openrouter-api-key", string_value="your-key")

# Retrieve secret
api_key = dbutils.secrets.get(scope="document-classifier", key="openrouter-api-key")
os.environ['OPENROUTER_API_KEY'] = api_key
```

### Step 4: Import and Use

```python
# In a Databricks notebook
import sys
sys.path.append('/dbfs/FileStore/document_classifier/')

from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier

# Use the system
preprocessor = DocumentPreprocessor()
classifier = DocumentClassifier()

# Classify a document
filepath = "/dbfs/FileStore/documents/sample.pdf"
preprocess_result = preprocessor.check_file_validity(filepath)
metadata = preprocess_result['metadata']
content = preprocessor.extract_content_for_analysis(filepath, metadata)
classification = classifier.classify_document(content, metadata)

print(f"Category: {classification['category']}")
print(f"Confidence: {classification['confidence']:.2%}")
```

---

## Option 2: Databricks Jobs (Batch Processing)

### Step 1: Create a Job Script

Create `databricks_job.py`:

```python
"""
Databricks Job for Batch Document Classification
"""

import os
import sys
import json
from datetime import datetime

# Add module path
sys.path.append('/dbfs/FileStore/document_classifier/')

from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from batch_processor import BatchProcessor

def main():
    # Get parameters from job
    input_path = dbutils.widgets.get("input_path")
    output_path = dbutils.widgets.get("output_path")
    
    print(f"Processing documents from: {input_path}")
    print(f"Output will be saved to: {output_path}")
    
    # Get list of files
    files = dbutils.fs.ls(input_path)
    pdf_files = [f.path for f in files if f.path.endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDF files")
    
    # Initialize processor
    batch_processor = BatchProcessor()
    
    # Create batch job
    job_id = batch_processor.create_batch_job(pdf_files)
    
    # Wait for completion
    import time
    while True:
        status = batch_processor.get_job_status(job_id)
        if status['status'] == 'completed':
            break
        print(f"Progress: {status['progress_percent']:.1f}%")
        time.sleep(5)
    
    # Export results
    results = batch_processor.get_job_results(job_id)
    
    # Save to DBFS
    output_file = f"{output_path}/results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    dbutils.fs.put(output_file, json.dumps(results, indent=2), overwrite=True)
    
    print(f"Results saved to: {output_file}")
    print(f"Processed: {status['processed_files']}")
    print(f"Failed: {status['failed_files']}")

if __name__ == '__main__':
    main()
```

### Step 2: Create Databricks Job

1. Go to Databricks Workspace → Jobs → Create Job
2. Configure:
   - **Name**: Document Classification Batch Job
   - **Task Type**: Python Script
   - **Script Path**: `/dbfs/FileStore/document_classifier/databricks_job.py`
   - **Cluster**: Select or create cluster
   - **Parameters**:
     - `input_path`: `/FileStore/documents/input/`
     - `output_path`: `/FileStore/documents/output/`
3. Schedule (optional): Set cron schedule for recurring jobs

---

## Option 3: Databricks Apps (Streamlit UI)

### Requirements
- Databricks ML Runtime 13.0+
- Databricks Apps feature enabled

### Step 1: Create App Directory

```bash
# In your local environment
mkdir databricks_app
cd databricks_app

# Copy essential files
cp config.py preprocessor.py classifier.py prompt_library.py \
   hitl_manager.py metrics_tracker.py demo_ui.py requirements.txt \
   databricks_app/
```

### Step 2: Create Databricks App Configuration

Create `databricks_app.yaml`:

```yaml
name: document-classifier
display_name: AI Document Classification System
description: Multi-modal document classification with dual-LLM verification

runtime:
  python_version: "3.10"
  
dependencies:
  - openai
  - python-dotenv
  - PyPDF2
  - pdf2image
  - pytesseract
  - opencv-python
  - pillow
  - streamlit
  - numpy

environment:
  OPENROUTER_API_KEY: "{{secrets/document-classifier/openrouter-api-key}}"

entrypoint: streamlit run demo_ui.py --server.port 8501
```

### Step 3: Deploy App

```bash
# Using Databricks CLI
databricks apps create --source-dir ./databricks_app

# Or via UI
# 1. Go to Databricks Workspace → Apps
# 2. Click "Create App"
# 3. Upload your app directory
# 4. Configure settings
# 5. Deploy
```

### Step 4: Access App

Once deployed, you'll get a URL like:
```
https://<workspace>.cloud.databricks.com/apps/<app-id>
```

---

## Option 4: MLflow Model Serving

### Step 1: Create MLflow Model Wrapper

Create `mlflow_model.py`:

```python
"""
MLflow Model Wrapper for Document Classifier
"""

import mlflow
import pandas as pd
from typing import Dict, Any

class DocumentClassifierModel(mlflow.pyfunc.PythonModel):
    
    def load_context(self, context):
        """Load model dependencies"""
        import sys
        sys.path.append(context.artifacts["model_path"])
        
        from preprocessor import DocumentPreprocessor
        from classifier import DocumentClassifier
        
        self.preprocessor = DocumentPreprocessor()
        self.classifier = DocumentClassifier()
    
    def predict(self, context, model_input):
        """
        Predict document classification
        
        Input: DataFrame with 'file_path' column
        Output: DataFrame with classification results
        """
        results = []
        
        for filepath in model_input['file_path']:
            # Preprocess
            preprocess_result = self.preprocessor.check_file_validity(filepath)
            
            if not preprocess_result['valid']:
                results.append({
                    'file': filepath,
                    'category': 'error',
                    'confidence': 0.0,
                    'error': str(preprocess_result['errors'])
                })
                continue
            
            # Extract and classify
            metadata = preprocess_result['metadata']
            content = self.preprocessor.extract_content_for_analysis(filepath, metadata)
            classification = self.classifier.classify_document(content, metadata)
            
            results.append({
                'file': filepath,
                'category': classification['category'],
                'confidence': classification['confidence'],
                'evidence_count': len(classification.get('evidence', [])),
                'safety_check': classification.get('safety_check', True)
            })
        
        return pd.DataFrame(results)

# Register model
with mlflow.start_run():
    model = DocumentClassifierModel()
    
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=model,
        artifacts={
            "model_path": "/dbfs/FileStore/document_classifier/"
        },
        conda_env={
            "channels": ["defaults"],
            "dependencies": [
                "python=3.10",
                "pip",
                {
                    "pip": [
                        "openai",
                        "PyPDF2",
                        "pdf2image",
                        "pytesseract",
                        "opencv-python",
                        "pillow",
                        "python-dotenv"
                    ]
                }
            ],
            "name": "document_classifier_env"
        }
    )
    
    # Register to Model Registry
    model_uri = f"runs:/{mlflow.active_run().info.run_id}/model"
    mlflow.register_model(model_uri, "document_classifier")
```

### Step 2: Deploy Model Endpoint

```python
# In Databricks notebook
from mlflow.deployments import get_deploy_client

client = get_deploy_client("databricks")

# Deploy model
endpoint_name = "document-classifier-endpoint"
client.create_endpoint(
    name=endpoint_name,
    config={
        "served_models": [{
            "model_name": "document_classifier",
            "model_version": "1",
            "workload_size": "Small",
            "scale_to_zero_enabled": True
        }]
    }
)
```

### Step 3: Call Endpoint

```python
# REST API call
import requests
import json

url = f"https://<workspace>.cloud.databricks.com/serving-endpoints/{endpoint_name}/invocations"
headers = {
    "Authorization": f"Bearer {databricks_token}",
    "Content-Type": "application/json"
}

data = {
    "dataframe_records": [
        {"file_path": "/dbfs/FileStore/documents/sample.pdf"}
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

---

## Architecture on Databricks

```
┌─────────────────────────────────────────────────────────────┐
│                    Databricks Workspace                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  DBFS (Databricks File System)                      │   │
│  │  ├─ /FileStore/document_classifier/                 │   │
│  │  │  ├─ config.py                                    │   │
│  │  │  ├─ preprocessor.py                              │   │
│  │  │  ├─ classifier.py                                │   │
│  │  │  └─ ... (other Python files)                     │   │
│  │  │                                                    │   │
│  │  ├─ /FileStore/documents/                           │   │
│  │  │  ├─ input/ (PDFs to classify)                    │   │
│  │  │  └─ output/ (classification results)             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Databricks Secrets                                  │   │
│  │  └─ document-classifier/openrouter-api-key          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Compute Options                                     │   │
│  │  ├─ Interactive Notebooks                           │   │
│  │  ├─ Scheduled Jobs                                  │   │
│  │  ├─ Databricks Apps (Streamlit)                     │   │
│  │  └─ Model Serving Endpoints                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  MLflow                                              │   │
│  │  ├─ Model Registry                                  │   │
│  │  ├─ Experiment Tracking                             │   │
│  │  └─ Model Serving                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    External Services
                    ├─ OpenRouter API
                    └─ LLM Models (GPT-4o)
```

---

## Considerations for Databricks

### 1. File Storage
- Use DBFS for storing documents and results
- Consider Delta Lake for structured results storage
- Use Unity Catalog for data governance

### 2. Compute Resources
- **Interactive**: Use standard clusters for development
- **Batch Jobs**: Use job clusters (auto-terminate)
- **Apps**: Use serverless compute (if available)
- **Model Serving**: Use model serving endpoints

### 3. Security
- Store API keys in Databricks Secrets
- Use Unity Catalog for access control
- Enable audit logging
- Use private endpoints for sensitive data

### 4. Scalability
- Batch processing can handle 1000s of documents
- Use Spark for massive parallel processing
- Scale model serving endpoints based on load

### 5. Cost Optimization
- Use spot instances for batch jobs
- Enable auto-scaling
- Set auto-termination for clusters
- Use serverless compute when possible

---

## Spark Integration (Optional)

For processing large volumes of documents in parallel:

```python
# Create Spark UDF for classification
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

def classify_document_udf(file_path):
    """Spark UDF for document classification"""
    from preprocessor import DocumentPreprocessor
    from classifier import DocumentClassifier
    
    preprocessor = DocumentPreprocessor()
    classifier = DocumentClassifier()
    
    preprocess_result = preprocessor.check_file_validity(file_path)
    if not preprocess_result['valid']:
        return ('error', 0.0, str(preprocess_result['errors']))
    
    metadata = preprocess_result['metadata']
    content = preprocessor.extract_content_for_analysis(file_path, metadata)
    classification = classifier.classify_document(content, metadata)
    
    return (
        classification['category'],
        classification['confidence'],
        str(classification.get('evidence', []))
    )

# Register UDF
schema = StructType([
    StructField("category", StringType()),
    StructField("confidence", DoubleType()),
    StructField("evidence", StringType())
])

classify_udf = udf(classify_document_udf, schema)

# Use with Spark DataFrame
df = spark.createDataFrame([
    ("/dbfs/FileStore/documents/doc1.pdf",),
    ("/dbfs/FileStore/documents/doc2.pdf",),
], ["file_path"])

results_df = df.withColumn("classification", classify_udf("file_path"))
results_df.write.format("delta").save("/FileStore/classification_results/")
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] Test locally with `python quick_test.py`
- [ ] Verify all dependencies in requirements.txt
- [ ] Set up Databricks Secrets for API keys
- [ ] Upload test documents to DBFS

### Deployment
- [ ] Upload Python files to DBFS
- [ ] Install dependencies on cluster
- [ ] Configure environment variables
- [ ] Test with sample document
- [ ] Set up monitoring and logging

### Post-Deployment
- [ ] Monitor API usage and costs
- [ ] Set up alerts for failures
- [ ] Document access procedures
- [ ] Train users on the system

---

## Recommended Approach

**For Your Use Case:**

1. **Start with Option 1 (Notebooks)** - Quick testing and validation
2. **Move to Option 2 (Jobs)** - Production batch processing
3. **Add Option 3 (Apps)** - If you need a UI for end users
4. **Consider Option 4 (MLflow)** - If you need REST API access

**Best Practice:**
- Use Databricks Jobs for scheduled batch processing
- Use Databricks Apps for interactive UI
- Store results in Delta Lake for analytics
- Use Unity Catalog for governance

---

## Summary

✅ **Yes, you can deploy to Databricks!**

**Recommended Setup:**
- Databricks Jobs for batch processing
- Databricks Apps for Streamlit UI
- DBFS for file storage
- Databricks Secrets for API keys
- Delta Lake for results storage

**Benefits:**
- Scalable compute
- Integrated with data lakehouse
- Built-in security and governance
- Easy scheduling and monitoring
- Cost-effective with auto-scaling

Would you like me to create specific deployment scripts for any of these options?

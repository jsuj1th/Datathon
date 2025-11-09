# Setup for Databricks with Unity Catalog (DBFS Root Disabled)

## Your Error: "Public DBFS root is disabled"

This means your workspace uses **Unity Catalog** for better security. We'll use **Workspace Files** instead of DBFS.

---

## Quick Setup (Using Workspace Files)

### Step 1: Upload Python Files via UI

1. **Go to Workspace**
   - Click **Workspace** in left sidebar
   - Navigate to your user folder

2. **Create Folder**
   - Click the **⋮** (three dots) next to your name
   - Select **Create** → **Folder**
   - Name it: `document_classifier`

3. **Upload Python Files**
   - Click the **⋮** next to `document_classifier` folder
   - Select **Import**
   - Upload these files one by one:
     - `config.py`
     - `preprocessor.py`
     - `classifier.py`
     - `prompt_library.py`
     - `hitl_manager.py`
     - `metrics_tracker.py`
     - `batch_processor.py`

### Step 2: Create Volumes for Documents (Unity Catalog Way)

In a new notebook, run:

```python
# Cell 1: Create catalog and schema (if not exists)
spark.sql("CREATE CATALOG IF NOT EXISTS main")
spark.sql("CREATE SCHEMA IF NOT EXISTS main.document_classifier")

# Cell 2: Create volumes for file storage
spark.sql("""
CREATE VOLUME IF NOT EXISTS main.document_classifier.input_documents
""")

spark.sql("""
CREATE VOLUME IF NOT EXISTS main.document_classifier.output_results
""")

spark.sql("""
CREATE VOLUME IF NOT EXISTS main.document_classifier.test_documents
""")

print("✓ Volumes created successfully")
```

### Step 3: Upload Documents

```python
# Cell 3: Upload a test document
# You can upload files via UI or use this code

# Via UI:
# 1. Go to Catalog → main → document_classifier → input_documents
# 2. Click "Upload" and select your PDF

# Via code (if you have file in workspace):
dbutils.fs.cp(
    "file:/Workspace/Users/your-email@example.com/sample.pdf",
    "/Volumes/main/document_classifier/input_documents/sample.pdf"
)
```

### Step 4: Set Up Secrets

```python
# Cell 4: Set up secrets (run this once)
# Note: You'll need to use Databricks CLI or UI for secrets

# Via UI:
# 1. Settings → Developer → Secrets
# 2. Create scope: document-classifier
# 3. Add secret: openrouter-api-key
```

### Step 5: Install Packages and Import

```python
# Cell 5: Install packages
%pip install openai python-dotenv PyPDF2 pdf2image pytesseract opencv-python pillow numpy

dbutils.library.restartPython()
```

```python
# Cell 6: Import modules from workspace
import sys
import os

# Add workspace path
workspace_path = "/Workspace/Users/your-email@example.com/document_classifier"
sys.path.append(workspace_path)

# Set API key from secrets
api_key = dbutils.secrets.get(scope="document-classifier", key="openrouter-api-key")
os.environ['OPENROUTER_API_KEY'] = api_key

# Import modules
from config import Config
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier

print("✓ Modules imported successfully")
```

### Step 6: Test Classification

```python
# Cell 7: Classify a document
preprocessor = DocumentPreprocessor()
classifier = DocumentClassifier()

# Path to document in Unity Catalog volume
document_path = "/Volumes/main/document_classifier/input_documents/sample.pdf"

# Preprocess
preprocess_result = preprocessor.check_file_validity(document_path)

if preprocess_result['valid']:
    metadata = preprocess_result['metadata']
    print(f"✓ Document validated: {metadata['page_count']} pages")
    
    # Extract content
    content = preprocessor.extract_content_for_analysis(document_path, metadata)
    
    # Classify
    classification = classifier.classify_document(content, metadata)
    
    print(f"\nCategory: {classification['category'].upper()}")
    print(f"Confidence: {classification['confidence']:.2%}")
else:
    print(f"❌ Validation failed: {preprocess_result['errors']}")
```

---

## Alternative: Use Repos (Git Integration)

This is the **BEST** approach for Unity Catalog workspaces:

### Step 1: Push Code to GitHub (Already Done!)

Your code is already on GitHub at:
```
https://github.com/jsuj1th/Datathon/tree/production_clean
```

### Step 2: Connect Databricks to GitHub

1. **Go to Repos**
   - Click **Repos** in left sidebar
   - Click **Add Repo**

2. **Configure Git**
   - **Git repository URL**: `https://github.com/jsuj1th/Datathon.git`
   - **Git provider**: GitHub
   - **Repository name**: `Datathon`
   - **Branch**: `production_clean`
   - Click **Create Repo**

3. **Access Your Code**
   - Your code is now at: `/Workspace/Repos/your-email/Datathon/`
   - All Python files are automatically available!

### Step 3: Use Code from Repo

```python
# Cell 1: Install packages
%pip install openai python-dotenv PyPDF2 pdf2image pytesseract opencv-python pillow numpy
dbutils.library.restartPython()
```

```python
# Cell 2: Import from repo
import sys
import os

# Add repo path
sys.path.append("/Workspace/Repos/your-email@example.com/Datathon")

# Set API key
api_key = dbutils.secrets.get(scope="document-classifier", key="openrouter-api-key")
os.environ['OPENROUTER_API_KEY'] = api_key

# Import modules
from config import Config
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier

print("✓ Modules imported from Git repo")
```

```python
# Cell 3: Create volumes for documents
spark.sql("CREATE CATALOG IF NOT EXISTS main")
spark.sql("CREATE SCHEMA IF NOT EXISTS main.document_classifier")
spark.sql("CREATE VOLUME IF NOT EXISTS main.document_classifier.input_documents")
spark.sql("CREATE VOLUME IF NOT EXISTS main.document_classifier.output_results")

print("✓ Volumes created")
```

```python
# Cell 4: Test classification
preprocessor = DocumentPreprocessor()
classifier = DocumentClassifier()

# Upload a document via UI to: Catalog → main → document_classifier → input_documents
# Then use it:
document_path = "/Volumes/main/document_classifier/input_documents/your-document.pdf"

preprocess_result = preprocessor.check_file_validity(document_path)
if preprocess_result['valid']:
    metadata = preprocess_result['metadata']
    content = preprocessor.extract_content_for_analysis(document_path, metadata)
    classification = classifier.classify_document(content, metadata)
    
    print(f"Category: {classification['category'].upper()}")
    print(f"Confidence: {classification['confidence']:.2%}")
```

---

## Path Comparison

| Old (DBFS) | New (Unity Catalog) |
|------------|---------------------|
| `/FileStore/document_classifier/` | `/Workspace/Users/you/document_classifier/` or `/Workspace/Repos/you/Datathon/` |
| `/FileStore/documents/input/` | `/Volumes/main/document_classifier/input_documents/` |
| `/FileStore/documents/output/` | `/Volumes/main/document_classifier/output_results/` |

---

## Recommended Approach

**Use Git Repos** (Option 2) because:
- ✅ Code is version controlled
- ✅ Easy to update (just git pull)
- ✅ Works with Unity Catalog
- ✅ No manual file uploads
- ✅ Your code is already on GitHub!

---

## Quick Start with Repos

1. **Add Repo in Databricks**
   - Repos → Add Repo
   - URL: `https://github.com/jsuj1th/Datathon.git`
   - Branch: `production_clean`

2. **Create Notebook**
   - Create → Notebook
   - Name: `document_classifier_test`

3. **Run This Code**:

```python
# Install packages
%pip install openai python-dotenv PyPDF2 pdf2image pytesseract opencv-python pillow numpy
dbutils.library.restartPython()
```

```python
# Import from repo
import sys, os
sys.path.append("/Workspace/Repos/<your-email>/Datathon")

# Set API key (create secret first via UI)
os.environ['OPENROUTER_API_KEY'] = dbutils.secrets.get("document-classifier", "openrouter-api-key")

from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier

print("✓ Ready to classify!")
```

```python
# Create volumes
spark.sql("CREATE CATALOG IF NOT EXISTS main")
spark.sql("CREATE SCHEMA IF NOT EXISTS main.document_classifier")
spark.sql("CREATE VOLUME IF NOT EXISTS main.document_classifier.input_documents")
print("✓ Upload PDFs to: Catalog → main → document_classifier → input_documents")
```

---

## Summary

**Your workspace has Unity Catalog enabled (more secure).**

**Best solution**: Use **Git Repos** integration
1. Connect your GitHub repo to Databricks
2. Code is automatically available
3. Use Unity Catalog Volumes for documents
4. No DBFS needed!

This is actually **better** than the old DBFS approach! 🎉

# Simple Setup - Upload Files via Databricks UI

## Easiest Method (No CLI, No Git)

### Step 1: Create Folder in Workspace (2 minutes)

1. **Go to Workspace**
   - Click **Workspace** in left sidebar
   - Click **Users**
   - Click your email/username

2. **Create Folder**
   - Click the **⋮** (three dots) next to your name
   - Select **Create** → **Folder**
   - Name it: `document_classifier`
   - Press Enter

### Step 2: Upload Python Files (5 minutes)

For each of these files, do the following:

**Files to upload:**
- config.py
- preprocessor.py
- classifier.py
- prompt_library.py
- hitl_manager.py
- metrics_tracker.py
- batch_processor.py

**How to upload each file:**

1. Click the **⋮** next to `document_classifier` folder
2. Select **Import**
3. Click **File**
4. Browse to the file on your computer (they're in `/Users/cherukupallimaitreya/new_hitachi/`)
5. Click **Import**
6. Repeat for all 7 files

### Step 3: Create Storage for Documents (2 minutes)

1. **Create a new Notebook**
   - Click **Create** → **Notebook**
   - Name: `setup_storage`
   - Click **Create**

2. **Run this code** (copy and paste into notebook):

```python
# Cell 1: Create catalog and schema
spark.sql("CREATE CATALOG IF NOT EXISTS main")
spark.sql("CREATE SCHEMA IF NOT EXISTS main.document_classifier")
print("✓ Catalog and schema created")
```

```python
# Cell 2: Create volumes for file storage
spark.sql("""
CREATE VOLUME IF NOT EXISTS main.document_classifier.input_documents
""")

spark.sql("""
CREATE VOLUME IF NOT EXISTS main.document_classifier.output_results
""")

print("✓ Volumes created")
print("\nYou can now upload PDFs to:")
print("Catalog → main → document_classifier → input_documents")
```

3. **Run both cells** (click the play button or press Shift+Enter)

### Step 4: Set Up API Key Secret (3 minutes)

1. **Go to Settings**
   - Click your username (top right)
   - Select **User Settings**

2. **Go to Developer Tab**
   - Click **Developer** (or **Access Tokens**)
   - Look for **Secrets** section

3. **Create Secret Scope**
   - Click **Manage** next to Secrets
   - Click **Create Scope**
   - Scope name: `document-classifier`
   - Click **Create**

4. **Add Secret**
   - In the scope `document-classifier`
   - Click **Add Secret**
   - Key: `openrouter-api-key`
   - Value: (paste your OpenRouter API key)
   - Click **Add**

### Step 5: Create Classification Notebook (5 minutes)

1. **Create new Notebook**
   - Click **Create** → **Notebook**
   - Name: `classify_documents`
   - Click **Create**

2. **Copy this code into the notebook:**

```python
# Cell 1: Install required packages
%pip install openai python-dotenv PyPDF2 pdf2image pytesseract opencv-python pillow numpy

# Restart Python to load new packages
dbutils.library.restartPython()
```

```python
# Cell 2: Import modules and set up
import sys
import os

# Add your workspace path (CHANGE THIS to your email!)
workspace_path = "/Workspace/Users/your-email@example.com/document_classifier"
sys.path.append(workspace_path)

# Get API key from secrets
api_key = dbutils.secrets.get(scope="document-classifier", key="openrouter-api-key")
os.environ['OPENROUTER_API_KEY'] = api_key

# Import classification modules
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier

print("✓ Setup complete!")
print("✓ Modules imported successfully")
```

```python
# Cell 3: Initialize classifier
preprocessor = DocumentPreprocessor()
classifier = DocumentClassifier()

print("✓ Classifier ready!")
```

```python
# Cell 4: Classify a document
# First, upload a PDF via: Catalog → main → document_classifier → input_documents

# Path to your document (change filename as needed)
document_path = "/Volumes/main/document_classifier/input_documents/your-document.pdf"

print(f"Classifying: {document_path}")
print("="*70)

# Preprocess
print("\n1. Pre-processing...")
preprocess_result = preprocessor.check_file_validity(document_path)

if not preprocess_result['valid']:
    print(f"❌ Validation failed: {preprocess_result['errors']}")
else:
    metadata = preprocess_result['metadata']
    print(f"✓ Document validated")
    print(f"  - Pages: {metadata.get('page_count')}")
    print(f"  - Images: {metadata.get('image_count')}")
    
    # Extract content
    print("\n2. Extracting content...")
    content = preprocessor.extract_content_for_analysis(document_path, metadata)
    print(f"✓ Content extracted")
    
    # Classify
    print("\n3. Classifying...")
    classification = classifier.classify_document(content, metadata)
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"\nCategory: {classification['category'].upper()}")
    print(f"Confidence: {classification['confidence']:.2%}")
    print(f"Safety: {'✓ Safe' if classification.get('safety_check', True) else '⚠️ Unsafe'}")
    
    # Category breakdown
    if classification.get('category_breakdown'):
        print("\nCategory Breakdown:")
        for cat, data in classification['category_breakdown'].items():
            if data.get('percentage', 0) > 0:
                print(f"  {cat.replace('_', ' ').title()}: {data['percentage']}%")
```

### Step 6: Upload a Test Document (2 minutes)

1. **Go to Catalog**
   - Click **Catalog** in left sidebar
   - Navigate to: **main** → **document_classifier** → **input_documents**

2. **Upload PDF**
   - Click **Upload** button
   - Select a PDF file from your computer
   - Click **Upload**

### Step 7: Run Classification (1 minute)

1. **Go back to your notebook** (`classify_documents`)

2. **Update the document path** in Cell 4:
   ```python
   document_path = "/Volumes/main/document_classifier/input_documents/YOUR-FILE-NAME.pdf"
   ```

3. **Run all cells** (click **Run All** at the top)

4. **View results!**

---

## Important: Update Your Email in Cell 2!

In Cell 2 of the classification notebook, change this line:

```python
workspace_path = "/Workspace/Users/your-email@example.com/document_classifier"
```

To your actual email, for example:
```python
workspace_path = "/Workspace/Users/maitreya@example.com/document_classifier"
```

To find your exact path:
1. Go to Workspace → Users
2. Look at your folder name
3. Copy that exact path

---

## Troubleshooting

### "Module not found" error

Make sure the workspace path is correct:
```python
# Check if files exist
dbutils.fs.ls("/Workspace/Users/your-email@example.com/document_classifier")
```

You should see all 7 Python files listed.

### "API key not configured" error

```python
# Test if secret exists
try:
    key = dbutils.secrets.get("document-classifier", "openrouter-api-key")
    print("✓ Secret found")
except:
    print("❌ Secret not found - please create it")
```

### "File not found" error

```python
# List files in volume
dbutils.fs.ls("/Volumes/main/document_classifier/input_documents/")
```

Make sure your PDF is uploaded and the filename matches.

---

## Summary

You should now have:
- ✅ Python files uploaded to Workspace
- ✅ Storage volumes created
- ✅ API key stored as secret
- ✅ Classification notebook ready
- ✅ Test document uploaded
- ✅ System working!

**No CLI needed, no Git needed - everything through the UI!** 🎉

---

## Next Steps

Once this works, you can:

1. **Upload more documents** to the input_documents volume
2. **Process multiple documents** by modifying Cell 4
3. **Save results** to the output_results volume
4. **Create a job** to run classifications on a schedule

For batch processing, see `databricks_batch_job.py` (upload it as a notebook the same way).

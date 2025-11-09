"""
Databricks Setup Script
Run this in a Databricks notebook to set up the document classification system
"""

# DATABRICKS NOTEBOOK
# Cell 1: Install Dependencies
%pip install openai python-dotenv PyPDF2 pdf2image pytesseract opencv-python pillow streamlit numpy

# Restart Python to load new packages
dbutils.library.restartPython()

# Cell 2: Create Directory Structure
dbutils.fs.mkdirs("/FileStore/document_classifier/")
dbutils.fs.mkdirs("/FileStore/documents/input/")
dbutils.fs.mkdirs("/FileStore/documents/output/")
dbutils.fs.mkdirs("/FileStore/documents/test_documents/")

print("✓ Directory structure created")

# Cell 3: Upload Python Files
# You'll need to upload these files manually or use the code below

import base64

def upload_file_to_dbfs(local_path, dbfs_path):
    """Upload a file to DBFS"""
    with open(local_path, 'r') as f:
        content = f.read()
    dbutils.fs.put(dbfs_path, content, overwrite=True)
    print(f"✓ Uploaded {local_path} to {dbfs_path}")

# Upload core files (run this from your local machine with Databricks Connect)
files_to_upload = [
    'config.py',
    'preprocessor.py',
    'classifier.py',
    'prompt_library.py',
    'hitl_manager.py',
    'metrics_tracker.py',
    'batch_processor.py',
    'demo_ui.py'
]

for filename in files_to_upload:
    try:
        upload_file_to_dbfs(
            f'./{filename}',
            f'/FileStore/document_classifier/{filename}'
        )
    except Exception as e:
        print(f"⚠️  Could not upload {filename}: {e}")
        print(f"   Please upload manually via Databricks UI")

# Cell 4: Set Up Secrets
print("""
To set up secrets, run these commands in your terminal:

databricks secrets create-scope --scope document-classifier
databricks secrets put --scope document-classifier --key openrouter-api-key

Or use the Databricks UI:
1. Go to Settings → Secrets
2. Create scope: document-classifier
3. Add secret: openrouter-api-key
""")

# Cell 5: Test Installation
import sys
sys.path.append('/dbfs/FileStore/document_classifier/')

try:
    from config import Config
    from preprocessor import DocumentPreprocessor
    from classifier import DocumentClassifier
    
    print("✓ All modules imported successfully")
    print("✓ System is ready to use!")
except Exception as e:
    print(f"❌ Import error: {e}")
    print("Please check that all files are uploaded correctly")

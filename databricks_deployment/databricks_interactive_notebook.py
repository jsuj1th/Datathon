"""
Databricks Interactive Notebook for Document Classification
Copy this into a Databricks notebook for interactive use
"""

# Databricks notebook source
# MAGIC %md
# MAGIC # AI Document Classification System
# MAGIC 
# MAGIC Interactive notebook for classifying documents using multi-modal AI

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Setup and Installation

# COMMAND ----------
# Install required packages
%pip install openai python-dotenv PyPDF2 pdf2image pytesseract opencv-python pillow numpy

# Restart Python
dbutils.library.restartPython()

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Import Modules

# COMMAND ----------
import os
import sys
import json
from datetime import datetime

# Add module path
sys.path.append('/dbfs/FileStore/document_classifier/')

# Import classification modules
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from config import Config

print("✓ Modules imported successfully")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Configure API Key

# COMMAND ----------
# Load API key from Databricks Secrets
try:
    api_key = dbutils.secrets.get(scope="document-classifier", key="openrouter-api-key")
    os.environ['OPENROUTER_API_KEY'] = api_key
    print("✓ API key loaded from secrets")
except Exception as e:
    print(f"⚠️  Could not load from secrets: {e}")
    print("Please enter API key manually:")
    # Uncomment to enter manually (not recommended for production)
    # api_key = dbutils.widgets.text("api_key", "", "OpenRouter API Key")
    # os.environ['OPENROUTER_API_KEY'] = dbutils.widgets.get("api_key")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Initialize Components

# COMMAND ----------
# Initialize preprocessor and classifier
preprocessor = DocumentPreprocessor()
classifier = DocumentClassifier()

print("✓ Classification system initialized")
print(f"  - Dual-LLM enabled: {Config.ENABLE_DUAL_LLM}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. List Available Documents

# COMMAND ----------
# List documents in DBFS
input_path = "/FileStore/documents/input/"

try:
    files = dbutils.fs.ls(input_path)
    pdf_files = [f for f in files if f.path.endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDF files:")
    for i, f in enumerate(pdf_files, 1):
        print(f"  {i}. {f.name} ({f.size / 1024:.1f} KB)")
except Exception as e:
    print(f"⚠️  Could not list files: {e}")
    print(f"Make sure documents are uploaded to: {input_path}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Classify a Single Document

# COMMAND ----------
# Select a document to classify
document_path = "/dbfs/FileStore/documents/input/sample.pdf"  # Change this

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
    print(f"  - Type: {metadata.get('type')}")
    print(f"  - Pages: {metadata.get('page_count')}")
    print(f"  - Images: {metadata.get('image_count')}")
    print(f"  - Has text: {metadata.get('has_text')}")
    
    # Extract content
    print("\n2. Extracting content...")
    content = preprocessor.extract_content_for_analysis(document_path, metadata)
    print(f"✓ Content extracted")
    print(f"  - Text: {len(content.get('text', ''))} characters")
    print(f"  - Images: {len(content.get('images', []))} images")
    
    # Classify
    print("\n3. Classifying...")
    classification = classifier.classify_document(content, metadata)
    
    # Display results
    print("\n" + "="*70)
    print("CLASSIFICATION RESULTS")
    print("="*70)
    print(f"\nCategory: {classification['category'].upper()}")
    print(f"Confidence: {classification['confidence']:.2%}")
    print(f"Safety Check: {'✓ Safe' if classification.get('safety_check', True) else '⚠️ Unsafe'}")
    
    # Category breakdown
    if classification.get('category_breakdown'):
        print("\nCategory Breakdown:")
        for cat, data in classification['category_breakdown'].items():
            if data.get('percentage', 0) > 0:
                print(f"  {cat.replace('_', ' ').title()}: {data['percentage']}%")
                if data.get('reason'):
                    print(f"    → {data['reason']}")
    
    # Evidence
    if classification.get('evidence'):
        print(f"\nEvidence ({len(classification['evidence'])} items):")
        for i, evidence in enumerate(classification['evidence'][:3], 1):
            print(f"  {i}. {evidence.get('finding', 'N/A')[:100]}...")
    
    # Dual-LLM verification
    if classification.get('dual_llm_enabled') and 'verification' in classification:
        verification = classification['verification']
        print("\nDual-LLM Verification:")
        if verification.get('agreement'):
            print(f"  ✓ Agreement: Both LLMs classified as {classification['category'].upper()}")
        else:
            print(f"  ⚠️ Disagreement:")
            print(f"    Primary: {verification.get('primary_category', 'unknown').upper()}")
            print(f"    Verification: {verification.get('verification_category', 'unknown').upper()}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 7. Batch Classification

# COMMAND ----------
# Classify multiple documents
input_path = "/FileStore/documents/input/"
output_path = "/FileStore/documents/output/"

# Get list of files
files = dbutils.fs.ls(input_path)
pdf_files = [f.path for f in files if f.path.endswith('.pdf')]

print(f"Processing {len(pdf_files)} documents...")
print()

results = []

for i, filepath in enumerate(pdf_files, 1):
    filename = os.path.basename(filepath)
    print(f"[{i}/{len(pdf_files)}] {filename}...", end=" ")
    
    try:
        local_path = filepath.replace('dbfs:', '/dbfs')
        
        # Preprocess and classify
        preprocess_result = preprocessor.check_file_validity(local_path)
        if not preprocess_result['valid']:
            print("❌ Invalid")
            results.append({'file': filename, 'status': 'failed'})
            continue
        
        metadata = preprocess_result['metadata']
        content = preprocessor.extract_content_for_analysis(local_path, metadata)
        classification = classifier.classify_document(content, metadata)
        
        print(f"✓ {classification['category'].upper()} ({classification['confidence']:.0%})")
        
        results.append({
            'file': filename,
            'status': 'success',
            'category': classification['category'],
            'confidence': classification['confidence']
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)[:50]}")
        results.append({'file': filename, 'status': 'failed', 'error': str(e)})

# Save results
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f"{output_path}/batch_results_{timestamp}.json"
dbutils.fs.put(output_file, json.dumps(results, indent=2), overwrite=True)

print(f"\n✓ Results saved to: {output_file}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 8. View Results Summary

# COMMAND ----------
# Display summary
import pandas as pd

# Convert results to DataFrame
df = pd.DataFrame(results)

print("BATCH CLASSIFICATION SUMMARY")
print("="*70)
print(f"Total files: {len(results)}")
print(f"Successful: {len(df[df['status'] == 'success'])}")
print(f"Failed: {len(df[df['status'] == 'failed'])}")
print()

if len(df[df['status'] == 'success']) > 0:
    print("Category Distribution:")
    category_counts = df[df['status'] == 'success']['category'].value_counts()
    for cat, count in category_counts.items():
        print(f"  {cat.upper()}: {count}")

# Display as table
display(df)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 9. Export to Delta Lake (Optional)

# COMMAND ----------
# Save results to Delta Lake for analytics
from pyspark.sql import SparkSession

# Convert to Spark DataFrame
spark_df = spark.createDataFrame(results)

# Save to Delta
delta_path = "/FileStore/delta/classification_results"
spark_df.write.format("delta").mode("append").save(delta_path)

print(f"✓ Results saved to Delta Lake: {delta_path}")

# Query results
print("\nRecent classifications:")
recent_df = spark.read.format("delta").load(delta_path).limit(10)
display(recent_df)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 10. Cleanup (Optional)

# COMMAND ----------
# Clear processed files from input folder (optional)
# Uncomment to enable

# for f in pdf_files:
#     dbutils.fs.rm(f)
# print("✓ Input files cleared")

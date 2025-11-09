"""
Databricks Batch Job for Document Classification
Upload this to DBFS and run as a Databricks Job
"""

# Databricks notebook source
import os
import sys
import json
from datetime import datetime

# Add module path
sys.path.append('/dbfs/FileStore/document_classifier/')

# Import modules
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier

# COMMAND ----------
# Cell 1: Setup and Configuration

# Get job parameters
dbutils.widgets.text("input_path", "/FileStore/documents/input/", "Input Path")
dbutils.widgets.text("output_path", "/FileStore/documents/output/", "Output Path")
dbutils.widgets.dropdown("enable_dual_llm", "false", ["true", "false"], "Enable Dual-LLM")

input_path = dbutils.widgets.get("input_path")
output_path = dbutils.widgets.get("output_path")
enable_dual_llm = dbutils.widgets.get("enable_dual_llm") == "true"

print("="*70)
print("DATABRICKS BATCH DOCUMENT CLASSIFICATION")
print("="*70)
print(f"Input Path: {input_path}")
print(f"Output Path: {output_path}")
print(f"Dual-LLM: {enable_dual_llm}")
print()

# COMMAND ----------
# Cell 2: Get API Key from Secrets

try:
    api_key = dbutils.secrets.get(scope="document-classifier", key="openrouter-api-key")
    os.environ['OPENROUTER_API_KEY'] = api_key
    print("✓ API key loaded from secrets")
except Exception as e:
    print(f"❌ Could not load API key: {e}")
    print("Please set up Databricks secrets:")
    print("  databricks secrets put --scope document-classifier --key openrouter-api-key")
    dbutils.notebook.exit("API key not configured")

# COMMAND ----------
# Cell 3: Get List of Files

try:
    files = dbutils.fs.ls(input_path)
    pdf_files = [f.path for f in files if f.path.endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDF files to process")
    for i, f in enumerate(pdf_files[:5], 1):
        print(f"  {i}. {os.path.basename(f)}")
    if len(pdf_files) > 5:
        print(f"  ... and {len(pdf_files) - 5} more")
    print()
    
    if len(pdf_files) == 0:
        print("❌ No PDF files found in input path")
        dbutils.notebook.exit("No files to process")
        
except Exception as e:
    print(f"❌ Error listing files: {e}")
    dbutils.notebook.exit("Could not list input files")

# COMMAND ----------
# Cell 4: Initialize Components

print("Initializing classification components...")
preprocessor = DocumentPreprocessor()
classifier = DocumentClassifier()
print("✓ Components initialized")
print()

# COMMAND ----------
# Cell 5: Process Documents

results = []
processed = 0
failed = 0

print("="*70)
print("PROCESSING DOCUMENTS")
print("="*70)
print()

for idx, filepath in enumerate(pdf_files, 1):
    filename = os.path.basename(filepath)
    print(f"[{idx}/{len(pdf_files)}] Processing: {filename}")
    
    try:
        # Convert DBFS path to local path
        local_path = filepath.replace('dbfs:', '/dbfs')
        
        # Preprocess
        preprocess_result = preprocessor.check_file_validity(local_path)
        
        if not preprocess_result['valid']:
            print(f"  ❌ Validation failed: {preprocess_result['errors']}")
            results.append({
                'file': filename,
                'status': 'failed',
                'error': str(preprocess_result['errors']),
                'timestamp': datetime.now().isoformat()
            })
            failed += 1
            continue
        
        metadata = preprocess_result['metadata']
        print(f"  ✓ Validated: {metadata.get('page_count')} pages, {metadata.get('image_count')} images")
        
        # Extract content
        content = preprocessor.extract_content_for_analysis(local_path, metadata)
        
        # Classify
        classification = classifier.classify_document(
            content, 
            metadata,
            enable_dual_llm=enable_dual_llm
        )
        
        print(f"  ✓ Classified as: {classification['category'].upper()} ({classification['confidence']:.0%})")
        
        # Store result
        result = {
            'file': filename,
            'status': 'success',
            'category': classification['category'],
            'confidence': classification['confidence'],
            'page_count': metadata.get('page_count'),
            'image_count': metadata.get('image_count'),
            'evidence_count': len(classification.get('evidence', [])),
            'safety_check': classification.get('safety_check', True),
            'dual_llm_enabled': classification.get('dual_llm_enabled', False),
            'category_breakdown': classification.get('category_breakdown', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add verification info if dual-LLM was used
        if classification.get('dual_llm_enabled') and 'verification' in classification:
            verification = classification['verification']
            result['verification'] = {
                'agreement': verification.get('agreement'),
                'primary_category': verification.get('primary_category'),
                'verification_category': verification.get('verification_category')
            }
        
        results.append(result)
        processed += 1
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        results.append({
            'file': filename,
            'status': 'failed',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })
        failed += 1
    
    print()

# COMMAND ----------
# Cell 6: Save Results

print("="*70)
print("SAVING RESULTS")
print("="*70)
print()

# Create output filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_filename = f"classification_results_{timestamp}.json"
output_file = f"{output_path}/{output_filename}"

# Prepare summary
summary = {
    'job_info': {
        'timestamp': datetime.now().isoformat(),
        'input_path': input_path,
        'output_path': output_path,
        'dual_llm_enabled': enable_dual_llm
    },
    'statistics': {
        'total_files': len(pdf_files),
        'processed': processed,
        'failed': failed,
        'success_rate': f"{(processed/len(pdf_files)*100):.1f}%" if len(pdf_files) > 0 else "0%"
    },
    'results': results
}

# Save to DBFS
try:
    dbutils.fs.put(
        output_file.replace('dbfs:', ''),
        json.dumps(summary, indent=2),
        overwrite=True
    )
    print(f"✓ Results saved to: {output_file}")
except Exception as e:
    print(f"❌ Could not save results: {e}")

# COMMAND ----------
# Cell 7: Display Summary

print()
print("="*70)
print("JOB SUMMARY")
print("="*70)
print()
print(f"Total Files: {len(pdf_files)}")
print(f"Processed: {processed}")
print(f"Failed: {failed}")
print(f"Success Rate: {(processed/len(pdf_files)*100):.1f}%")
print()

# Category breakdown
if processed > 0:
    print("Classification Breakdown:")
    categories = {}
    for result in results:
        if result['status'] == 'success':
            cat = result['category']
            categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items()):
        percentage = (count / processed) * 100
        print(f"  {cat.upper()}: {count} ({percentage:.1f}%)")

print()
print(f"Results saved to: {output_file}")
print()
print("="*70)

# Return summary for job monitoring
dbutils.notebook.exit(json.dumps({
    'status': 'completed',
    'processed': processed,
    'failed': failed,
    'output_file': output_file
}))

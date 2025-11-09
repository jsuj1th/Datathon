#!/bin/bash

# Upload to Databricks Script
# This script uploads all necessary files to Databricks DBFS

echo "=========================================="
echo "Uploading to Databricks"
echo "=========================================="
echo ""

# Check if databricks CLI is installed
if ! command -v databricks &> /dev/null; then
    echo "❌ Databricks CLI not found"
    echo "Install it with: pip install databricks-cli"
    echo "Then configure: databricks configure --token"
    exit 1
fi

echo "✓ Databricks CLI found"
echo ""

# Create directories
echo "Creating DBFS directories..."
databricks fs mkdirs dbfs:/FileStore/document_classifier/
databricks fs mkdirs dbfs:/FileStore/documents/input/
databricks fs mkdirs dbfs:/FileStore/documents/output/
databricks fs mkdirs dbfs:/FileStore/documents/test_documents/
echo "✓ Directories created"
echo ""

# Upload Python files
echo "Uploading Python files..."
files=(
    "config.py"
    "preprocessor.py"
    "classifier.py"
    "prompt_library.py"
    "hitl_manager.py"
    "metrics_tracker.py"
    "batch_processor.py"
)

for file in "${files[@]}"; do
    if [ -f "../$file" ]; then
        echo "  Uploading $file..."
        databricks fs cp "../$file" "dbfs:/FileStore/document_classifier/$file" --overwrite
    else
        echo "  ⚠️  $file not found, skipping"
    fi
done

echo "✓ Python files uploaded"
echo ""

# Upload test documents
echo "Uploading test documents..."
if [ -d "../test_documents" ]; then
    for pdf in ../test_documents/*.pdf; do
        if [ -f "$pdf" ]; then
            filename=$(basename "$pdf")
            echo "  Uploading $filename..."
            databricks fs cp "$pdf" "dbfs:/FileStore/documents/test_documents/$filename" --overwrite
        fi
    done
    echo "✓ Test documents uploaded"
else
    echo "⚠️  test_documents folder not found"
fi
echo ""

# Upload Databricks scripts
echo "Uploading Databricks scripts..."
databricks fs cp "databricks_batch_job.py" "dbfs:/FileStore/document_classifier/databricks_batch_job.py" --overwrite
echo "✓ Databricks scripts uploaded"
echo ""

echo "=========================================="
echo "Upload Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Set up secrets:"
echo "   databricks secrets create-scope --scope document-classifier"
echo "   databricks secrets put --scope document-classifier --key openrouter-api-key"
echo ""
echo "2. Import notebooks:"
echo "   - databricks_interactive_notebook.py"
echo "   - databricks_batch_job.py"
echo ""
echo "3. Test the system:"
echo "   Run the interactive notebook to verify everything works"
echo ""

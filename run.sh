#!/bin/bash

# AI Document Classification System - Quick Start Script

echo "=================================="
echo "AI Document Classification System"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your API keys:"
    echo "   - OPENAI_API_KEY (required)"
    echo "   - ANTHROPIC_API_KEY (optional)"
    echo ""
    read -p "Press Enter after configuring .env file..."
fi

# Create required directories
echo "📁 Creating required directories..."
mkdir -p uploads test_documents static templates

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check system dependencies
echo ""
echo "🔍 Checking system dependencies..."

if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Tesseract OCR not found. Install with:"
    echo "   macOS: brew install tesseract"
    echo "   Ubuntu: sudo apt-get install tesseract-ocr"
fi

if ! command -v pdfinfo &> /dev/null; then
    echo "⚠️  Poppler not found. Install with:"
    echo "   macOS: brew install poppler"
    echo "   Ubuntu: sudo apt-get install poppler-utils"
fi

# Run tests
echo ""
echo "🧪 Running system tests..."
python test_system.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo ""
    echo "🚀 Starting application..."
    echo "   Access the UI at: http://localhost:5000"
    echo ""
    echo "   Press Ctrl+C to stop the server"
    echo ""
    python app.py
else
    echo ""
    echo "❌ Some tests failed. Please check the configuration."
    echo "   Make sure your .env file has valid API keys."
    exit 1
fi

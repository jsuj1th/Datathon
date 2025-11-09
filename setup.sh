#!/bin/bash

# Setup script for Automated Job Retriever

echo "🚀 Setting up Automated Job Retriever..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
playwright install chromium

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Copy environment template
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your GitHub token!"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "=" * 60
echo "✨ Setup Complete!"
echo "=" * 60
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GITHUB_PERSONAL_ACCESS_TOKEN"
echo "   Get a token from: https://github.com/settings/tokens"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the data collection:"
echo "   python main.py"
echo ""
echo "4. Check the output:"
echo "   cat data/jobs_output.json"
echo ""

#!/bin/bash

# Setup script for LinkedIn MCP Server
echo "🚀 Setting up LinkedIn MCP Server..."

# Check if Python 3.9+ is installed
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
if [[ $(echo "$python_version >= 3.9" | bc) -eq 0 ]]; then
    echo "❌ Error: Python 3.9 or higher is required"
    exit 1
fi
echo "✅ Python $python_version found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install the package in development mode
echo "📦 Installing package in development mode..."
pip install -e .

# Copy environment template
if [ ! -f ".env" ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your LinkedIn credentials"
fi

# Make scripts executable
chmod +x setup.sh
chmod +x main.py
chmod +x test_linkedin_mcp.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your LinkedIn credentials:"
echo "   - LINKEDIN_EMAIL=your_email@example.com"
echo "   - LINKEDIN_PASSWORD=your_password"
echo ""
echo "2. Test the installation:"
echo "   python test_linkedin_mcp.py"
echo ""
echo "3. Start the MCP server:"
echo "   python main.py"
echo ""
echo "4. Configure Claude Desktop with the provided configuration"
echo ""

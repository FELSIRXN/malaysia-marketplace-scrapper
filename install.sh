#!/bin/bash
# Installation script for neru-scrapper
# Handles common installation issues including metadata generation errors

echo "🚀 Installing neru-scrapper dependencies..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Upgrade pip and install build tools first
echo "📦 Upgrading pip and installing build tools..."
python3 -m pip install --upgrade pip setuptools wheel

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔨 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip in virtual environment
pip install --upgrade pip setuptools wheel

# Install dependencies with error handling
echo "📋 Installing dependencies..."

# Core dependencies first (most stable)
echo "Installing core dependencies..."
pip install requests beautifulsoup4 python-dotenv

# Scientific computing dependencies
echo "Installing scientific computing dependencies..."
pip install numpy pandas

# Visualization dependencies
echo "Installing visualization dependencies..."
pip install matplotlib seaborn plotly

# Web scraping dependencies
echo "Installing web scraping dependencies..."
pip install selenium lxml fake-useragent

# Office file support
echo "Installing office file support..."
pip install openpyxl

# Text processing
echo "Installing text processing dependencies..."
pip install wordcloud

# Web framework dependencies
echo "Installing web framework dependencies..."
pip install fastapi uvicorn pydantic aiofiles

echo "✅ Installation completed successfully!"
echo ""
echo "To activate the virtual environment, run:"
echo "source venv/bin/activate"
echo ""
echo "To run the scraper:"
echo "python main.py"

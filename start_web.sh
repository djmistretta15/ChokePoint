#!/bin/bash

echo "⚡ Tollbooth Seeker AI - Web Dashboard"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data
mkdir -p web

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --break-system-packages

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Run the web server
echo "🌐 Starting Web Dashboard..."
echo ""
echo "Dashboard URL: http://localhost:5000"
echo "API Endpoint: http://localhost:5000/api/dashboard"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 web_server.py

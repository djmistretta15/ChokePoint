#!/bin/bash

echo "⚡ Tollbooth Seeker AI - Startup Script"
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

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --break-system-packages

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Run the engine
echo "🚀 Starting Tollbooth Seeker AI..."
echo "   Infrastructure Chokepoint Intelligence Engine"
echo "   Press Ctrl+C to stop"
echo ""

python3 main.py

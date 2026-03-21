#!/bin/bash

# ==================================
# House Price Predictor - Quick Start
# ==================================

echo "============================================"
echo "🏠 House Price Predictor - Quick Start"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 detected: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Create directories if they don't exist
echo "📁 Setting up directories..."
mkdir -p saved_models
mkdir -p templates
mkdir -p static
echo "✅ Directories created"
echo ""

# Check for model files
echo "🔍 Checking for model files..."

MODEL_FOUND=false
FEATURES_FOUND=false

if [ -f "saved_models/best_model.pkl" ] || [ -f "best_model.pkl" ]; then
    echo "✅ Model file found"
    MODEL_FOUND=true
else
    echo "⚠️  Model file not found (best_model.pkl)"
fi

if [ -f "saved_models/feature_names.pkl" ] || [ -f "feature_names.pkl" ] || [ -f "feature_names.txt" ]; then
    echo "✅ Feature names file found"
    FEATURES_FOUND=true
else
    echo "⚠️  Feature names file not found"
fi

if [ -f "saved_models/scaler.pkl" ] || [ -f "scaler.pkl" ]; then
    echo "✅ Scaler file found"
else
    echo "ℹ️  Scaler file not found (optional)"
fi

echo ""

# Start server
if [ "$MODEL_FOUND" = true ] && [ "$FEATURES_FOUND" = true ]; then
    echo "============================================"
    echo "🚀 Starting server..."
    echo "============================================"
    echo ""
    echo "📡 Server will be available at:"
    echo "   🌐 Web App: http://127.0.0.1:8000"
    echo "   📚 API Docs: http://127.0.0.1:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
else
    echo "============================================"
    echo "⚠️  SETUP REQUIRED"
    echo "============================================"
    echo ""
    echo "Please add the following files before running:"
    
    if [ "$MODEL_FOUND" = false ]; then
        echo "   • best_model.pkl (trained ML model)"
    fi
    
    if [ "$FEATURES_FOUND" = false ]; then
        echo "   • feature_names.pkl or feature_names.txt"
    fi
    
    echo ""
    echo "Place them in the 'saved_models/' directory or in the root directory."
    echo ""
    echo "Once files are added, run this script again:"
    echo "   bash start.sh"
    echo ""
fi

#!/bin/bash
# Setup script to fix Pylance errors

echo "🔧 Setting up Python environment to fix Pylance errors..."

# Navigate to backend
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "🎯 NEXT STEP: Select Python interpreter in your editor"
echo ""
echo "In VS Code/Windsurf:"
echo "  1. Press Ctrl+Shift+P"
echo "  2. Type: Python: Select Interpreter"
echo "  3. Select: ./backend/venv/bin/python"
echo ""
echo "This will fix all Pylance errors! 💚"

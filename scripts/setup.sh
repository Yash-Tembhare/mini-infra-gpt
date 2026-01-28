#!/bin/bash

# ==========================================
# Mini InfraGPT - Setup Script
# ==========================================

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              Mini InfraGPT - Setup Script                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "💡 Install Python from: https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python $(python3 --version) found"

# Check if pip is installed
echo ""
echo "🔍 Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed!"
    echo "💡 Install pip: python3 -m ensurepip --upgrade"
    exit 1
fi
echo "✅ pip found"

# Create virtual environment
echo ""
echo "🐍 Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null || {
    echo "⚠️  Could not activate virtual environment automatically"
    echo "💡 Activate it manually:"
    echo "   Linux/Mac: source venv/bin/activate"
    echo "   Windows: venv\\Scripts\\activate"
}

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Check Terraform
echo ""
echo "🔍 Checking Terraform installation..."
if ! command -v terraform &> /dev/null; then
    echo "⚠️  Terraform is not installed!"
    echo "💡 Install from: https://www.terraform.io/downloads"
    echo "   This is required for AWS deployment"
else
    echo "✅ Terraform $(terraform version | head -n 1) found"
fi

# Check AWS CLI
echo ""
echo "🔍 Checking AWS CLI installation..."
if ! command -v aws &> /dev/null; then
    echo "⚠️  AWS CLI is not installed!"
    echo "💡 Install from: https://aws.amazon.com/cli/"
    echo "   This is required for AWS deployment"
else
    echo "✅ AWS CLI $(aws --version) found"
fi

# Check Docker
echo ""
echo "🔍 Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker is not installed!"
    echo "💡 Install from: https://www.docker.com/get-started"
    echo "   This is optional for local testing"
else
    echo "✅ Docker $(docker --version) found"
fi

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p generated-terraform
mkdir -p logs
echo "✅ Directories created"

# Final instructions
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ SETUP COMPLETE!                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1️⃣  Set your API keys:"
echo "   export ANTHROPIC_API_KEY='your-claude-api-key'"
echo ""
echo "2️⃣  Configure AWS credentials:"
echo "   aws configure"
echo ""
echo "3️⃣  Run the application:"
echo "   python main.py 'I need a web server'"
echo ""
echo "💡 For more help, see README.md"
echo ""
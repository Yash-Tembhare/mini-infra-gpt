#!/bin/bash

# ==========================================
# Mini InfraGPT - Deployment Script
# ==========================================

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           Mini InfraGPT - Deploy to AWS                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Terraform directory exists
if [ ! -d "generated-terraform" ]; then
    echo "❌ No generated Terraform found!"
    echo "💡 First run: python main.py 'your infrastructure request'"
    exit 1
fi

# Check AWS credentials
echo "🔍 Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured!"
    echo "💡 Run: aws configure"
    exit 1
fi
echo "✅ AWS credentials OK"

# Navigate to Terraform directory
cd generated-terraform

# Terraform workflow
echo ""
echo "🚀 Starting deployment..."
echo ""

echo "1️⃣  Initializing Terraform..."
terraform init

echo ""
echo "2️⃣  Planning infrastructure..."
terraform plan

echo ""
echo "3️⃣  Applying infrastructure..."
echo "⏱️  This will take 3-5 minutes..."
terraform apply -auto-approve

echo ""
echo "✅ Deployment complete!"
echo ""

# Show outputs
echo "📊 Deployment Information:"
terraform output

echo ""
echo "💡 To destroy resources later: ./scripts/cleanup.sh"
echo ""
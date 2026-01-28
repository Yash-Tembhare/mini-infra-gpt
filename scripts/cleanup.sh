#!/bin/bash

# ==========================================
# Mini InfraGPT - Cleanup Script
# ==========================================

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           Mini InfraGPT - Cleanup AWS Resources             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Terraform directory exists
if [ ! -d "generated-terraform" ]; then
    echo "❌ No Terraform state found!"
    exit 1
fi

cd generated-terraform

echo "⚠️  WARNING: This will DELETE all AWS resources created by this project!"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Cleanup cancelled"
    exit 0
fi

echo ""
echo "🗑️  Destroying infrastructure..."
terraform destroy -auto-approve

echo ""
echo "✅ All resources destroyed!"
echo "💰 AWS charges stopped"
echo ""
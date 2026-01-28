#!/usr/bin/env python3
"""
Mini InfraGPT - Main Application
"""

import sys
from src.ai_parser import parse_infrastructure_request
from src.terraform_generator import generate_terraform_code

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════╗
║          🤖 Mini InfraGPT                               ║
║      AI-Powered Infrastructure Creator                   ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    print_banner()
    
    if len(sys.argv) > 1:
        request = ' '.join(sys.argv[1:])
    else:
        print("📝 What infrastructure do you need?\n")
        print("💡 Examples:")
        print("   • I need a simple web server")
        print("   • Create an API with PostgreSQL")
        print("   • Web app with MySQL\n")
        request = input("👉 Your request: ")
    
    if not request.strip():
        print("❌ No request provided!")
        sys.exit(1)
    
    print(f"\n💭 Your request: {request}\n")
    print("="*60)
    
    print("\n🧠 STEP 1: Analyzing request...\n")
    specs = parse_infrastructure_request(request)
    
    print("\n" + "="*60)
    print("\n📝 STEP 2: Generating Terraform code...\n")
    tf_file = generate_terraform_code(specs)
    
    print("\n" + "="*60)
    print("\n✅ PREPARATION COMPLETE!")
    print("="*60)
    print("\n📋 Next Steps:\n")
    print("1️⃣  Review Terraform:")
    print(f"   cat {tf_file}")
    print("\n2️⃣  Deploy to AWS:")
    print("   cd generated-terraform")
    print("   terraform init")
    print("   terraform apply")
    print("\n3️⃣  Cleanup:")
    print("   terraform destroy")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)

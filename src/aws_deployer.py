"""
AWS Deployer - Handles Terraform execution and AWS operations
"""

import subprocess
import sys
import time
import os
import json

def run_command(command, cwd=None, capture_output=False):
    """
    Run a shell command and handle errors
    
    Args:
        command (list): Command and arguments as list
        cwd (str): Working directory
        capture_output (bool): Whether to capture output
        
    Returns:
        CompletedProcess object if capture_output=True, else None
    """
    try:
        if capture_output:
            result = subprocess.run(
                command,
                cwd=cwd,
                check=True,
                capture_output=True,
                text=True
            )
            return result
        else:
            subprocess.run(command, cwd=cwd, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {' '.join(command)}")
        if capture_output and e.stderr:
            print(f"Error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ Command not found: {command[0]}")
        print(f"💡 Make sure {command[0]} is installed and in your PATH")
        sys.exit(1)

def terraform_init(terraform_dir):
    """Initialize Terraform"""
    print("\n🔧 Initializing Terraform...")
    run_command(['terraform', 'init'], cwd=terraform_dir)
    print("✅ Terraform initialized!")

def terraform_plan(terraform_dir):
    """Run Terraform plan"""
    print("\n📋 Creating execution plan...")
    run_command(['terraform', 'plan'], cwd=terraform_dir)
    print("✅ Plan created!")

def terraform_apply(terraform_dir):
    """Apply Terraform configuration"""
    print("\n⚡ Applying infrastructure changes...")
    print("⏱️  This will take 3-5 minutes...")
    
    # Ask for confirmation
    response = input("\n🤔 Do you want to proceed? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("❌ Deployment cancelled!")
        sys.exit(0)
    
    run_command(['terraform', 'apply', '-auto-approve'], cwd=terraform_dir)
    print("✅ Infrastructure deployed!")

def terraform_output(terraform_dir, output_name=None):
    """Get Terraform outputs"""
    if output_name:
        result = run_command(
            ['terraform', 'output', '-raw', output_name],
            cwd=terraform_dir,
            capture_output=True
        )
        return result.stdout.strip()
    else:
        result = run_command(
            ['terraform', 'output', '-json'],
            cwd=terraform_dir,
            capture_output=True
        )
        return json.loads(result.stdout)

def terraform_destroy(terraform_dir):
    """Destroy Terraform-managed infrastructure"""
    print("\n🗑️  Destroying infrastructure...")
    
    # Ask for confirmation
    response = input("\n⚠️  This will DELETE all resources. Are you sure? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("❌ Destruction cancelled!")
        sys.exit(0)
    
    run_command(['terraform', 'destroy', '-auto-approve'], cwd=terraform_dir)
    print("✅ Infrastructure destroyed!")

def wait_for_instance(instance_ip, timeout=300):
    """
    Wait for EC2 instance to be ready
    
    Args:
        instance_ip (str): Public IP of the instance
        timeout (int): Maximum wait time in seconds
    """
    print(f"\n⏳ Waiting for instance {instance_ip} to be ready...")
    print("   (This may take 2-3 minutes)")
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Try to ping the instance
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '2', instance_ip],
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"✅ Instance is responding to ping!")
                
                # Wait a bit more for SSH to be ready
                print("   Waiting for SSH service...")
                time.sleep(30)
                return True
                
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            print(f"   Still waiting... ({int(time.time() - start_time)}s)")
        
        time.sleep(10)
    
    print("⚠️  Timeout waiting for instance. It might still be starting up.")
    return False

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    try:
        result = subprocess.run(
            ['aws', 'sts', 'get-caller-identity'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            identity = json.loads(result.stdout)
            print(f"✅ AWS credentials configured for account: {identity['Account']}")
            return True
        else:
            print("❌ AWS credentials not configured!")
            print("\n💡 Configure AWS CLI:")
            print("   aws configure")
            return False
            
    except FileNotFoundError:
        print("❌ AWS CLI not installed!")
        print("\n💡 Install AWS CLI:")
        print("   https://aws.amazon.com/cli/")
        return False
    except Exception as e:
        print(f"❌ Error checking AWS credentials: {e}")
        return False

# Main deployment function
def deploy_infrastructure(terraform_dir='generated-terraform'):
    """
    Complete deployment workflow
    
    Args:
        terraform_dir (str): Path to Terraform configuration directory
    """
    print("\n" + "="*60)
    print("☁️  AWS DEPLOYMENT")
    print("="*60)
    
    # Check AWS credentials
    if not check_aws_credentials():
        sys.exit(1)
    
    # Run Terraform workflow
    terraform_init(terraform_dir)
    terraform_plan(terraform_dir)
    terraform_apply(terraform_dir)
    
    # Get outputs
    print("\n📊 Retrieving deployment information...")
    outputs = terraform_output(terraform_dir)
    
    instance_ip = outputs.get('instance_public_ip', {}).get('value')
    instance_id = outputs.get('instance_id', {}).get('value')
    app_url = outputs.get('application_url', {}).get('value')
    
    print(f"\n✅ Deployment Information:")
    print(f"   Instance ID: {instance_id}")
    print(f"   Public IP: {instance_ip}")
    print(f"   Application URL: {app_url}")
    
    # Wait for instance
    if instance_ip:
        wait_for_instance(instance_ip)
    
    return {
        'instance_ip': instance_ip,
        'instance_id': instance_id,
        'app_url': app_url
    }

# Test mode
if __name__ == "__main__":
    print("Testing AWS Deployer...")
    check_aws_credentials()
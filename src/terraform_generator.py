"""
Terraform Generator - Creates Terraform configuration files dynamically
"""

import os


def generate_terraform_code(specs):
    """
    Generate Terraform configuration based on parsed specifications
    """

    print("📝 Generating Terraform configuration...")

    # Create output directory
    output_dir = 'generated-terraform'
    os.makedirs(output_dir, exist_ok=True)

    # Main Terraform configuration
    main_tf = f"""
terraform {{
  required_version = ">= 1.0"

  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = "{specs['region']}"
}}

# VPC
resource "aws_vpc" "main" {{
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {{
    Name    = "mini-infra-gpt-vpc"
    Project = "mini-infra-gpt"
  }}
}}

# Public Subnet (AZ auto-selected)
resource "aws_subnet" "public" {{
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {{
    Name    = "public-subnet"
    Project = "mini-infra-gpt"
  }}
}}

# Internet Gateway
resource "aws_internet_gateway" "igw" {{
  vpc_id = aws_vpc.main.id

  tags = {{
    Name    = "mini-infra-gpt-igw"
    Project = "mini-infra-gpt"
  }}
}}

# Route Table
resource "aws_route_table" "public" {{
  vpc_id = aws_vpc.main.id

  route {{
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }}

  tags = {{
    Name    = "public-route-table"
    Project = "mini-infra-gpt"
  }}
}}

# Route Table Association
resource "aws_route_table_association" "public" {{
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}}

# Security Group
resource "aws_security_group" "web" {{
  name        = "mini-infra-gpt-web-sg"
  description = "Allow HTTP and SSH"
  vpc_id      = aws_vpc.main.id

  ingress {{
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  ingress {{
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  tags = {{
    Name    = "web-security-group"
    Project = "mini-infra-gpt"
  }}
}}

# Get latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {{
  most_recent = true
  owners      = ["amazon"]

  filter {{
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }}

  filter {{
    name   = "virtualization-type"
    values = ["hvm"]
  }}
}}

# EC2 Instance
resource "aws_instance" "web" {{
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public.id

  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y python3 python3-pip
              pip3 install flask
              EOF

  tags = {{
    Name    = "mini-infra-gpt-server"
    Project = "mini-infra-gpt"
    Type    = "{specs['app_type']}"
  }}
}}

# Outputs
output "instance_id" {{
  description = "EC2 instance ID"
  value       = aws_instance.web.id
}}

output "instance_public_ip" {{
  description = "Public IP address"
  value       = aws_instance.web.public_ip
}}

output "instance_public_dns" {{
  description = "Public DNS name"
  value       = aws_instance.web.public_dns
}}

output "application_url" {{
  description = "Application URL"
  value       = "http://${{aws_instance.web.public_ip}}"
}}
"""

    # Add database if needed
    if specs.get('database_needed', False):
        print("  ✅ Adding RDS database configuration...")

        db_port = 3306 if specs['database_type'] == 'mysql' else 5432
        db_version = '8.0' if specs['database_type'] == 'mysql' else '15'

        db_config = f"""

# Private Subnet for Database
resource "aws_subnet" "private" {{
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"

  tags = {{
    Name    = "private-subnet-db"
    Project = "mini-infra-gpt"
  }}
}}

# DB Subnet Group
resource "aws_db_subnet_group" "main" {{
  name       = "mini-infra-gpt-db-subnet"
  subnet_ids = [aws_subnet.public.id, aws_subnet.private.id]

  tags = {{
    Name    = "mini-infra-gpt-db-subnet-group"
    Project = "mini-infra-gpt"
  }}
}}

# Database Security Group
resource "aws_security_group" "db" {{
  name        = "mini-infra-gpt-db-sg"
  description = "Allow database traffic from web server"
  vpc_id      = aws_vpc.main.id

  ingress {{
    from_port       = {db_port}
    to_port         = {db_port}
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }}

  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  tags = {{
    Name    = "database-security-group"
    Project = "mini-infra-gpt"
  }}
}}

# RDS Database
resource "aws_db_instance" "main" {{
  identifier        = "mini-infra-gpt-db"
  engine            = "{specs['database_type']}"
  engine_version    = "{db_version}"
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name  = "miniinfragpt"
  username = "admin"
  password = "ChangeMe123!"

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]

  skip_final_snapshot = true
  publicly_accessible = false

  tags = {{
    Name    = "mini-infra-gpt-database"
    Project = "mini-infra-gpt"
  }}
}}

output "database_endpoint" {{
  description = "Database endpoint"
  value       = aws_db_instance.main.endpoint
}}

output "database_name" {{
  description = "Database name"
  value       = aws_db_instance.main.db_name
}}
"""
        main_tf += db_config

    # Write to file
    terraform_file = os.path.join(output_dir, 'main.tf')
    with open(terraform_file, 'w') as f:
        f.write(main_tf)

    print("✅ Terraform configuration generated!")
    print(f"📁 Location: {terraform_file}")
    print("📊 Resources to create:")
    print("   • VPC and Networking")
    print("   • Security Groups")
    print("   • EC2 Instance (t3.micro)")
    if specs.get('database_needed'):
        print(f"   • RDS Database ({specs['database_type']})")

    return terraform_file


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Terraform Generator")
    print("=" * 60)

    test_specs = {
        "instance_type": "t3.micro",
        "database_needed": False,
        "database_type": "none",
        "region": "us-east-1",
        "app_type": "web"
    }

    generate_terraform_code(test_specs)

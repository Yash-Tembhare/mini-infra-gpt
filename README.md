# 🚀 Mini InfraGPT

<div align="center">

**AI-Powered Infrastructure Automation - Create AWS infrastructure using natural language!**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Flask](https://img.shields.io/badge/Flask-Web-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

**✨ 100% Free - No Paid APIs Required! ✨**

[🌐 Live Demo](http://54.157.117.108/) • [📖 Documentation](#documentation) • [🚀 Quick Start](#quick-start)

</div>

---

## 📖 Overview

Mini InfraGPT automates AWS infrastructure deployment using natural language processing. Just describe what you need in plain English, and the system automatically:

- 🧠 **Parses** your infrastructure requirements intelligently
- 📝 **Generates** Terraform code dynamically
- ☁️ **Deploys** complete AWS infrastructure
- 🐳 **Containerizes** and deploys your application
- 📊 **Monitors** system health with built-in endpoints

### Example Usage
```bash
$ python main.py "I need a web server with PostgreSQL database"

🧠 Analyzing request...
✅ Specifications parsed
📝 Generating Terraform...
✅ Infrastructure ready to deploy!

$ cd generated-terraform && terraform apply
⏱️  Deploying to AWS...
✅ Your infrastructure is live!
🌐 http://YOUR-IP
```

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🆓 **100% Free** | No paid API keys required - uses rule-based parsing |
| 🏗️ **Infrastructure as Code** | Auto-generates production-ready Terraform |
| ☁️ **AWS Integration** | Full deployment automation for EC2, VPC, RDS |
| 🐍 **Python-Powered** | Clean, modular, well-documented codebase |
| 🔄 **CI/CD Ready** | GitHub Actions workflow included |
| 📊 **Monitoring** | Built-in health checks and status endpoints |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Terraform 1.0+
- AWS CLI (configured)
- AWS Account (Free Tier)

### Installation
```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/mini-infra-gpt.git
cd mini-infra-gpt

# 2. Setup environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure AWS
aws configure
# Enter your AWS credentials
```

### Deploy Infrastructure
```bash
# 1. Generate infrastructure code
python main.py "I need a simple web server"

# 2. Deploy to AWS
cd generated-terraform
terraform init
terraform plan
terraform apply  # Type 'yes' to confirm

# 3. Get your server IP
terraform output instance_public_ip

# 4. Deploy web application
cd ..
./deploy-app.sh
```

### Access Your Application
```
http://YOUR_PUBLIC_IP
```

---

## 📁 Project Structure
```
mini-infra-gpt/
├── src/
│   ├── ai_parser.py           # Natural language processing
│   ├── terraform_generator.py # Dynamic IaC generation
│   └── aws_deployer.py        # AWS automation
├── docker/
│   ├── Dockerfile             # Container definition
│   └── app.py                 # Flask application
├── scripts/
│   ├── setup.sh               # Environment setup
│   ├── deploy.sh              # AWS deployment
│   └── cleanup.sh             # Resource cleanup
├── tests/
│   └── test_parser.py         # Unit tests
├── app.py                     # Web application
├── deploy-app.sh              # App deployment script
├── main.py                    # Main entry point
└── requirements.txt           # Python dependencies
```

---

## 🛠️ How It Works

### Architecture
```
┌─────────────────────────────────────────────────────────┐
│                      USER INPUT                          │
│         "I need a web server with database"              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 INFRASTRUCTURE PARSER                    │
│          Analyzes request → Extracts specs               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              TERRAFORM CODE GENERATOR                    │
│         Creates VPC, Subnets, Security Groups            │
│              EC2 Instances, RDS Databases                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  AWS DEPLOYMENT                          │
│    terraform apply → Infrastructure provisioned          │
└─────────────────────────────────────────────────────────┘
```

### Components

1. **AI Parser** (`src/ai_parser.py`)
   - Parses natural language requests
   - Extracts infrastructure specifications
   - Fallback to rule-based parsing

2. **Terraform Generator** (`src/terraform_generator.py`)
   - Dynamically creates Terraform configurations
   - Supports EC2, VPC, RDS, Security Groups
   - Modular and extensible

3. **Flask Application** (`app.py`)
   - Lightweight web server
   - Health check endpoints
   - Beautiful responsive UI

---

## 📝 Usage Examples

### Simple Web Server
```bash
python main.py "I need a simple web server"
```

### API with Database
```bash
python main.py "Create an API server with PostgreSQL"
```

### Full Stack Application
```bash
python main.py "Web application with MySQL database"
```

---

## 🧪 Testing
```bash
# Run unit tests
pytest tests/ -v

# Test individual components
python src/ai_parser.py
python src/terraform_generator.py
```

---

## 🔐 Security Best Practices

- ✅ Never commit AWS credentials or SSH keys
- ✅ Use `.gitignore` to exclude sensitive files
- ✅ Rotate credentials regularly
- ✅ Use IAM roles with least privilege
- ✅ Enable MFA on AWS accounts
- ✅ Review security groups before deployment

---

## 💰 Cost Management

### AWS Free Tier Includes:
- **EC2:** 750 hours/month of t3.micro (12 months)
- **RDS:** 750 hours/month of db.t3.micro (12 months)
- **Storage:** 30GB EBS, 5GB S3
- **Data Transfer:** 15GB outbound

### ⚠️ Important

**Always destroy resources when not in use:**
```bash
cd generated-terraform
terraform destroy  # Type 'yes' to confirm
```

**Estimated monthly cost if exceeding free tier:** $15-25

---

## 🔧 Troubleshooting

### Common Issues

**"AWS credentials not configured"**
```bash
aws configure
```

**"Terraform not found"**
```bash
# Ubuntu/WSL
sudo apt install terraform

# macOS
brew install terraform
```

**"Permission denied" on scripts**
```bash
chmod +x scripts/*.sh
chmod +x deploy-app.sh
```

**"Instance type not available"**
- Edit `generated-terraform/main.tf`
- Change `instance_type` to `t2.micro` or `t3.micro`

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- [Terraform](https://www.terraform.io/) - Infrastructure as Code
- [AWS](https://aws.amazon.com/) - Cloud Infrastructure
- [Flask](https://flask.palletsprojects.com/) - Web Framework
- [Python](https://www.python.org/) - Programming Language

---

## 📧 Contact

**Your Name**
- Email: yashtembhare2025@gmail.com
- LinkedIn: https://www.linkedin.com/in/yash-tembhare/https://www.linkedin.com/in/yash-tembhare/
- GitHub: [@yourusername](https://github.com/Yash-Tembhare)

**Project Link:** https://github.com/yourusername/mini-infra-gpt

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

**Built with ❤️ by - Yash Tembhare for DevOps Learning**

</div>

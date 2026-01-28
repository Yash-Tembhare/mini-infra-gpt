"""
Simple Flask Web Application
This will be deployed inside a Docker container on AWS
"""

from flask import Flask, jsonify, render_template_string
import socket
import os
from datetime import datetime

app = Flask(__name__)

# HTML template for the homepage
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini InfraGPT</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
        }
        
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .info-box {
            background: #f7f7f7;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .info-box strong {
            color: #667eea;
        }
        
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }
        
        .tech-badge {
            background: #667eea;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .status {
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #4CAF50;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .footer {
            margin-top: 30px;
            text-align: center;
            color: #999;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Mini InfraGPT</h1>
        <p class="subtitle"><span class="status"></span>System is Live!</p>
        
        <div class="info-box">
            <strong>🖥️ Hostname:</strong> {{ hostname }}
        </div>
        
        <div class="info-box">
            <strong>🌐 Server IP:</strong> {{ server_ip }}
        </div>
        
        <div class="info-box">
            <strong>⏰ Deployed At:</strong> {{ deploy_time }}
        </div>
        
        <div class="info-box">
            <strong>🎯 Project:</strong> AI-Powered Infrastructure Automation
        </div>
        
        <h3 style="margin-top: 30px; color: #667eea;">Technology Stack:</h3>
        <div class="tech-stack">
            <span class="tech-badge">🐍 Python</span>
            <span class="tech-badge">🤖 Claude AI</span>
            <span class="tech-badge">☁️ AWS</span>
            <span class="tech-badge">🏗️ Terraform</span>
            <span class="tech-badge">🐳 Docker</span>
            <span class="tech-badge">⚙️ CI/CD</span>
            <span class="tech-badge">🔧 Linux</span>
        </div>
        
        <div class="footer">
            <p>Built with ❤️ for DevOps Learning</p>
            <p style="margin-top: 5px;">📊 <a href="/health" style="color: #667eea;">Health Check Endpoint</a></p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Homepage - shows project information"""
    return render_template_string(
        HTML_TEMPLATE,
        hostname=socket.gethostname(),
        server_ip=socket.gethostbyname(socket.gethostname()),
        deploy_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

@app.route('/health')
def health():
    """Health check endpoint - returns JSON status"""
    return jsonify({
        "status": "healthy",
        "hostname": socket.gethostname(),
        "project": "mini-infra-gpt",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/info')
def info():
    """API endpoint - returns system information"""
    return jsonify({
        "project": "Mini InfraGPT",
        "description": "AI-Powered Infrastructure Automation",
        "technologies": [
            "Python", "Claude AI", "AWS", "Terraform", 
            "Docker", "CI/CD", "Linux"
        ],
        "hostname": socket.gethostname(),
        "environment": os.environ.get("ENVIRONMENT", "production")
    })

if __name__ == '__main__':
    # Run the Flask app
    # 0.0.0.0 makes it accessible from outside the container
    # Port 5000 is the default Flask port
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False  # Set to False in production
    )
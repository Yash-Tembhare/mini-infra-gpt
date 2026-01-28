from flask import Flask
import socket
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mini InfraGPT - Live!</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 600px;
                width: 100%;
            }}
            h1 {{
                color: #667eea;
                margin-bottom: 20px;
                font-size: 2.5em;
            }}
            .info {{
                background: #f7f7f7;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
            }}
            .info strong {{
                color: #667eea;
            }}
            .badges {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 20px;
            }}
            .badge {{
                background: #667eea;
                color: white;
                padding: 8px 15px;
                border-radius: 20px;
                font-size: 0.9em;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                color: #999;
            }}
            .status {{
                display: inline-block;
                width: 12px;
                height: 12px;
                background: #4CAF50;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Mini InfraGPT</h1>
            <p style="color: #666; margin-bottom: 20px;">
                <span class="status"></span>System Online!
            </p>
            
            <div class="info">
                <strong>🖥️ Hostname:</strong> {socket.gethostname()}
            </div>
            
            <div class="info">
                <strong>🌐 Server IP:</strong> {socket.gethostbyname(socket.gethostname())}
            </div>
            
            <div class="info">
                <strong>⏰ Deployed:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
            </div>
            
            <div class="info">
                <strong>🎯 Project:</strong> AI-Powered Infrastructure Automation
            </div>
            
            <h3 style="margin-top: 30px; color: #667eea;">Technology Stack:</h3>
            <div class="badges">
                <span class="badge">🐍 Python</span>
                <span class="badge">☁️ AWS EC2</span>
                <span class="badge">🏗️ Terraform</span>
                <span class="badge">🐳 Docker</span>
                <span class="badge">⚡ Flask</span>
                <span class="badge">🔄 CI/CD</span>
            </div>
            
            <div class="footer">
                <p>Built with ❤️ for DevOps Learning</p>
                <p style="margin-top: 10px;">
                    <a href="/health" style="color: #667eea;">Health Check</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {
        "status": "healthy",
        "hostname": socket.gethostname(),
        "timestamp": datetime.now().isoformat(),
        "project": "mini-infra-gpt"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

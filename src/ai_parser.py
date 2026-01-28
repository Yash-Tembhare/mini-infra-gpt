"""
AI Parser - Uses Ollama or fallback parsing
"""

import sys

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


def check_ollama_running():
    """Check if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def parse_infrastructure_request(user_input):
    """
    Convert natural language to infrastructure specs
    Uses fallback parsing (no AI needed)
    """

    print("🔍 Analyzing your request...")

    user_lower = user_input.lower()

    # Detect database
    db_keywords = ['database', 'db', 'mysql', 'postgres', 'postgresql', 'sql',
                   'rds']
    database_needed = any(kw in user_lower for kw in db_keywords)

    # Database type
    if 'postgres' in user_lower or 'postgresql' in user_lower:
        database_type = 'postgres'
    elif 'mysql' in user_lower:
        database_type = 'mysql'
    else:
        database_type = 'none' if not database_needed else 'postgres'

    # App type
    if 'api' in user_lower or 'backend' in user_lower or 'rest' in user_lower:
        app_type = 'api'
    else:
        app_type = 'web'

    specs = {
        "instance_type": "t2.micro",
        "database_needed": database_needed,
        "database_type": database_type,
        "region": "us-east-1",
        "app_type": app_type
    }

    print("✅ Request parsed successfully!")
    print("📋 Specifications:")
    for key, value in specs.items():
        print(f"   • {key}: {value}")

    return specs


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Infrastructure Parser")
    print("=" * 60)
    print()

    tests = [
        "I need a simple web server",
        "Create API with PostgreSQL database",
        "Basic server for testing",
        "Web application with MySQL"
    ]

    for test in tests:
        print(f"📝 Request: {test}")
        print("-" * 60)
        parse_infrastructure_request(test)
        print()

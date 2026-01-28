"""
Unit tests for AI Parser
"""

import pytest
import os
from src.ai_parser import parse_infrastructure_request

def test_parser_basic():
    """Test basic parsing functionality"""
    # Skip if no API key (for CI/CD)
    if not os.environ.get('ANTHROPIC_API_KEY'):
        pytest.skip("ANTHROPIC_API_KEY not set")
    
    result = parse_infrastructure_request("I need a simple web server")
    
    assert 'instance_type' in result
    assert 'database_needed' in result
    assert 'region' in result
    assert result['region'] == 'us-east-1'

def test_parser_with_database():
    """Test parsing with database requirement"""
    if not os.environ.get('ANTHROPIC_API_KEY'):
        pytest.skip("ANTHROPIC_API_KEY not set")
    
    result = parse_infrastructure_request("Create an API with PostgreSQL")
    
    assert result['database_needed'] == True
    assert result['database_type'] in ['postgres', 'postgresql', 'mysql']

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
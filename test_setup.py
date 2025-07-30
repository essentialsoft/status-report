#!/usr/bin/env python3
"""
Test script to verify JIRA and Ollama connectivity
"""

import os
import requests
from dotenv import load_dotenv

def test_environment():
    """Test if environment variables are properly set"""
    load_dotenv()
    
    jira_token = os.getenv("JIRA_TOKEN")
    jira_url = os.getenv("JIRA_URL")
    jql = os.getenv("JIRA_JQL")
    
    print("🔍 Testing Environment Configuration...")
    
    if not jira_token or jira_token == "your_token_here":
        print("❌ JIRA_TOKEN is not properly set")
        return False
    else:
        print("✅ JIRA_TOKEN is set")
    
    if not jira_url or "yourdomain" in jira_url:
        print("❌ JIRA_URL is not properly set")
        return False
    else:
        print(f"✅ JIRA_URL is set: {jira_url}")
    
    if not jql:
        print("❌ JIRA_JQL is not set")
        return False
    else:
        print(f"✅ JIRA_JQL is set: {jql}")
    
    return True

def test_jira_connection():
    """Test JIRA API connectivity"""
    load_dotenv()
    
    jira_token = os.getenv("JIRA_TOKEN")
    jira_url = os.getenv("JIRA_URL")
    
    print("\n🔗 Testing JIRA Connection...")
    
    try:
        headers = {
            "Authorization": f"Bearer {jira_token}",
            "Accept": "application/json"
        }
        
        # Test with /myself endpoint
        response = requests.get(
            f"{jira_url}/rest/api/3/myself",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ JIRA connection successful!")
            print(f"   Logged in as: {user_data.get('displayName', 'Unknown')}")
            print(f"   Email: {user_data.get('emailAddress', 'Unknown')}")
            return True
        else:
            print(f"❌ JIRA connection failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ JIRA connection error: {e}")
        return False

def test_ollama_connection():
    """Test Ollama API connectivity"""
    print("\n🤖 Testing Ollama Connection...")
    
    try:
        # Test with a simple prompt
        body = {
            "model": "llama3",
            "messages": [
                {"role": "user", "content": "Say 'Hello from Ollama test'"}
            ],
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=body,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result.get("message", {}).get("content", "No response")
            print("✅ Ollama connection successful!")
            print(f"   Response: {message[:100]}...")
            return True
        else:
            print(f"❌ Ollama connection failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama connection error: {e}")
        print("   Make sure Ollama is running: 'ollama serve'")
        print("   And llama3 model is available: 'ollama pull llama3'")
        return False

def test_jira_query():
    """Test JIRA JQL query"""
    load_dotenv()
    
    jira_token = os.getenv("JIRA_TOKEN")
    jira_url = os.getenv("JIRA_URL")
    jql = os.getenv("JIRA_JQL")
    
    print(f"\n📋 Testing JIRA Query: {jql}")
    
    try:
        headers = {
            "Authorization": f"Bearer {jira_token}",
            "Accept": "application/json"
        }
        
        params = {
            "jql": jql,
            "maxResults": 5,
            "fields": "summary,status"
        }
        
        response = requests.get(
            f"{jira_url}/rest/api/3/search",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            issues = data.get("issues", [])
            total = data.get("total", 0)
            
            print(f"✅ JQL query successful!")
            print(f"   Found {total} total issues")
            print(f"   Showing first {len(issues)} issues:")
            
            for issue in issues[:3]:
                key = issue.get("key", "Unknown")
                summary = issue.get("fields", {}).get("summary", "No summary")
                status = issue.get("fields", {}).get("status", {}).get("name", "Unknown")
                print(f"   - {key}: {summary[:50]}... [{status}]")
            
            return True
        else:
            print(f"❌ JQL query failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ JQL query error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 JIRA to DOCX Automation - System Test")
    print("=" * 50)
    
    # Run tests
    tests = [
        test_environment(),
        test_jira_connection(),
        test_ollama_connection(),
        test_jira_query()
    ]
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = sum(tests)
    total = len(tests)
    
    if passed == total:
        print(f"✅ All tests passed ({passed}/{total})!")
        print("🎉 System is ready to run!")
    else:
        print(f"❌ {total - passed} test(s) failed ({passed}/{total})")
        print("🔧 Please fix the issues above before running the automation.")
    
    print("\nNext steps:")
    if passed == total:
        print("   Run: python jira_automation.py")
    else:
        print("   1. Fix the configuration issues")
        print("   2. Run this test again: python test_setup.py")
        print("   3. Then run: python jira_automation.py")

if __name__ == "__main__":
    main()

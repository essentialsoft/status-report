#!/usr/bin/env python3
"""
Configuration validator for JIRA to DOCX automation
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    required_files = [
        'requirements.txt',
        '.env',
        'jira_automation.py',
        'README.md'
    ]
    
    print("📁 Checking required files...")
    all_exist = True
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_exist = False
    
    return all_exist

def check_env_file():
    """Check .env file configuration"""
    print("\n🔧 Checking .env configuration...")
    
    if not Path('.env').exists():
        print("❌ .env file not found")
        return False
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        issues = []
        
        if 'your_token_here' in content:
            issues.append("JIRA_TOKEN still contains placeholder value")
        
        if 'yourdomain' in content:
            issues.append("JIRA_URL still contains placeholder domain")
        
        if 'JIRA_TOKEN=' not in content:
            issues.append("JIRA_TOKEN not defined")
        
        if 'JIRA_URL=' not in content:
            issues.append("JIRA_URL not defined")
        
        if 'JIRA_JQL=' not in content:
            issues.append("JIRA_JQL not defined")
        
        if issues:
            print("❌ .env file configuration issues:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ .env file appears properly configured")
            return True
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def check_python_version():
    """Check Python version"""
    print("\n🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.9+")
        return False

def check_dependencies():
    """Check if required packages can be imported"""
    print("\n📦 Checking Python dependencies...")
    
    packages = {
        'requests': 'HTTP requests library',
        'docx': 'python-docx for Word documents',
        'dotenv': 'python-dotenv for environment variables'
    }
    
    all_available = True
    
    for package, description in packages.items():
        try:
            if package == 'docx':
                # python-docx imports as 'docx'
                __import__('docx')
            elif package == 'dotenv':
                # python-dotenv imports as 'dotenv'
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"❌ {package} - {description} - NOT INSTALLED")
            all_available = False
    
    if not all_available:
        print("\n💡 To install missing packages:")
        print("   pip3 install -r requirements.txt")
    
    return all_available

def provide_next_steps(checks_passed):
    """Provide next steps based on validation results"""
    print("\n" + "="*50)
    print("📋 Validation Summary:")
    
    passed = sum(checks_passed)
    total = len(checks_passed)
    
    if passed == total:
        print(f"✅ All checks passed ({passed}/{total})!")
        print("\n🎉 Configuration is ready!")
        print("\nNext steps:")
        print("1. Test the setup: python3 test_setup.py")
        print("2. Run automation: python3 jira_automation.py")
    else:
        print(f"❌ {total - passed} check(s) failed ({passed}/{total})")
        print("\n🔧 Please fix the issues above:")
        
        if not checks_passed[0]:  # Files check
            print("   - Ensure all required files are present")
        
        if not checks_passed[1]:  # Environment check
            print("   - Configure .env file with your JIRA credentials")
            print("   - Copy .env.example to .env and edit it")
        
        if not checks_passed[2]:  # Python version
            print("   - Upgrade to Python 3.9 or higher")
        
        if not checks_passed[3]:  # Dependencies
            print("   - Install dependencies: pip3 install -r requirements.txt")
        
        print("\n   Then run this validator again: python3 validate_config.py")

def main():
    """Main validation function"""
    print("🔍 JIRA to DOCX Automation - Configuration Validator")
    print("="*60)
    
    # Run all checks
    checks = [
        check_files(),
        check_env_file(),
        check_python_version(),
        check_dependencies()
    ]
    
    # Provide summary and next steps
    provide_next_steps(checks)

if __name__ == "__main__":
    main()

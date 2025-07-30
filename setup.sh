#!/bin/bash

echo "🚀 Setting up JIRA to DOCX Automation"
echo "====================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Check if .env file has been configured
if grep -q "your_token_here" .env; then
    echo ""
    echo "⚠️  Warning: .env file needs to be configured"
    echo "   Please edit .env file with your actual JIRA credentials"
    echo ""
    echo "   1. Get your JIRA Personal Access Token:"
    echo "      - Go to JIRA → Account Settings → Security → API tokens"
    echo "      - Create new token and copy it"
    echo ""
    echo "   2. Edit .env file:"
    echo "      - Replace 'your_token_here' with your actual token"
    echo "      - Replace 'yourdomain' with your JIRA domain"
    echo "      - Update the JQL query as needed"
    echo ""
else
    echo "✅ .env file appears to be configured"
fi

# Check if Ollama is running
echo ""
echo "🤖 Checking Ollama..."
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "✅ Ollama is running"
    
    # Check if llama3 model is available
    if ollama list | grep -q "llama3"; then
        echo "✅ llama3 model is available"
    else
        echo "⚠️  llama3 model not found. Installing..."
        ollama pull llama3
        if [ $? -eq 0 ]; then
            echo "✅ llama3 model installed successfully"
        else
            echo "❌ Failed to install llama3 model"
        fi
    fi
else
    echo "⚠️  Ollama is not running or not installed"
    echo ""
    echo "   To install and start Ollama:"
    echo "   1. Install: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "   2. Start: ollama serve"
    echo "   3. Install model: ollama pull llama3"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure .env file (if not done already)"
echo "2. Ensure Ollama is running with llama3 model"
echo "3. Test the setup: python3 test_setup.py"
echo "4. Run the automation: python3 jira_automation.py"

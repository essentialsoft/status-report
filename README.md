# JIRA to DOCX Automation

Automated system for retrieving JIRA issues, summarizing them with Ollama LLM, and generating Word document reports.

## Features

- Fetch JIRA issues using JQL queries from multiple projects
- AI-powered summarization using Ollama (local LLM)
- Generate professional Word document reports
- Support for multiple project configurations
- Configurable via environment variables
- Error handling and validation

## Prerequisites

1. **Python 3.9+**
2. **Ollama** running locally with `llama3` model
3. **JIRA Personal Access Token**

## Quick Setup

#### Using Virtual Environment

It is recommended to use a virtual environment to isolate dependencies. Follow these steps:

1. Create a virtual environment:
     ```bash
     python3 -m venv venv
     ```

2. Activate the virtual environment:
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Configure Environment

Copy the example configuration and edit it:

```bash
cp .env.example .env
# Then edit .env with your actual values
```

Or edit the `.env` file directly with your JIRA credentials:

```env
JIRA_TOKEN=ATATTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
JIRA_URL=https://tracker.nci.nih.gov
JIRA_JQL=' AND (updated >= "2025-07-01" OR created >= "2025-07-01") AND issuetype in ("User Story", Bug, Task)'
JIRA_PROJECTS=Index of NCI Studies,CCDI CPI,Clinical and Translational Data Commons,Population Science Data Commons, CCDI cBioPortal,Bento-Commons, NCI Data Sharing Hub
```

**How to get JIRA Token:**
1. Go to JIRA → Account Settings → Security → API tokens
2. Create new token
3. Copy the token to `.env` file

#### 3. Setup Ollama

Install and run Ollama with llama3 model:

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull llama3 model
ollama pull llama3

# Start Ollama service
ollama serve
```

## Usage

### Validate Configuration

Before running the automation, validate your setup:

```bash
python3 validate_config.py
```

### Test Connections

Test JIRA and Ollama connectivity:

```bash
python3 test_setup.py
```

### Run the Automation

The automation can be run in two ways:

**Option 1: Direct execution (uses hardcoded project names)**
```bash
python3 jira_automation.py
```


### Expected Output

The automation will:
1. Process each specified project in your hardcoded list or PROJECT_NAMES environment variable
2. Fetch issues from JIRA based on your JQL query for each project  
3. Process each issue through Ollama for AI summarization
4. Generate `JIRA_Summary_Report.docx` with formatted results organized by project

**Default Projects** (when using direct execution):
- Index of NCI Studies
- CCDI CPI  
- Clinical and Translational Data Commons
- Population Science Data Commons
- CCDI cBioPortal
- Bento-Commons
- NCI Data Sharing Hub

### Sample JQL Queries

The JQL query in your `.env` file determines which issues are fetched for each project:

```bash
# Recent issues (current default)
' AND (updated >= "2025-07-01" OR created >= "2025-07-01") AND issuetype in ("User Story", Bug, Task)'

# All open issues  
' AND status != "Done"'

# High priority issues
' AND priority = "High" AND status != "Done"'

# Issues assigned to you
' AND assignee = currentUser() AND status != "Done"'

# Issues created in last 30 days
' AND created >= -30d'

# Specific issue types
' AND issuetype in ("Bug", "Task", "Story")'
```

## File Structure

```
├── jira_automation.py          # Main automation script
├── requirements.txt            # Python dependencies
├── .env                       # Environment configuration
├── .env.example               # Example configuration template
├── README.md                  # This file
├── setup.sh                   # Automated setup script
├── validate_config.py         # Configuration validator
├── test_setup.py              # Connection tester
└── JIRA_Summary_Report.docx   # Generated report (after running)
```

## Configuration Options

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `JIRA_TOKEN` | Your JIRA Personal Access Token | `ATATTxx...` |
| `JIRA_URL` | Your JIRA instance URL | `https://tracker.nci.nih.gov` |
| `JIRA_JQL` | JQL query to filter issues (applies to all projects) | `' AND updated >= "2025-07-01"'` |
| `PROJECT_NAMES` | Comma-separated list of project names (optional) | `"Project1,Project2,Project3"` |

### Project Configuration

**Method 1: Hardcoded Projects (Default)**
The script includes a default list of NCI projects. No additional configuration needed.

**Method 2: Environment Variable**
Set `PROJECT_NAMES` in your `.env` file and modify the script to use `JiraToDocxAutomation.from_env_projects()` instead of the hardcoded list.

### Customization

You can modify the script to:
- Change project names in the hardcoded list (lines 275-283 in `jira_automation.py`)
- Switch to environment-based project configuration (uncomment lines 271-272)
- Change the Ollama model (line 16)
- Adjust the maximum number of results per project (line 50)
- Customize the Word document formatting
- Add additional JIRA fields

## Troubleshooting

### Common Issues

1. **Import errors**: Run `pip3 install -r requirements.txt`
2. **JIRA authentication**: Check your token and URL in `.env`
3. **Ollama connection**: Ensure Ollama is running on `localhost:11434`
4. **No issues found**: Verify your JQL query returns results in JIRA for the specified projects
5. **Project not found**: Ensure project names in the hardcoded list or PROJECT_NAMES match exactly with JIRA project names

### Error Messages

- `JIRA_TOKEN must be set`: Update your `.env` file with actual token
- `PROJECT_NAMES must be set`: Set PROJECT_NAMES in .env if using from_env_projects() method
- `Error connecting to Ollama`: Start Ollama service
- `JIRA API error`: Check your JIRA URL and token permissions
- `Project not found in JIRA`: Verify project names exist and are spelled correctly

### Testing Connection

Test JIRA connection:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://tracker.nci.nih.gov/rest/api/3/myself"
```

Test Ollama connection:
```bash
curl -X POST http://localhost:11434/api/generate \
     -d '{"model":"llama3","prompt":"test","stream":false}'
```

## Optional Enhancements

- **Scheduling**: Use cron jobs for automated runs (see `run_automation.sh`)
- **Email Reports**: Add SMTP integration
- **Dynamic Project Lists**: Use JIRA API to fetch project lists automatically
- **Web Interface**: Build Flask/FastAPI frontend
- **Cloud Storage**: Upload reports to S3/Google Drive
- **Multi-environment**: Support different .env files for different environments

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- Use environment-specific tokens with minimal required permissions
- Ensure Ollama is not exposed to public networks

## License

This project is for internal use. Please ensure compliance with your organization's security policies.

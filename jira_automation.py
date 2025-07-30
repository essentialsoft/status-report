import os
import requests
import json
from docx import Document
from dotenv import load_dotenv
from typing import List, Dict, Any
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_URL = os.getenv("JIRA_URL")
JQL = os.getenv("JIRA_JQL")

OLLAMA_URL = "http://localhost:11434/api/generate"


class JiraToDocxAutomation:
    """Main class for JIRA to DOCX automation system"""
    
    def __init__(self, project_names: List[str]):
        self.validate_config()
        self.project_names = project_names if isinstance(project_names, list) else [project_names]
    
    @classmethod
    def from_env_projects(cls):
        """
        Create automation instance using project names from environment variable
        Expected format: JIRA_PROJECTS="Project1,Project2,Project3"
        """
        project_names_env = os.getenv("JIRA_PROJECTS", "")
        if not project_names_env:
            raise ValueError("JIRA_PROJECTS must be set in .env file (comma-separated list)")

        project_names = [name.strip() for name in project_names_env.split(",")]
        return project_names
    
    def validate_config(self):
        """Validate that all required environment variables are set"""
        if not JIRA_TOKEN or JIRA_TOKEN == "your_token_here":
            raise ValueError("JIRA_TOKEN must be set in .env file")
        if not JIRA_URL or "yourdomain" in JIRA_URL:
            raise ValueError("JIRA_URL must be set to your actual JIRA instance in .env file")
        if not JQL:
            raise ValueError("JIRA_JQL must be set in .env file")

    def fetch_issues(self, project_name: str) -> List[Dict[str, Any]]:
        """
        Fetch issues from JIRA using JQL
        
        Returns:
            List of issue dictionaries
        """
        try:
            headers = {
                "Authorization": f"Bearer {JIRA_TOKEN}",
                "Accept": "application/json",
            }
            
            params = {
                "jql": "project = '" + project_name + "' " + JQL,
                "fields": "issuetype,key,summary,status,project,priority,assignee,reporter,created,updated,duedate",
            }

            print(f"Fetching issues from JIRA with JQL: project = '{project_name}' {JQL}")
            response = requests.get(
                "https://tracker.nci.nih.gov/rest/api/2/search", 
                headers=headers, 
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"JIRA API error: {response.status_code} - {response.text}")
            
            data = response.json()
            issues = data.get("issues", [])
            print(f"Successfully fetched {len(issues)} issues from JIRA")
            return issues
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issues from JIRA: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
    
    def summarize_with_ollama(self, text: str) -> str:
        """
        Summarize text using Ollama LLM
        
        Args:
            text: The text to summarize
            
        Returns:
            Summarized text
        """
        try:
            # Prepare the request body for Ollama chat API
            body = {
                "model": "llama3",
                "prompt": (
                        "You are a project manager assistant. Given a list of JIRA issues or tasks with the fields: "
                        "Issue Type, Issue Key, Summary, and Status, create a concise and professional high-level summary "
                        "of planned or ongoing activities for this specific project in the current or upcoming month. "
                        "Focus on key themes, major milestones, and overall project direction. Do not list individual issues. "
                        "The overall summary should be limited to 150 words. Split the summary into two sections: Planned Activities and Completed Tasks from the past month. "
                        "Additionally, provide a list of Deliverable tasks including the following fields: Due Date, Date Updated, Status, and Deliverable Name. "
                        f"Here is the list of issues for this project: {text}"
                    ),
                "stream": False
            }

            headers = {
                "Content-Type": "application/json"
            }
            
            print("Generating summary with Ollama...")
            response = requests.post(
                OLLAMA_URL, 
                json=body,
                headers=headers
            )
            
            if response.status_code != 200:
                print(f"Ollama API error: {response.status_code} - {response.text}")
                return f"Error generating summary: {response.text}"
            
            result = response.json()
            summary = result.get("response", {})
            return summary.strip()
            
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            return f"Error connecting to Ollama: {e}"
        except Exception as e:
            print(f"Unexpected error during summarization: {e}")
            return f"Error generating summary: {e}"


    def generate_word_document(self, projects_data: Dict[str, Dict], filename: str = "JIRA_Summary_Report.docx"):
        """
        Generate Word document with issues grouped by project
        
        Args:
            projects_data: Dictionary with project names as keys and project data as values
            filename: Output filename
        """
        try:
            print(f"Generating Word document: {filename}")
            
            doc = Document()
            
            # Add title
            title = doc.add_heading("Projects monthly status report", 1)
            title.alignment = 1  # Center alignment
            
            # Process each project
            for project_name, project_data in projects_data.items():
                issues = project_data.get("issues", [])
                project_summary = project_data.get("ai_summary", "No summary available")
                
                # Add project heading
                doc.add_heading(f"{project_name}: Tasks completed or to be continued in the upcoming month.", 2)
                
                # Create table with headers
                issues_table = doc.add_table(rows=1, cols=4)
                issues_table.style = 'Table Grid'
                
                # Set table headers
                hdr_cells = issues_table.rows[0].cells
                hdr_cells[0].text = 'Issue Type'
                hdr_cells[1].text = 'Issue key'
                hdr_cells[2].text = 'Summary'
                hdr_cells[3].text = 'Status'
                
                # Add issues to table
                for issue in issues:
                    row_cells = issues_table.add_row().cells
                    row_cells[0].text = issue.get("issue type", "N/A")
                    row_cells[1].text = issue.get("issue key", "No key")
                    row_cells[2].text = issue.get("summary", "No summary")
                    row_cells[3].text = issue.get("status", "No status")

                # Project summary section
                doc.add_heading("Project Summary", level=3)
                doc.add_paragraph(project_summary)
                doc.add_page_break()
                
            # Save document
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_with_timestamp = f"{filename.split('.')[0]}_{timestamp}.docx"
            doc.save(filename_with_timestamp)
            print(f"Document saved successfully as {filename}")
            
        except Exception as e:
            print(f"Error generating Word document: {e}")
    

    def run(self):
        """
        Main execution method for multiple projects
        """
        print("Starting JIRA to DOCX automation for multiple projects...")
        print("=" * 50)
        
        projects_data = {}
        
        # Process each project
        for project_name in self.project_names:
            print(f"\nProcessing project: {project_name}")
            print("-" * 30)
            
            # Step 1: Fetch issues from JIRA for this project
            issues = self.fetch_issues(project_name)
            if not issues:
                print(f"No issues found for project {project_name}")
                projects_data[project_name] = {
                    "issues": [],
                    "ai_summary": f"No issues found for project {project_name}"
                }
                continue
            
            # Step 2: Process each issue
            issue_summaries = []
            
            for i, issue in enumerate(issues, 1):
                # Extract metadata
                fields = issue.get("fields", {})
                issue_data = {
                    "issue type": fields.get("issuetype", "Unknown").get("name", "Unknown"),
                    "issue key": issue.get("key", "No key"),
                    "summary": fields.get("summary", "No summary"),
                    "status": fields.get("status", {}).get("name", "Unknown"),
                    "created": fields.get("created", "Unknown"),
                    "updated": fields.get("updated", "Unknown"),
                    "duedate": fields.get("duedate", "No due date"),
                    "priority": fields.get("priority", {}).get("name", "None"),
                }
                
                issue_summaries.append(issue_data)
            
            # Step 3: Generate AI summary for this project
            issues_string = "\n".join([f"Issue Key: {issue['issue key']}, Summary: {issue['summary']}, Status: {issue['status']}, Created: {issue['created']}, Updated: {issue['updated']}, Due Date: {issue['duedate']}, Priority: {issue['priority']}" for issue in issue_summaries])
            print(f"\nGenerating AI summary for {project_name}...")
            ai_summary = self.summarize_with_ollama(issues_string)
            print(f"AI Summary for {project_name}:\n{ai_summary}")
            
            # Store project data
            projects_data[project_name] = {
                "issues": issue_summaries,
                "ai_summary": ai_summary
            }
        
        # Step 4: Generate combined Word document
        print(f"\n{'='*50}")
        print("Generating combined Word document for all projects...")
        
        total_issues = sum(len(project_data["issues"]) for project_data in projects_data.values())
        self.generate_word_document(projects_data)

        print(f"\n{'='*50}")
        print("Automation completed successfully!")
        print(f"Generated report for {len(projects_data)} projects with {total_issues} total issues.")
    
 
def main():
    """Entry point for the application"""
    try:
     
        project_names = JiraToDocxAutomation.from_env_projects()
        print(f"Project names: {project_names}")
        automation = JiraToDocxAutomation(project_names)
        automation.run()
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease ensure:")
        print("1. Your .env file is properly configured")
        print("2. Ollama is running locally with llama3 model")
        print("3. Your JIRA credentials are correct")
        print("4. Project names exist in your JIRA instance")
        print("5. If using from_env_projects(), set PROJECT_NAMES in .env file")


if __name__ == "__main__":
    main()

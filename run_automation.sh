#!/bin/bash

# JIRA to DOCX Automation Runner
# This script can be used with cron for scheduled automation

# Set the working directory to the script location
cd "$(dirname "$0")"

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Create logs directory if it doesn't exist
mkdir -p logs

# Generate timestamp for log file
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/automation_${TIMESTAMP}.log"

echo "Starting JIRA to DOCX automation at $(date)" | tee -a "$LOG_FILE"
echo "Logging to: $LOG_FILE" | tee -a "$LOG_FILE"
echo "=============================================" | tee -a "$LOG_FILE"

# Run the automation
python3 jira_automation.py 2>&1 | tee -a "$LOG_FILE"

# Check if the report was generated
if [ -f "JIRA_Summary_Report.docx" ]; then
    # Create timestamped backup
    REPORT_BACKUP="reports/JIRA_Summary_Report_${TIMESTAMP}.docx"
    mkdir -p reports
    cp "JIRA_Summary_Report.docx" "$REPORT_BACKUP"
    
    echo "Report generated successfully: $REPORT_BACKUP" | tee -a "$LOG_FILE"
    
    # Optional: Send email notification (uncomment and configure)
    # echo "JIRA report generated" | mail -s "JIRA Automation Complete" your-email@company.com
    
    # Optional: Upload to cloud storage (uncomment and configure)
    # aws s3 cp "$REPORT_BACKUP" s3://your-bucket/reports/
    
else
    echo "Error: Report was not generated!" | tee -a "$LOG_FILE"
    exit 1
fi

echo "=============================================" | tee -a "$LOG_FILE"
echo "Automation completed at $(date)" | tee -a "$LOG_FILE"

# Clean up old logs (keep last 30 days)
find logs -name "automation_*.log" -mtime +30 -delete 2>/dev/null

# Clean up old reports (keep last 10)
ls -t reports/JIRA_Summary_Report_*.docx 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null

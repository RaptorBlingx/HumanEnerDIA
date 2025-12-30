#!/bin/bash
# Weekly Chatbot Performance Analysis
# Runs every Monday at 9 AM to analyze the previous week's query logs
# Add to crontab: 0 9 * * 1 /home/ubuntu/humanergy/scripts/weekly_chatbot_analysis.sh

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_DIR/chatbot/rasa/logs/query_log.jsonl"
REPORT_DIR="$PROJECT_DIR/chatbot/reports"
REPORT_FILE="$REPORT_DIR/weekly_analysis_$(date +%Y%m%d).txt"
DAYS=7

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "========================================"
echo "📊 Weekly Chatbot Performance Analysis"
echo "========================================"
echo "Date: $(date)"
echo "Analyzing last $DAYS days..."
echo ""

# Create reports directory if it doesn't exist
mkdir -p "$REPORT_DIR"

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo -e "${RED}❌ Error: Log file not found: $LOG_FILE${NC}"
    echo "No query data to analyze yet."
    exit 1
fi

# Check if log file has data
if [ ! -s "$LOG_FILE" ]; then
    echo -e "${YELLOW}⚠️  Warning: Log file is empty${NC}"
    echo "No queries logged yet. Start using the chatbot to generate data."
    exit 0
fi

# Run the analysis
echo "Running analysis script..."
python3 "$SCRIPT_DIR/analyze_query_logs.py" "$DAYS" "$LOG_FILE" > "$REPORT_FILE" 2>&1

# Check if analysis was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Analysis complete!${NC}"
    echo ""
    echo "Report saved to: $REPORT_FILE"
    echo ""
    
    # Display summary (first 50 lines)
    echo "========================================"
    echo "Report Preview:"
    echo "========================================"
    head -50 "$REPORT_FILE"
    
    echo ""
    echo "========================================"
    echo "📧 Next Steps:"
    echo "========================================"
    echo "1. Review full report: cat $REPORT_FILE"
    echo "2. Check recommendations section for improvements"
    echo "3. Add missing keywords for failed queries"
    echo "4. Update chatbot based on usage patterns"
    echo ""
    
    # Check for critical issues
    failed_count=$(grep -c "Failed:" "$REPORT_FILE" || true)
    if [ "$failed_count" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Action Required:${NC}"
        echo "Found failed queries that need attention."
        echo "See 'Failed Queries' section in the report."
    fi
    
    # Archive old reports (keep last 12 weeks = 3 months)
    echo "Cleaning up old reports (keeping last 12 weeks)..."
    find "$REPORT_DIR" -name "weekly_analysis_*.txt" -mtime +84 -delete 2>/dev/null || true
    
else
    echo -e "${RED}❌ Analysis failed!${NC}"
    echo "Check the error log: $REPORT_FILE"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ Weekly analysis complete!"
echo "========================================"

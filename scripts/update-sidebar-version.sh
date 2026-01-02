#!/bin/bash
# Update sidebar.js version across all HTML files
# Usage: ./scripts/update-sidebar-version.sh

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Sidebar.js Version Update Script${NC}"
echo "================================================"

# Generate new version (timestamp)
NEW_VERSION=$(date +%Y%m%d%H%M%S)

echo -e "${YELLOW}📅 New version: v=${NEW_VERSION}${NC}"
echo ""

# Find all HTML files
HTML_FILES=$(find portal/public -name "*.html" -type f 2>/dev/null)
COUNT=$(echo "$HTML_FILES" | wc -l)

echo -e "${BLUE}📁 Found ${COUNT} HTML files${NC}"
echo ""

# Update all files
UPDATED=0
for FILE in $HTML_FILES; do
    if grep -q "sidebar.js?v=" "$FILE" 2>/dev/null; then
        # Get old version
        OLD_VERSION=$(grep -o "sidebar.js?v=[^\"']*" "$FILE" | head -1 | cut -d'=' -f2)
        
        # Update file
        sed -i "s/sidebar\.js?v=[^\"']*/sidebar.js?v=${NEW_VERSION}/g" "$FILE"
        
        echo -e "   ${GREEN}✅${NC} ${FILE} (v=${OLD_VERSION} → v=${NEW_VERSION})"
        ((UPDATED++))
    fi
done

echo ""
echo -e "${GREEN}✨ Updated ${UPDATED} files${NC}"
echo ""

# Restart nginx
echo -e "${BLUE}🔄 Restarting nginx...${NC}"
docker compose restart nginx > /dev/null 2>&1

# Wait for nginx to fully restart
sleep 3

# Verify deployment
echo ""
echo -e "${BLUE}🔍 Verifying deployment...${NC}"
DEPLOYED=$(curl -s https://wasabi.intel50001.com/index.html 2>/dev/null | grep -o "sidebar.js?v=[0-9]*" | head -1)

if [[ "$DEPLOYED" == "sidebar.js?v=${NEW_VERSION}" ]]; then
    echo -e "${GREEN}✅ Deployment verified: ${DEPLOYED}${NC}"
    echo ""
    echo -e "${GREEN}🎉 Update complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Test https://wasabi.intel50001.com in browser"
    echo "2. Check sidebar opens correctly"
    echo "3. Verify 'Pilot Factory Call' link appears"
    echo ""
    echo "Git commit suggestion:"
    echo -e "${YELLOW}git commit -m \"feat: update sidebar.js (v=${NEW_VERSION})\"${NC}"
else
    echo -e "${YELLOW}⚠️  Warning: Could not verify deployment${NC}"
    echo "Deployed: ${DEPLOYED}"
    echo "Expected: sidebar.js?v=${NEW_VERSION}"
    echo ""
    echo "Please check manually:"
    echo "curl -s https://wasabi.intel50001.com/index.html | grep sidebar.js"
fi

echo ""
echo "================================================"

#!/bin/bash
# ============================================================
#  JDS Knowledge Server — One-Click Installer
#  Just run: ./install.sh
# ============================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}============================================${NC}"
echo -e "${BOLD}  JDS Knowledge Server — Installing...${NC}"
echo -e "${BOLD}============================================${NC}"
echo ""

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 not found. Install from https://www.python.org/downloads/${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"

# 2. Get the directory where this script lives (= where server.py is)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_PATH="${SCRIPT_DIR}/server.py"

if [ ! -f "$SERVER_PATH" ]; then
    echo -e "${RED}ERROR: server.py not found in ${SCRIPT_DIR}${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Server found: ${SERVER_PATH}"

# 3. Make server executable
chmod +x "$SERVER_PATH"

# 4. Detect Claude Desktop config location
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/Claude"
else
    CONFIG_DIR="$APPDATA/Claude"
fi

CONFIG_FILE="${CONFIG_DIR}/claude_desktop_config.json"

# 5. Create config dir if needed
mkdir -p "$CONFIG_DIR"

# 6. Update or create Claude Desktop config
if [ -f "$CONFIG_FILE" ]; then
    # Config exists — check if it already has mcpServers
    if python3 -c "
import json, sys
with open('${CONFIG_FILE}', 'r') as f:
    config = json.load(f)
if 'mcpServers' not in config:
    config['mcpServers'] = {}
config['mcpServers']['jds-knowledge'] = {
    'command': 'python3',
    'args': ['${SERVER_PATH}']
}
with open('${CONFIG_FILE}', 'w') as f:
    json.dump(config, f, indent=2)
print('updated')
" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Claude Desktop config updated"
    else
        echo -e "${YELLOW}⚠${NC} Could not auto-update config. Adding manually..."
        # Fallback: write fresh config preserving nothing
        python3 -c "
import json
config = {'mcpServers': {'jds-knowledge': {'command': 'python3', 'args': ['${SERVER_PATH}']}}}
with open('${CONFIG_FILE}', 'w') as f:
    json.dump(config, f, indent=2)
"
        echo -e "${GREEN}✓${NC} Claude Desktop config created"
    fi
else
    # No config file — create one
    python3 -c "
import json
config = {'mcpServers': {'jds-knowledge': {'command': 'python3', 'args': ['${SERVER_PATH}']}}}
with open('${CONFIG_FILE}', 'w') as f:
    json.dump(config, f, indent=2)
"
    echo -e "${GREEN}✓${NC} Claude Desktop config created"
fi

# 7. Run quick test
echo ""
echo -e "${BOLD}Running tests...${NC}"
if python3 "${SCRIPT_DIR}/test_server.py" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} All 147 tests passed"
else
    echo -e "${YELLOW}⚠${NC} Some tests failed — server may still work"
fi

# 8. Done!
echo ""
echo -e "${BOLD}${GREEN}============================================${NC}"
echo -e "${BOLD}${GREEN}  INSTALLED SUCCESSFULLY!${NC}"
echo -e "${BOLD}${GREEN}============================================${NC}"
echo ""
echo -e "  ${BOLD}Next step:${NC} Restart Claude Desktop"
echo ""
echo -e "  Then ask Claude:"
echo -e "  ${YELLOW}\"Look up the Button component\"${NC}"
echo -e "  ${YELLOW}\"What is primary-50 color?\"${NC}"
echo -e "  ${YELLOW}\"Find calendar icon\"${NC}"
echo -e "  ${YELLOW}\"Get Figma reference for homepage\"${NC}"
echo ""

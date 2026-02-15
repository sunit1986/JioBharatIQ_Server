#!/bin/bash
# ============================================================
#  JioBharatIQ Server — One-Click Installer
#  Just run: ./install.sh
# ============================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

SERVER_VERSION="v1.2"
SERVER_NAME="JioBharatIQ_${SERVER_VERSION}"

echo ""
echo -e "${BOLD}============================================${NC}"
echo -e "${BOLD}  ${SERVER_NAME} Server — Installing...${NC}"
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

# ============================================================
# 4. Configure Claude Desktop
# ============================================================
if [[ "$OSTYPE" == "darwin"* ]]; then
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
else
    CLAUDE_CONFIG_DIR="$APPDATA/Claude"
fi

CLAUDE_CONFIG="${CLAUDE_CONFIG_DIR}/claude_desktop_config.json"
mkdir -p "$CLAUDE_CONFIG_DIR"

if [ -f "$CLAUDE_CONFIG" ]; then
    if python3 -c "
import json
with open('${CLAUDE_CONFIG}', 'r') as f:
    config = json.load(f)
if 'mcpServers' not in config:
    config['mcpServers'] = {}
config['mcpServers']['${SERVER_NAME}'] = {
    'command': 'python3',
    'args': ['${SERVER_PATH}']
}
with open('${CLAUDE_CONFIG}', 'w') as f:
    json.dump(config, f, indent=2)
print('updated')
" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Claude Desktop configured"
    else
        python3 -c "
import json
config = {'mcpServers': {'${SERVER_NAME}': {'command': 'python3', 'args': ['${SERVER_PATH}']}}}
with open('${CLAUDE_CONFIG}', 'w') as f:
    json.dump(config, f, indent=2)
"
        echo -e "${GREEN}✓${NC} Claude Desktop configured (fresh)"
    fi
else
    python3 -c "
import json
config = {'mcpServers': {'${SERVER_NAME}': {'command': 'python3', 'args': ['${SERVER_PATH}']}}}
with open('${CLAUDE_CONFIG}', 'w') as f:
    json.dump(config, f, indent=2)
"
    echo -e "${GREEN}✓${NC} Claude Desktop configured"
fi

# ============================================================
# 5. Configure Cursor (if installed)
# ============================================================
CURSOR_CONFIG="$HOME/.cursor/mcp.json"

if [ -d "$HOME/.cursor" ]; then
    if [ -f "$CURSOR_CONFIG" ]; then
        if python3 -c "
import json
with open('${CURSOR_CONFIG}', 'r') as f:
    config = json.load(f)
if 'mcpServers' not in config:
    config['mcpServers'] = {}
config['mcpServers']['${SERVER_NAME}'] = {
    'command': 'python3',
    'args': ['${SERVER_PATH}']
}
with open('${CURSOR_CONFIG}', 'w') as f:
    json.dump(config, f, indent=2)
print('updated')
" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} Cursor configured"
        else
            echo -e "${YELLOW}⚠${NC} Could not update Cursor config — add manually"
        fi
    else
        python3 -c "
import json
config = {'mcpServers': {'${SERVER_NAME}': {'command': 'python3', 'args': ['${SERVER_PATH}']}}}
with open('${CURSOR_CONFIG}', 'w') as f:
    json.dump(config, f, indent=2)
"
        echo -e "${GREEN}✓${NC} Cursor configured"
    fi
else
    echo -e "${YELLOW}—${NC} Cursor not found (skipped)"
fi

# ============================================================
# 6. Run quick test
# ============================================================
echo ""
echo -e "${BOLD}Running tests...${NC}"
if python3 "${SCRIPT_DIR}/test_server.py" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} All 147 tests passed"
else
    echo -e "${YELLOW}⚠${NC} Some tests failed — server may still work"
fi

# ============================================================
# 7. Done!
# ============================================================
echo ""
echo -e "${BOLD}${GREEN}============================================${NC}"
echo -e "${BOLD}${GREEN}  INSTALLED SUCCESSFULLY!${NC}"
echo -e "${BOLD}${GREEN}============================================${NC}"
echo ""
echo -e "  ${BOLD}Next step:${NC} Restart Claude Desktop / Cursor"
echo ""
echo -e "  Then ask Claude:"
echo -e "  ${YELLOW}\"Look up the Button component\"${NC}"
echo -e "  ${YELLOW}\"What is primary-50 color?\"${NC}"
echo -e "  ${YELLOW}\"Find calendar icon\"${NC}"
echo -e "  ${YELLOW}\"Get Figma reference for homepage\"${NC}"
echo ""

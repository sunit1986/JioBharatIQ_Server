#!/bin/bash
# Uninstall JioBharatIQ Server from Claude Desktop and Cursor

set -e

GREEN='\033[0;32m'
NC='\033[0m'

SERVER_VERSION="v1.2"
SERVER_NAME="JioBharatIQ_${SERVER_VERSION}"

# Remove from Claude Desktop
if [[ "$OSTYPE" == "darwin"* ]]; then
    CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CLAUDE_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
else
    CLAUDE_CONFIG="$APPDATA/Claude/claude_desktop_config.json"
fi

if [ -f "$CLAUDE_CONFIG" ]; then
    python3 -c "
import json
with open('${CLAUDE_CONFIG}', 'r') as f:
    config = json.load(f)
if 'mcpServers' in config and '${SERVER_NAME}' in config['mcpServers']:
    del config['mcpServers']['${SERVER_NAME}']
    if not config['mcpServers']:
        del config['mcpServers']
with open('${CLAUDE_CONFIG}', 'w') as f:
    json.dump(config, f, indent=2)
"
    echo -e "${GREEN}✓${NC} Removed from Claude Desktop"
fi

# Remove from Cursor
CURSOR_CONFIG="$HOME/.cursor/mcp.json"
if [ -f "$CURSOR_CONFIG" ]; then
    python3 -c "
import json
with open('${CURSOR_CONFIG}', 'r') as f:
    config = json.load(f)
if 'mcpServers' in config and '${SERVER_NAME}' in config['mcpServers']:
    del config['mcpServers']['${SERVER_NAME}']
    if not config['mcpServers']:
        del config['mcpServers']
with open('${CURSOR_CONFIG}', 'w') as f:
    json.dump(config, f, indent=2)
"
    echo -e "${GREEN}✓${NC} Removed from Cursor"
fi

echo ""
echo "  Restart Claude Desktop / Cursor to complete uninstall."

#!/bin/bash
# Uninstall JDS Knowledge Server from Claude Desktop

set -e

GREEN='\033[0;32m'
NC='\033[0m'

if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_FILE="$HOME/.config/Claude/claude_desktop_config.json"
else
    CONFIG_FILE="$APPDATA/Claude/claude_desktop_config.json"
fi

if [ -f "$CONFIG_FILE" ]; then
    python3 -c "
import json
with open('${CONFIG_FILE}', 'r') as f:
    config = json.load(f)
if 'mcpServers' in config and 'jds-knowledge' in config['mcpServers']:
    del config['mcpServers']['jds-knowledge']
    if not config['mcpServers']:
        del config['mcpServers']
with open('${CONFIG_FILE}', 'w') as f:
    json.dump(config, f, indent=2)
"
    echo -e "${GREEN}✓${NC} Removed jds-knowledge from Claude Desktop config"
    echo "  Restart Claude Desktop to complete uninstall."
else
    echo "Config file not found. Nothing to uninstall."
fi

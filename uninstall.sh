#!/bin/bash
# Uninstall JioBharatIQ Server from Claude Desktop and Cursor

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SERVER_NAME="JioBharatIQ"

# Remove from Claude Desktop
if [[ "$OSTYPE" == "darwin"* ]]; then
    CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CLAUDE_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
else
    CLAUDE_CONFIG="$APPDATA/Claude/claude_desktop_config.json"
fi

remove_server() {
    local config_file="$1"
    local app_name="$2"
    if [ -f "$config_file" ]; then
        python3 -c "
import json
with open('${config_file}', 'r') as f:
    config = json.load(f)
removed = False
if 'mcpServers' in config:
    for key in list(config['mcpServers'].keys()):
        if 'JioBharatIQ' in key or 'jiobharatiq' in key.lower():
            del config['mcpServers'][key]
            removed = True
    if not config['mcpServers']:
        del config['mcpServers']
with open('${config_file}', 'w') as f:
    json.dump(config, f, indent=2)
if removed:
    print('removed')
" 2>/dev/null && echo -e "${GREEN}✓${NC} Removed from $app_name" || echo -e "${YELLOW}-${NC} $app_name: no changes needed"
    fi
}

remove_server "$CLAUDE_CONFIG" "Claude Desktop"
remove_server "$HOME/.cursor/mcp.json" "Cursor"

# Remove from Claude Code CLI
if command -v claude &> /dev/null; then
    claude mcp remove JioBharatIQ 2>/dev/null && echo -e "${GREEN}✓${NC} Removed from Claude Code" || true
fi

echo ""
echo "  Restart Claude Desktop / Cursor to complete uninstall."
echo ""
echo "  To also remove uv (optional):"
echo "  rm -rf ~/.local/bin/uv ~/.local/bin/uvx ~/.cache/uv"

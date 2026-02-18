#!/bin/bash
# ============================================================
#  JioBharatIQ Server — Installer (uv + uvx)
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
echo -e "${BOLD}  JioBharatIQ Server — Installing...${NC}"
echo -e "${BOLD}============================================${NC}"
echo ""

# ============================================================
# 1. Ensure git is available (macOS needs Xcode CLT)
# ============================================================
if ! command -v git &> /dev/null; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${YELLOW}Installing Xcode Command Line Tools (needed for git)...${NC}"
        echo -e "${YELLOW}A popup may appear — click 'Install' and wait for it to finish.${NC}"
        xcode-select --install 2>/dev/null || true
        # Wait for the installation to complete
        echo -e "${YELLOW}Waiting for Xcode CLT installation to finish...${NC}"
        until command -v git &> /dev/null; do
            sleep 5
        done
        echo -e "${GREEN}✓${NC} Xcode Command Line Tools installed"
    else
        echo -e "${RED}ERROR: git is not installed. Please install git and re-run.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} git already installed"
fi

# ============================================================
# 2. Install uv if not present
# ============================================================
if ! command -v uvx &> /dev/null; then
    echo -e "${YELLOW}Installing uv (package manager)...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Source the env so uvx is available in this session
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    if ! command -v uvx &> /dev/null; then
        echo -e "${RED}ERROR: uv installed but uvx not found. Restart your terminal and re-run.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} uv installed"
else
    echo -e "${GREEN}✓${NC} uv already installed"
fi

# ============================================================
# 3. Symlink uv AND uvx into /usr/local/bin (so GUI apps can find them)
# ============================================================
if [[ "$OSTYPE" == "darwin"* ]]; then
    UV_PATH=$(which uv)
    UVX_PATH=$(which uvx)
    NEED_SUDO=false

    if [ "$UV_PATH" != "/usr/local/bin/uv" ]; then
        NEED_SUDO=true
    fi
    if [ "$UVX_PATH" != "/usr/local/bin/uvx" ]; then
        NEED_SUDO=true
    fi

    if [ "$NEED_SUDO" = true ]; then
        echo -e "${YELLOW}Making uv/uvx visible to Claude Desktop (may ask for password)...${NC}"
        sudo ln -sf "$UV_PATH" /usr/local/bin/uv
        sudo ln -sf "$UVX_PATH" /usr/local/bin/uvx
        echo -e "${GREEN}✓${NC} uv linked to /usr/local/bin/uv"
        echo -e "${GREEN}✓${NC} uvx linked to /usr/local/bin/uvx"
    else
        echo -e "${GREEN}✓${NC} uv and uvx already in /usr/local/bin"
    fi
fi

# ============================================================
# 4. MCP config snippet
# ============================================================
MCP_CONFIG='{
  "mcpServers": {
    "JioBharatIQ": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/sunit1986/JioBharatIQ_Server.git", "jiobharatiq-server"]
    }
  }
}'

# ============================================================
# 5. Configure Claude Desktop
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
    # Merge into existing config using Python (uv bundles Python)
    uv run python3 -c "
import json, sys
try:
    with open('${CLAUDE_CONFIG}', 'r') as f:
        config = json.load(f)
except:
    config = {}
if 'mcpServers' not in config:
    config['mcpServers'] = {}
config['mcpServers']['JioBharatIQ'] = {'command': 'uvx', 'args': ['--from', 'git+https://github.com/sunit1986/JioBharatIQ_Server.git', 'jiobharatiq-server']}
with open('${CLAUDE_CONFIG}', 'w') as f:
    json.dump(config, f, indent=2)
" 2>/dev/null || {
        # Fallback: write directly
        echo "$MCP_CONFIG" > "$CLAUDE_CONFIG"
    }
    echo -e "${GREEN}✓${NC} Claude Desktop configured"
else
    echo "$MCP_CONFIG" > "$CLAUDE_CONFIG"
    echo -e "${GREEN}✓${NC} Claude Desktop configured (fresh)"
fi

# ============================================================
# 6. Configure Cursor (if installed)
# ============================================================
CURSOR_CONFIG="$HOME/.cursor/mcp.json"

if [ -d "$HOME/.cursor" ]; then
    if [ -f "$CURSOR_CONFIG" ]; then
        uv run python3 -c "
import json
try:
    with open('${CURSOR_CONFIG}', 'r') as f:
        config = json.load(f)
except:
    config = {}
if 'mcpServers' not in config:
    config['mcpServers'] = {}
config['mcpServers']['JioBharatIQ'] = {'command': 'uvx', 'args': ['--from', 'git+https://github.com/sunit1986/JioBharatIQ_Server.git', 'jiobharatiq-server']}
with open('${CURSOR_CONFIG}', 'w') as f:
    json.dump(config, f, indent=2)
" 2>/dev/null || {
            echo "$MCP_CONFIG" > "$CURSOR_CONFIG"
        }
        echo -e "${GREEN}✓${NC} Cursor configured"
    else
        echo "$MCP_CONFIG" > "$CURSOR_CONFIG"
        echo -e "${GREEN}✓${NC} Cursor configured"
    fi
else
    echo -e "${YELLOW}-${NC} Cursor not found (skipped)"
fi

# ============================================================
# 7. Pre-warm the uvx cache
# ============================================================
echo ""
echo -e "${BOLD}Downloading server package...${NC}"
uvx --from "git+https://github.com/sunit1986/JioBharatIQ_Server.git" jiobharatiq-server --help > /dev/null 2>&1 || true
echo -e "${GREEN}✓${NC} Package cached"

# ============================================================
# 8. Done!
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

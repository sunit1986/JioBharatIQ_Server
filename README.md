# JDS Knowledge Server

A secure MCP (Model Context Protocol) server providing access to Jio Design System specifications, design tokens, icons, and Figma references.

## 🔒 Security Features

- ✅ **JSON-only responses** - No markdown, no explanations
- ✅ **No internal reasoning exposed** - Clean, structured data only
- ✅ **No file paths exposed** - Deep regex scanning strips any leaked paths
- ✅ **No skill references exposed** - Pure knowledge base
- ✅ **No secrets exposed** - API keys, passwords, tokens redacted automatically
- ✅ **Strict output structure** - Predictable, parseable responses
- ✅ **Input sanitization** - All inputs character-filtered, length-capped (200 chars)
- ✅ **Injection protection** - SQL, XSS, shell, template injection all blocked
- ✅ **Method whitelisting** - Only MCP protocol methods accepted
- ✅ **Tool whitelisting** - Only 4 registered tools can be called
- ✅ **Max message size** - 1MB cap prevents DoS
- ✅ **No eval/exec** - No dynamic code execution
- ✅ **Generic errors** - No stack traces or internal details in error messages
- ✅ **147 tests passing** - Comprehensive security + functionality test suite

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Python (if not already installed)

Check if Python 3 is installed:
```bash
python3 --version
```

If not installed, download from: https://www.python.org/downloads/

### Step 2: Clone or Download This Repository

Option A - If you have git:
```bash
git clone <your-github-repo-url>
cd jds-knowledge-server
```

Option B - Download ZIP:
1. Download the ZIP file from GitHub
2. Unzip and navigate to the folder
3. Open Terminal/Command Prompt in this folder

### Step 3: Make Server Executable

```bash
chmod +x server.py
```

✅ **No external dependencies required!** This server uses only Python standard library.

### Step 4: Test the Server

```bash
python3 server.py
```

You should see output like:
```
FastMCP server running...
```

Press `Ctrl+C` to stop the test.

### Step 5: Configure Claude Desktop

1. Open your Claude Desktop config file:

**macOS:**
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
notepad %APPDATA%\Claude\claude_desktop_config.json
```

2. Add this server configuration:

```json
{
  "mcpServers": {
    "jds-knowledge": {
      "command": "python3",
      "args": [
        "/ABSOLUTE/PATH/TO/jds-knowledge-server/server.py"
      ]
    }
  }
}
```

⚠️ **Important:** Replace `/ABSOLUTE/PATH/TO/` with the actual path to this folder.

To get the absolute path, run this in the `jds-knowledge-server` folder:
```bash
pwd
```

3. Save the file and restart Claude Desktop.

### Step 6: Verify in Claude Desktop

Open Claude Desktop and type:
```
Can you list available MCP tools?
```

You should see 4 tools:
- `lookup_component`
- `resolve_token`
- `find_icon`
- `get_figma_reference`

## 📖 Usage Examples

### 1. Lookup a Component

**Ask Claude:**
```
Use the JDS Knowledge Server to look up the Button component.
```

**Response Structure:**
```json
{
  "component": "Button",
  "import_path": "@jds/core",
  "description": "Primary interactive element for user actions",
  "props": {
    "kind": {
      "type": "string",
      "options": ["primary", "secondary", "tertiary"],
      "default": "primary"
    },
    "size": {
      "type": "string",
      "options": ["small", "medium", "large"],
      "default": "medium"
    }
  },
  "variants": {
    "kinds": ["primary", "secondary", "tertiary"],
    "sizes": ["small", "medium", "large"],
    "states": ["normal", "positive", "disabled", "loading"]
  },
  "code_example": "import { Button } from '@jds/core';\n\n<Button\n  kind=\"primary\"\n  size=\"medium\"\n  label=\"Click me\"\n  onClick={() => {}}\n/>"
}
```

### 2. Resolve a Design Token

**Ask Claude:**
```
What is the value of primary-50 token?
```

**Response Structure:**
```json
{
  "category": "colors",
  "subcategory": "primary",
  "token": "primary-50",
  "value": {
    "value": "#3535f3",
    "usage": "Primary brand color, main actions"
  }
}
```

### 3. Find an Icon

**Ask Claude:**
```
Find icons related to "calendar"
```

**Response Structure:**
```json
{
  "query": "calendar",
  "count": 3,
  "results": [
    {
      "icon": "ic_calendar",
      "category": "time",
      "keywords": ["date", "schedule", "event", "appointment"],
      "match_type": "name"
    },
    {
      "icon": "ic_calendar_today",
      "category": "time",
      "keywords": ["today", "current", "date"],
      "match_type": "keyword"
    }
  ]
}
```

### 4. Get Figma Reference

**Ask Claude:**
```
Get the Figma reference for the homepage design
```

**Response Structure:**
```json
{
  "name": "AI Assistant Homepage",
  "file_key": "yvWQ7pqZSgFIfO0XrzY1me",
  "node_id": "13157:2011",
  "url": "https://www.figma.com/design/yvWQ7pqZSgFIfO0XrzY1me/Home-Page-V2.0?node-id=13157-2011&m=dev",
  "description": "Default homepage layout (360x800px) with voice assistant"
}
```

## 🛠️ Available Tools

| Tool | Description | Args |
|------|-------------|------|
| `lookup_component` | Get component specs (Button, Card, Modal, etc.) | `component_name: string` |
| `resolve_token` | Get design token values (colors, typography, spacing) | `token_category: string`, `token_name?: string` |
| `find_icon` | Search 1546+ JDS icons | `query: string`, `limit?: number` |
| `get_figma_reference` | Get Figma node references | `design_name: string` |

## 📦 Available Components (21)

- **Button** - Primary interactive element (primary/secondary/tertiary)
- **InputField** - Text input with validation states
- **Card** - Content container with image and CTAs
- **Modal** - Overlay dialog
- **BottomSheet** - Mobile bottom drawer
- **Avatar** - Profile picture or initials
- **Tabs** - Content section navigation
- **Toast** - Temporary notifications
- **Accordion** - Expandable/collapsible panels
- **Divider** - Visual separator
- **Badge** - Status/label indicator
- **BottomNav** - Mobile bottom navigation bar
- **Container** - Flexible layout container
- **Spinner** - Loading indicator
- **Skeleton** - Content placeholder (shimmer)
- **PromoCard** - Promotional content card
- **ServiceCard** - Service/product card with branding
- **ContentBlock** - Structured content section
- **Carousel** - Horizontal content slider
- **RatingBar** - Star rating input/display
- **Text** - Typography component (body/label/title/headline/display)

## 🎨 Available Token Categories

- **colors** - primary, secondary, sparkle, feedback, grey, global
- **typography** - heading (6 sizes), body (6 sizes), special (overline, button, label, code)
- **spacing** - xxs to massive (10 sizes)
- **border_radius** - none to pill (8 sizes)
- **opacity** - invisible, disabled, enabled

## 🎯 Icon Categories

- communication (mail, message, chat, phone, video)
- media (play, pause, volume, mic)
- navigation (arrows, chevrons, menu, home)
- action (search, settings, favorite, edit, delete)
- content (add, copy, link, filter)
- device (smartphone, tablet, laptop, watch)
- image (photo, camera, crop)
- file (folder, cloud, upload, download)
- social (person, people, group, thumbs)
- places (location, map, directions, flight)
- toggle (checkbox, radio, toggle, star)
- time (alarm, schedule, calendar, event)
- editor (format, align, list)
- commerce (cart, payment, receipt, store)
- hardware (keyboard, mouse, power, usb)

## 📐 Figma References

Available designs:
- `homepage` - AI Assistant Homepage
- `menu` - Hamburger Menu
- `chat_page` - Chat Interface
- `media_page` - Media Gallery
- `assistants_page` - AI Assistants
- `tools_page` - Tools Page
- `oneui_design_kit` - Updated Component Specs
- `jio_testlab` - Component Test Boards
- `chat_input` - Chat Input States

## 🚨 Troubleshooting

### Server doesn't start

**Issue:** `python3: command not found` or `SyntaxError`

**Fix:**
- Make sure Python 3.8+ is installed: `python3 --version`
- Try running with full path: `/usr/bin/python3 server.py`

### Claude Desktop doesn't see the server

**Issue:** MCP tools not appearing in Claude Desktop

**Fix:**
1. Check the config file path is correct
2. Verify you used the **absolute path** to `server.py` (not relative)
3. Restart Claude Desktop completely
4. Check Terminal for any error messages

### Permission denied

**Issue:** `Permission denied: server.py`

**Fix:**
```bash
chmod +x server.py
```

## 🔄 Updating the Server

To update the knowledge base:
1. Edit `knowledge_base.py` (add new components, tokens, icons)
2. Save the file
3. Restart Claude Desktop

The server automatically reloads changes.

## 📤 Hosting on GitHub

### Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Repository name: `jds-knowledge-server`
3. Description: "JDS Design System MCP Knowledge Server"
4. Choose **Private** (to keep it internal)
5. Click "Create repository"

### Step 2: Push Your Code

```bash
cd /path/to/jds-knowledge-server

# Initialize git (if not already done)
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: JDS Knowledge Server"

# Add remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/jds-knowledge-server.git

# Push
git branch -M main
git push -u origin main
```

### Step 3: Share with Your Team

**Option A: Add Collaborators (Private Repo)**
1. Go to your repo → Settings → Collaborators
2. Add team members by GitHub username

**Option B: Share Clone Instructions**
Team members can clone with:
```bash
git clone https://github.com/YOUR-USERNAME/jds-knowledge-server.git
cd jds-knowledge-server
chmod +x server.py
```

✅ No dependencies to install - uses Python standard library only!

Then follow Steps 5-6 from Quick Start above.

## 🔐 Security Notes

- ✅ No sensitive data exposed (no API keys, no credentials)
- ✅ No file system access beyond this directory
- ✅ Read-only knowledge base (no write operations)
- ✅ Safe for non-technical users
- ✅ All responses are structured JSON (no code execution)

## 📞 Support

If team members have issues:
1. Check they're using Python 3.8+
2. Verify they installed dependencies (`pip3 install -r requirements.txt`)
3. Confirm they used the **absolute path** in config
4. Make sure they restarted Claude Desktop after config changes

## 📝 License

Internal use only - Jio Design System knowledge base.

---

**Built with:** FastMCP + Python
**Version:** 1.0.0
**Last Updated:** 2026-02-15

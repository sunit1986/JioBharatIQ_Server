# JDS Knowledge Server

MCP server for Jio Design System — components, tokens, icons, Figma references.

## Install

### One-time setup: install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Configure your AI tool

**Claude Desktop** — Settings > Developer > Edit Config:

```json
{
  "mcpServers": {
    "JioBharatIQ": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/sunit1986/JioBharatIQ_Server.git", "jiobharatiq-server"]
    }
  }
}
```

**Cursor** — Settings > MCP > Add Server:

```json
{
  "mcpServers": {
    "JioBharatIQ": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/sunit1986/JioBharatIQ_Server.git", "jiobharatiq-server"]
    }
  }
}
```

**Claude Code (CLI)**:

```bash
claude mcp add JioBharatIQ -- uvx --from "git+https://github.com/sunit1986/JioBharatIQ_Server.git" jiobharatiq-server
```

Restart the app. That's it.

## What you get

5 tools inside Claude Desktop / Cursor:

| Ask Claude... | Tool used |
|--------------|-----------|
| "How do I use Button?" | `lookup_component` |
| "What's primary-50 color?" | `resolve_token` |
| "Find a calendar icon" | `find_icon` |
| "Where's the homepage Figma?" | `get_figma_reference` |
| "Get assets for my project" | `get_assets` |

## 21 Components

Button, InputField, Card, Modal, BottomSheet, Avatar, Tabs, Toast, Accordion, Divider, Badge, BottomNav, Container, Spinner, Skeleton, PromoCard, ServiceCard, ContentBlock, Carousel, RatingBar, Text

## Token Categories

- **colors** — primary, secondary, sparkle, feedback, grey, global
- **typography** — heading (6), body (6), overline, button, label, code
- **spacing** — xxs to massive (10 sizes)
- **border_radius** — none to pill (8 sizes)
- **opacity** — invisible, disabled, enabled

## 1301 Icons (15 categories)

communication, media, navigation, action, content, device, image, file, social, places, toggle, time, editor, commerce, hardware

## 9 Figma References

homepage, menu, chat_page, media_page, assistants_page, tools_page, oneui_design_kit, jio_testlab, chat_input

## Assets (GitHub CDN)

All assets served via GitHub CDN — no local files needed:
- **Fonts**: 18 JioType weights (WOFF2 for web, TTF for native)
- **Animations**: HelloJio idle + listening (MP4)
- **Icons**: 71 JSX components + 1230 SVG icons

## How updates work

New version pushed to GitHub → team gets it automatically on next app restart. No action needed.

Force immediate update:
```bash
uvx --reinstall --from "git+https://github.com/sunit1986/JioBharatIQ_Server.git" jiobharatiq-server
```

## Troubleshooting

**Tools not showing?** Restart the app after adding config.

**uvx not found?** Run `curl -LsSf https://astral.sh/uv/install.sh | sh` then restart your terminal.

**Slow first run?** Normal — uvx downloads the package + Python runtime (~10 sec, cached after).

**Tools not loading on corporate network?** If your network blocks `raw.githubusercontent.com`, the uv cache can get corrupted. Fix:
```bash
rm -rf ~/.cache/uv/git-v0/
```
Then restart the app. No config change needed.

## Security

- JSON-only responses, no internal reasoning exposed
- Input sanitization + injection protection
- No file paths or secrets in output
- Method and tool whitelisting

---

Jio Design System | v3.4.0

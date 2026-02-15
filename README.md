# JDS Knowledge Server

MCP server for Jio Design System — components, tokens, icons, Figma references.

## Install (one command)

```bash
git clone https://github.com/sunit1986/JioBharatIQ_Server.git && cd JioBharatIQ_Server && ./install.sh
```

That's it. Restart Claude Desktop.

## Uninstall

```bash
cd JioBharatIQ_Server && ./uninstall.sh
```

## What you get

4 tools inside Claude Desktop:

| Ask Claude... | Tool used |
|--------------|-----------|
| "How do I use Button?" | `lookup_component` |
| "What's primary-50 color?" | `resolve_token` |
| "Find a calendar icon" | `find_icon` |
| "Where's the homepage Figma?" | `get_figma_reference` |

## 21 Components

Button, InputField, Card, Modal, BottomSheet, Avatar, Tabs, Toast, Accordion, Divider, Badge, BottomNav, Container, Spinner, Skeleton, PromoCard, ServiceCard, ContentBlock, Carousel, RatingBar, Text

## Token Categories

- **colors** — primary, secondary, sparkle, feedback, grey, global
- **typography** — heading (6), body (6), overline, button, label, code
- **spacing** — xxs to massive (10 sizes)
- **border_radius** — none to pill (8 sizes)
- **opacity** — invisible, disabled, enabled

## 15 Icon Categories (1546 icons)

communication, media, navigation, action, content, device, image, file, social, places, toggle, time, editor, commerce, hardware

## 9 Figma References

homepage, menu, chat_page, media_page, assistants_page, tools_page, oneui_design_kit, jio_testlab, chat_input

## Security

- JSON-only responses, no internal reasoning exposed
- Input sanitization + injection protection
- No file paths or secrets in output
- Method and tool whitelisting
- 147 tests passing

## Troubleshooting

**Tools not showing?** Restart Claude Desktop after install.

**Python not found?** Install from https://www.python.org/downloads/

**Permission denied?** Run `chmod +x install.sh server.py`

## Run tests

```bash
python3 test_server.py
```

---
Internal use only — Jio Design System | v1.0.0

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

5 tools inside Claude Desktop / Cursor:

| Ask Claude... | Tool used |
|--------------|-----------|
| "How do I use Button?" | `lookup_component` |
| "What's primary-50 color?" | `resolve_token` |
| "Find a calendar icon" | `find_icon` |
| "Where's the homepage Figma?" | `get_figma_reference` |
| "Get assets for my project" | `get_assets` (pass `project_dir` for auto copy commands) |

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

## Bundled Assets (ready to use)

Everything you need for prototyping is included in `assets/`:

```
assets/
  fonts/
    ttf/          18 JioType fonts (variable + all weights)
    woff2/        18 JioType web fonts (for web projects)
  animations/
    HelloJio_Breath(IdleState)_241.mp4   (idle animation)
    HelloJio_Listening_241.mp4           (listening animation)
  icons/          73 JDS icon components (.jsx)
```

### Using fonts in your prototype

**CSS/HTML:**
```css
@font-face {
  font-family: 'JioType';
  src: url('./assets/fonts/woff2/JioTypeVarW05-Regular.woff2') format('woff2'),
       url('./assets/fonts/ttf/JioTypeVar.ttf') format('truetype');
}
```

**Copy to project:** `cp -r assets/fonts/ttf/ your-project/fonts/`

### Using animations

```html
<video src="./assets/animations/HelloJio_Listening_241.mp4" autoplay loop muted></video>
```

### Using icons

```jsx
import { IcSearch } from './assets/icons/IcSearch';
```

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

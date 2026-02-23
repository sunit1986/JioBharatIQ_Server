# JDS Knowledge Server — v3.2.0

When building any prototype or UI with this design system:

---

## STEP 0 — Always do these first (before writing a single line of code)

1. Call `get_assets` to get GitHub CDN URLs for all JDS assets. Use `cdn_url` values directly in HTML — no file copying.
2. Call `lookup_component` for EVERY component you will use (Button, Card, InputField, etc.).
3. Call `resolve_token` for EVERY color, spacing, or typography value — never hardcode.

---

## STRICT RULES — no exceptions

### Fonts
- **JioType ONLY** for all text (load WOFF2 from GitHub CDN via `get_assets`)
- NEVER use: Inter, Arial, Helvetica, Roboto, system-ui, sans-serif

### Icons
- **JDS SVG library ONLY** — call `find_icon` → use `svg_path` → inline in HTML
- Available: IcMic, IcSearch, IcSendMessage, IcChevronRight/Left/Down/Up, IcClose, IcAdd, IcProfile, IcChat, IcBack, IcBurgerMenu, IcShare, IcStar, IcFavorite, IcPlay, IcPause, IcStop, IcSettings, IcNotification, IcRefresh, IcTrash, IcEditPen, IcVoice, IcDownload, IcUpload, IcDocument, IcInfo, IcWarning, IcError, IcSuccess, IcBrain, IcLanguage, IcMicOff + 1200+ SVGs
- NEVER use: Material icons, Heroicons, Feather, Bootstrap icons, or emoji as UI icons

### Colors — JDS tokens only
| Token | Value | Use for |
|-------|-------|---------|
| primary-50 | #3535f3 | Brand, CTAs, active states |
| secondary-50 | #f7ab20 | Secondary accent, highlights |
| sparkle-50 | #1eccb0 | Teal accent, success badges |
| error | #fa2f40 | Error states |
| warning | #f06d0f | Warning states |
| success | #25ab21 | Success states |
| grey-100 | #141414 | Primary text |
| grey-60 | #b5b5b5 | Disabled text |
| grey-40 | #e0e0e0 | Borders, dividers |
| grey-20 | #f5f5f5 | Skeleton, subtle bg |
| surface-ghost | #eeeeef | Input fields, cards bg |
| surface-ghost-icon | #e7e9ff | Icon button bg |
| surface-bold | #3900ad | Speak button, bold CTA |
| text-high | #141414 | Primary text |
| text-low | rgba(25,27,30,0.65) | Placeholder, secondary |
| icon-medium | #170054 | Icon color |

NEVER use: #a855f7, #22c55e, #f97316, #ec4899, or any non-JDS arbitrary color.

### Typography — JDS type scale only
| Role | Token | Size | Weight |
|------|-------|------|--------|
| Display | display-l/m/s | 52/44/36px | Black, -3% letter-spacing |
| Headline | headline-l to 3xs | 32-18px | Black/Bold |
| Title | title-l to 3xs | 20-13px | Bold |
| Body | body-2xl to 3xs | 20-11px | Medium |
| Label | label-2xl to 4xs | 16-8px | Bold |
| Overline | overline | 10px | Bold, UPPERCASE |

NEVER use ad-hoc sizes like 11px, 12px, 17px outside the scale.

### Components
- ALWAYS `lookup_component` before implementing any JDS component
- Use exact props, tokens, and sizing from the spec — no custom variants

### Opacity tokens
- invisible = 0
- disabled = 0.38
- enabled = 1.0
- overlay-tint = 0.4
- NEVER use arbitrary values like 0.5, 0.7, 0.9

### Loading states
- Content loading → **Skeleton (shimmer, bg=#f5f5f5)** — NEVER spinners for content
- Action loading → **Spinner** (inside buttons, for API calls)

### Mode
- **Light mode by default** for ALL prototypes
- Dark mode ONLY if the user explicitly requests it

---

## Prototype format (mandatory for HTML prototypes)

- Single file: one `index.html` with all CSS + JS inline. No build tools, no CDN libraries.
- Canvas: 360px wide mobile (JDS standard)
- Phone frame: rounded corners (48px), dark border, notch, status bar (time + signal + battery)
- Left sidebar: lists all screens by name. Click = show in phone. Active screen highlighted.
- UX directions: show 3 different interaction models, not just visual variants
- Content: real Indian names, ₹ amounts, Hindi/English — no Lorem Ipsum, no placeholders
- States: default + loading (skeleton) + empty + error + success — all accessible from sidebar

---

## JBIQ / Branding rules

- Brand name = **JBIQ** (not "Jio Omni AI")
- AI avatar = 4-dot 2×2 grid (blue=#3535f3, orange=#f7ab20, purple=#6464ff, teal=#1eccb0)
- HelloJio animation: 148×148px full-screen, 32×32px inline indicator
- Speak button: bg=#3900ad, radius=999px, padding=12px 20px, white text JioType Bold 16px
- Voice input icon: IcMic (JDS), not custom mic SVGs

---

## Figma references

| Design | File Key | Notes |
|--------|----------|-------|
| Homepage v2 | yvWQ7pqZSgFIfO0XrzY1me | node 13157:2011 — default AI assistant home |
| Chat Input | b95Apii4f27AoRxhm0nJZq | node 20031:7407 — canonical chat input |
| Exploration (new direction) | gkZ1yhR3PeuOiExiQD1P5r | Voice-first UX, personalized |
| OneUI Design Kit | A1kqKEXc8srjVxPVyFNsQq | JDS component library |
| Jio Testlab | SjyssHuM5x8fcnriezopvK | Component API specs |
| AI Summit | JMHVLSCpZ0ZHlOu1YbZVu1 | Conversational AI patterns |
| Widgets | M2U8HzavyLSL7T9KSdVpU4 | Commerce/travel/food widgets |

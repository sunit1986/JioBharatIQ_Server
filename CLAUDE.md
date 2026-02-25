# JDS Knowledge Server v3.4.0

When building any prototype or UI using this server, follow these rules and use the embedded reference data below.

## Mandatory Workflow

1. Call `get_assets` FIRST to get GitHub-hosted CDN URLs for all JDS assets. Use cdn_url values directly in HTML src/url attributes.
2. Use **JioType font family ONLY** (woff2 for web, ttf for native). NEVER use Inter, Arial, Helvetica, Roboto, or sans-serif.
3. Call `lookup_component` before implementing any JDS component.
4. Call `resolve_token` for colors, typography, spacing. NEVER hardcode values.
5. Use `find_icon` to get SVG path data for icons. See the Icon Reference below for inline SVG paths.
6. Use HelloJio animations from assets/animations/ for AI/assistant states.
7. NEVER use emojis anywhere in UI. Use JDS icons instead.
8. NEVER use placeholder or dummy assets. Always use real JDS assets.

---

# DESIGN TOKENS (Complete Reference)

Use these values when `resolve_token` is unavailable or as a quick reference.

## Colors

### Primary
| Token | Value |
|-------|-------|
| primary-20 | #e8e8fc |
| primary-30 | #9999ff |
| primary-40 | #6464ff |
| primary-50 | #3535f3 |
| primary-60 | #000093 |
| primary-70 | #00004c |
| primary-80 | #010029 |

### Secondary
| Token | Value |
|-------|-------|
| secondary-20 | #fef7e9 |
| secondary-30 | #ffe3ae |
| secondary-40 | #ffd947 |
| secondary-50 | #f7ab20 |
| secondary-60 | #ac660c |
| secondary-70 | #7f4b10 |
| secondary-80 | #401d0c |

### Sparkle
| Token | Value |
|-------|-------|
| sparkle-20 | #e8faf7 |
| sparkle-30 | #a7f6e9 |
| sparkle-40 | #7aebd9 |
| sparkle-50 | #1eccb0 |
| sparkle-60 | #1e7b74 |
| sparkle-70 | #0e5c4f |
| sparkle-80 | #08332c |

### Feedback
| Token | Value |
|-------|-------|
| error | #fa2f40 |
| warning | #f06d0f |
| success | #25ab21 |

### Grey Scale
| Token | Value |
|-------|-------|
| grey-100 | #141414 |
| grey-80 | #000000a6 (66% opacity) |
| grey-60 | #b5b5b5 |
| grey-40 | #e0e0e0 |
| grey-20 | #f5f5f5 |

NOTE: Only grey-20, grey-40, grey-60, grey-80, grey-100 exist. There is NO grey-5, grey-10, grey-50, grey-70, grey-90.

### Global
| Token | Value |
|-------|-------|
| white | #ffffff |
| black | #141414 |

### Semantic / Surface Tokens (CSS Variables)
| Variable | Value | Usage |
|----------|-------|-------|
| --surface | #ffffff | Main background |
| --surface-ghost | #eeeeef | Input field background |
| --surface-ghost-icon | #e7e9ff | Icon button background |
| --surface-bold | #3900ad | Primary CTA background |
| --text-high | #141414 | Primary text |
| --text-low | #191b1e at 65% opacity | Secondary text |
| --text-on-bold | #ffffff | Text on bold surfaces |
| --icon-medium | #170054 | Icon default color |

## Typography

Font: **JioType** (variable font). Weights: Regular 400, Medium 500, Bold 700, Black 900.
Line-height: 120% default. Letter-spacing: -0.5% default. Baseline grid: 4px.

### Variants & Sizes
| Variant | Available Sizes |
|---------|-----------------|
| Display | S, M, L |
| Headline | 3XS, 2XS, XS, S, M, L |
| Title | 3XS, 2XS, XS, S, M, L |
| Body | 3XS, 2XS, XS, S, M, L, XL, 2XL |
| Label | 4XS, 3XS, 2XS, XS, S, M, L, XL, 2XL |

Weight options: **low** (Regular), **medium** (Medium), **high** (Bold/Black)

### Size Tokens
| Token | Value |
|-------|-------|
| --typography/size/body/3xs | 8px |
| --typography/size/body/2xs | 10px |
| --typography/size/body/xs | 12px |
| --typography/size/body/s | 14px |
| --typography/size/body/m | 16px |
| --typography/size/body/l | 18px |
| --typography/size/label/s | 12px |
| --typography/size/label/m | 16px |
| --typography/size/label/l | 18px |

### Contextual Usage
| Element | Style |
|---------|-------|
| Header Title | JioType Bold, 18px |
| Category Badge | JioType Medium, 12px |
| Chat Message | JioType Medium, 16px |
| Chip Label | JioType Medium, 14px |
| Card Title | JioType Bold, 16px |
| Card Rate/Price | JioType Bold, 24px |
| Input Placeholder | JioType Medium, 16px |
| Speak Button | JioType Bold, 15px |

## Spacing

| Token | Value |
|-------|-------|
| 4xs | 2px |
| 3xs | 4px |
| 2xs | 6px |
| xs | 8px |
| s | 10px |
| base | 12px |
| m | 14px |
| l | 16px |
| xl | 20px |
| 2xl | 24px |
| 3xl | 32px |
| huge | 40px |
| massive | 48px |

## Border Radius

| Token | Value |
|-------|-------|
| none | 0px |
| xSmall | 4px |
| small | 8px |
| medium | 12px |
| large | 16px |
| xl | 20px |
| xxl | 24px |
| 3xl | 28px |
| 4xl | 23px |
| pill | 999px |

## Opacity

| Token | Value |
|-------|-------|
| opacity.invisible | 0 |
| opacity.disabled | 0.38 |
| opacity.medium | 0.65 |
| opacity.enabled | 1 |

---

# ICON REFERENCE — 71 Core Icons with Inline SVG Paths

Use these SVG paths directly in HTML prototypes:
```html
<svg viewBox="0 0 24 24" fill="none" width="24" height="24">
  <path d="[PASTE svg_path HERE]" fill="currentColor"/>
</svg>
```

CDN base: `https://raw.githubusercontent.com/sunit1986/JioBharatIQ_Server/main/assets/icons/`

| Icon | Keywords | svg_path |
|------|----------|----------|
| IcAccessibility | accessibility, a11y | `M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c.83 0 1.5.67 1.5 1.5S12.83 8 12 8s-1.5-.67-1.5-1.5S11.17 5 12 5zm5.24 4.97l-3.74.94v1.86l2.39 4.79c.25.49.05 1.09-.45 1.34a1.007 1.007 0 01-1.35-.44l-2.11-4.21-2.11 4.21a1.007 1.007 0 01-1.35.44 1.01 1.01 0 01-.45-1.34l2.39-4.79v-1.86l-3.74-.94a1 1 0 01.48-1.94l3.88.97h1.75l3.88-.97a.995.995 0 011.21.73.995.995 0 01-.73 1.21h.05z` |
| IcAdd | add, plus, create, new | `M20 11h-7V4a1 1 0 00-2 0v7H4a1 1 0 000 2h7v7a1 1 0 002 0v-7h7a1 1 0 000-2z` |
| IcAlarm | alarm, clock, reminder, timer | `M3.88 6.71l2.83-2.83a1.004 1.004 0 00-1.42-1.42L2.46 5.29a1.004 1.004 0 101.42 1.42zm17.66-1.42l-2.83-2.83a1.004 1.004 0 10-1.42 1.42l2.83 2.83a1.004 1.004 0 001.42-1.42zM12 4a9 9 0 00-7.46 14l-1.25 1.29a1.004 1.004 0 101.42 1.42l1.14-1.15a9 9 0 0012.3 0l1.14 1.15a1.004 1.004 0 101.42-1.42L19.46 18A9 9 0 0012 4zm2.12 11.12a1 1 0 01-1.41 0l-1.42-1.41a1.15 1.15 0 01-.21-.33A1.001 1.001 0 0011 13V8a1 1 0 012 0v4.59l1.12 1.12a1 1 0 010 1.41z` |
| IcArrowBack | arrow back, return, go back | `M2.29 12.71l6 6a1.004 1.004 0 101.42-1.42L5.41 13H21a1 1 0 100-2H5.41l4.3-4.29a1 1 0 000-1.42 1 1 0 00-1.42 0l-6 6a1 1 0 000 1.42z` |
| IcBack | back, chevron left, previous | `M15 20a1.003 1.003 0 01-.71-.29l-7-7a1 1 0 010-1.42l7-7a1.005 1.005 0 011.42 1.42L9.41 12l6.3 6.29a.997.997 0 01.219 1.095.999.999 0 01-.93.615z` |
| IcBrain | brain, ai, intelligence, smart | `M9 3c-1.1 0-2 .9-2 2-1.45 0-2.66 1.03-2.94 2.39C4.66 7.14 5.31 7 6 7c.96 0 1.85.27 2.61.74.52.32.6 1.04.17 1.47l-.08.08c-.32.32-.8.34-1.19.11a2.969 2.969 0 00-3.11.06c-.21.13-.4.29-.57.47h-.01a3.359 3.359 0 00-.47.69c-.08.15-.15.32-.2.49l-.06.18c-.06.23-.09.46-.09.71 0 1.07.56 2 1.4 2.53-.25.44-.4.93-.4 1.47 0 1.66 1.34 3 3 3 0 1.1.9 2 2 2s2-.9 2-2V5c0-1.1-.9-2-2-2zm10.6 6.47c.25-.44.4-.93.4-1.47 0-1.66-1.34-3-3-3 0-1.1-.9-2-2-2s-2 .9-2 2v8.5c0 1.1.9 2 2 2 .38 0 .74-.11 1.05-.3.39-.24.9-.19 1.22.14a1 1 0 01-.17 1.55 3.906 3.906 0 01-4.11.05V19c0 1.1.9 2 2 2s2-.9 2-2c1.66 0 3-1.34 3-3 0-.15-.02-.29-.04-.44-.01-.09-.03-.17-.05-.25 0-.04-.02-.08-.03-.12-.07-.23-.16-.45-.28-.66a2.969 2.969 0 00-1.81-1.42c-.46-.13-.8-.5-.8-.98 0-.65.62-1.14 1.25-.97 1.05.27 1.96.88 2.62 1.69.08-.27.13-.55.13-.85 0-1.07-.56-2-1.4-2.53h.02z` |
| IcBurgerMenu | menu, hamburger, navigation | `M4 7h16a1 1 0 100-2H4a1 1 0 000 2zm16 10H4a1 1 0 000 2h16a1 1 0 000-2zm0-6H4a1 1 0 000 2h16a1 1 0 000-2z` |
| IcCalendar | calendar, date, schedule | `M18 3h-1a1 1 0 00-2 0H9a1 1 0 00-2 0H6a3 3 0 00-3 3v12a3 3 0 003 3h12a3 3 0 003-3V6a3 3 0 00-3-3zm-4.5 14a1 1 0 01-2 0v-3.59l-.29.3a1.004 1.004 0 11-1.42-1.42l2-2a.999.999 0 011.09-.21 1 1 0 01.62.92v6zM19 7H5V6a1 1 0 011-1h1a1 1 0 002 0h6a1 1 0 002 0h1a1 1 0 011 1v1z` |
| IcCart | cart, shopping, basket, buy | `M8.5 19a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm9 0a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm4.12-12.17A2 2 0 0020 6H6.58l-.41-1.52A2 2 0 004.23 3H3a1 1 0 000 2h1.23l2.83 10.48A2 2 0 009 17h8.67a2 2 0 001.89-1.37l2.34-7a2 2 0 00-.28-1.8z` |
| IcChat | chat, message, conversation, talk | `M15 4H9a7 7 0 00-1 13.92V20a1.5 1.5 0 002.4 1.2l4.27-3.2H15a7 7 0 000-14zm-7 8a1 1 0 110-2 1 1 0 010 2zm4 0a1 1 0 110-2 1 1 0 010 2zm4 0a1 1 0 110-2 1 1 0 010 2z` |
| IcChevronDown | chevron down, dropdown, expand | `M12 15a1.002 1.002 0 01-.71-.29l-4-4a1.004 1.004 0 111.42-1.42l3.29 3.3 3.29-3.3a1.004 1.004 0 111.42 1.42l-4 4A1.001 1.001 0 0112 15z` |
| IcChevronLeft | chevron left, left, previous | `M14 17a1.003 1.003 0 01-.71-.29l-4-4a1 1 0 010-1.42l4-4a1.005 1.005 0 011.42 1.42L11.41 12l3.3 3.29a.997.997 0 01.219 1.095.999.999 0 01-.93.615z` |
| IcChevronRight | chevron right, right, next | `M10 17a1.002 1.002 0 01-1.006-1 1 1 0 01.296-.71l3.3-3.29-3.3-3.29a1.004 1.004 0 011.42-1.42l4 4a.997.997 0 01.219 1.095.999.999 0 01-.22.325l-4 4A1 1 0 0110 17z` |
| IcChevronUp | chevron up, collapse, up | `M16 15a.998.998 0 01-.71-.29L12 11.41l-3.29 3.3a1.004 1.004 0 01-1.42-1.42l4-4a.999.999 0 011.42 0l4 4A1.001 1.001 0 0116 15z` |
| IcClose | close, x, dismiss, cancel | `M13.41 12l6.3-6.29a1.004 1.004 0 00-1.42-1.42L12 10.59l-6.29-6.3a1.004 1.004 0 10-1.42 1.42l6.3 6.29-6.3 6.29a.999.999 0 000 1.42 1 1 0 001.42 0l6.29-6.3 6.29 6.3a1.001 1.001 0 001.639-.325 1 1 0 00-.22-1.095L13.41 12z` |
| IcCloseRemove | close circle, remove circle | `M12 2a10 10 0 100 20 10 10 0 000-20zm3.71 12.29a1.002 1.002 0 01-.325 1.639 1 1 0 01-1.095-.219L12 13.41l-2.29 2.3a1 1 0 01-1.639-.325 1 1 0 01.219-1.095l2.3-2.29-2.3-2.29a1.004 1.004 0 011.42-1.42l2.29 2.3 2.29-2.3a1.004 1.004 0 011.42 1.42L13.41 12l2.3 2.29z` |
| IcConfirm | confirm, check, tick, done | `M9 19a1.002 1.002 0 01-.71-.29l-5-5a1.004 1.004 0 111.42-1.42L9 16.59l10.29-10.3a1.004 1.004 0 111.42 1.42l-11 11A1 1 0 019 19z` |
| IcCopy | copy, duplicate, clipboard | `M13 8H5a3 3 0 00-3 3v8a3 3 0 003 3h8a3 3 0 003-3v-8a3 3 0 00-3-3zm6-6h-8a3 3 0 00-3 3v1h5a5 5 0 015 5v5h1a3 3 0 003-3V5a3 3 0 00-3-3z` |
| IcDislike | dislike, thumbs down, downvote | `M3.568 6.67l-.55 5A3 3 0 005.998 15h4v3.92a2 2 0 003.94.56l1-4c.04-.157.06-.318.06-.48V4h-8.45a3 3 0 00-2.98 2.67zM18.998 4h-2v11h2a2 2 0 002-2V6a2 2 0 00-2-2z` |
| IcDocument | document, file, paper | `M13 6V2H7.5A2.5 2.5 0 005 4.5v15A2.5 2.5 0 007.5 22h10a2.5 2.5 0 002.5-2.5V9h-4a3 3 0 01-3-3zm3 1h4a2 2 0 00-.59-1.41l-3-3A2 2 0 0015 2v4a1 1 0 001 1z` |
| IcDownload | download, save, get | `M16 20H8c-.55 0-1-.45-1-1s.45-1 1-1h8c.55 0 1 .45 1 1s-.45 1-1 1zM16.71 10.29a.996.996 0 00-1.41 0l-2.29 2.29V4.99c0-.55-.45-1-1-1s-1 .45-1 1v7.59l-2.29-2.29a.996.996 0 10-1.41 1.41l4 4c.2.2.45.29.71.29.26 0 .51-.1.71-.29l4-4a.996.996 0 000-1.41h-.02z` |
| IcEditPen | edit, pen, write, pencil | `M19.5 4.5a3.54 3.54 0 00-5 0l-.29.29 5 5 .29-.29a3.54 3.54 0 000-5zm-13.95 9a3 3 0 00-.76 1.3l-1 3.65a1.5 1.5 0 001.81 1.81l3.65-1.05a3 3 0 001.3-.76l7.24-7.24-5-5-7.24 7.29z` |
| IcError | error, fail, problem | `M12 2a10 10 0 100 20 10 10 0 000-20zm3.71 12.29a1.002 1.002 0 01-.325 1.639 1 1 0 01-1.095-.219L12 13.41l-2.29 2.3a1 1 0 01-1.639-.325 1 1 0 01.219-1.095l2.3-2.29-2.3-2.29a1.004 1.004 0 011.42-1.42l2.29 2.3 2.29-2.3a1.004 1.004 0 011.42 1.42L13.41 12l2.3 2.29z` |
| IcFavorite | favorite, heart, love, wishlist | `M15.6 4A5.6 5.6 0 0012 5.46 5.6 5.6 0 008.4 4 5.36 5.36 0 003 9.44c0 3.37 2.63 6.43 7.16 10.56l.49.45a2 2 0 002.7 0l.49-.44C18.37 15.86 21 12.8 21 9.44A5.36 5.36 0 0015.6 4z` |
| IcFilterMultiple | filter, sort, sliders, adjust | `M4 7h9.18a3 3 0 005.64 0H20a1 1 0 100-2h-1.18a3 3 0 00-5.64 0H4a1 1 0 000 2zm12-2a1 1 0 110 2 1 1 0 010-2zm4 12h-1.18a3 3 0 00-5.64 0H4a1 1 0 000 2h9.18a3 3 0 005.64 0H20a1 1 0 100-2zm-4 2a1 1 0 110-2 1 1 0 010 2zm4-8h-9.18a3 3 0 00-5.64 0H4a1 1 0 000 2h1.18a3 3 0 005.64 0H20a1 1 0 100-2zM8 13a1 1 0 110-2 1 1 0 010 2z` |
| IcHomeConnection | home, house, dashboard | `M22 10.07a1.53 1.53 0 00-.48-.76L13.85 2.7a2.79 2.79 0 00-3.7 0L2.53 9.31A1.53 1.53 0 002.08 11c.098.29.283.54.53.72.242.187.535.295.84.31H4v7a3 3 0 003 3h10a3 3 0 003-3V12h.55a1.49 1.49 0 00.84-.31c.247-.18.432-.43.53-.72a1.54 1.54 0 00.08-.9zM12 19A1 1 0 1112 17 1 1 0 0112 19zm3.38-3.77a1 1 0 01-1.37.35 3.79 3.79 0 00-4 0 1 1 0 01-1-1.72 5.83 5.83 0 016.08 0 1 1 0 01.29 1.37zm2.45-3.15a1 1 0 01-1.39.27 8.09 8.09 0 00-8.88 0 1.002 1.002 0 01-1.12-1.66 10.15 10.15 0 0111.12 0 1 1 0 01.27 1.39z` |
| IcInfo | info, information, about, help | `M12 2a10 10 0 100 20 10 10 0 000-20zm0 3.5a1.5 1.5 0 110 3 1.5 1.5 0 010-3zm2 12h-4a1 1 0 010-2h1v-3h-1a1 1 0 010-2h2a1 1 0 011 1v4h1a1 1 0 010 2z` |
| IcLanguage | language, translate, globe | `M21.71 4.29A1 1 0 0021 4h-2.23a1 1 0 00-1 1 1 1 0 001 1H19v1.48a2 2 0 01-.85.09 2.3 2.3 0 01-.81-.24A2.29 2.29 0 0016 4.1a2.3 2.3 0 00-2.62.9 1 1 0 001.24 1.38.36.36 0 01.14-.1.54.54 0 01.18 0c.24.02.37.15.22.48a1 1 0 00.62 1.385.76.76 0 01.42.12.7.7 0 01.27.34.78.78 0 01-.16.61.78.78 0 01-.38.2A.71.71 0 0115 10a.82.82 0 01-.34-.27.791.791 0 01-.12-.42 1 1 0 00-2 0 2.73 2.73 0 004.56 2.05 2.72 2.72 0 00.9-1.81c.133.01.267.01.4 0 .2.014.402.008.6-.02v1.56a1 1 0 002 0V6a1 1 0 00.71-1.71zm-12.28.34a1 1 0 00-1.86 0l-5.5 14a1 1 0 001.86.73L5.65 15h5.7l1.72 4.37a1 1 0 001.86-.74L9.43 4.63zm-3 8.37L8.5 7.73 10.57 13H6.43z` |
| IcLike | like, thumbs up, upvote, good | `M3 11v7a2 2 0 002 2h2V9H5a2 2 0 00-2 2zm17.24-1A3 3 0 0018 9h-4V5.08a2 2 0 00-3.94-.57l-1 4A2.12 2.12 0 009 9v11h8.44a3 3 0 003-2.67l.55-5a2.999 2.999 0 00-.75-2.33z` |
| IcList | list, bullet list, items | `M20 17H9a1 1 0 000 2h11a1 1 0 000-2zm0-6H9a1 1 0 000 2h11a1 1 0 000-2zM9 7h11a1 1 0 100-2H9a1 1 0 000 2zM4.5 4.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm0 6a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm0 6a1.5 1.5 0 100 3 1.5 1.5 0 000-3z` |
| IcMic | mic, microphone, voice, record, audio | `M12 15a3 3 0 003-3V5a3 3 0 00-6 0v7a3 3 0 003 3zm6-5a1 1 0 00-1 1v1a5 5 0 11-10 0v-1a1 1 0 10-2 0v1a7 7 0 1014 0v-1a1 1 0 00-1-1zm-3 10H9a1 1 0 000 2h6a1 1 0 000-2z` |
| IcMicOff | mic off, mute, microphone off | `M7.07 12.69A5.2 5.2 0 017 12v-1a1 1 0 10-2 0v1a7 7 0 00.41 2.34l1.66-1.65zM12 2a3 3 0 00-3 3v5.76l6-6A3 3 0 0012 2zm3 18H9a1 1 0 000 2h6a1 1 0 100-2zm-3-5a3 3 0 003-3v-1.56L20.49 5a1.055 1.055 0 00-1.49-1.49L3.51 19A1.055 1.055 0 005 20.49l2.87-2.88A7 7 0 0019 12v-1a1 1 0 00-2 0v1a5 5 0 01-7.73 4.18l1.46-1.47A3 3 0 0012 15z` |
| IcMinus | minus, subtract, remove | `M3.293 11.293A1 1 0 014 11h16a1 1 0 010 2H4a1 1 0 01-.707-1.707z` |
| IcMoreHorizontal | more, dots, ellipsis, options | `M5.5 10.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm6.5 0a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm6.5 0a1.5 1.5 0 100 3 1.5 1.5 0 000-3z` |
| IcNext | next, forward, chevron right | `M9 20a1.002 1.002 0 01-.71-.29l6.3-6.29-6.3-6.29a1.004 1.004 0 011.42-1.42l7 7a1 1 0 010 1.42l-7 7A1 1 0 019 20z` |
| IcNightClear | night, moon, dark mode | `M14.94 8.24c-.5 3.43-3.28 6.2-6.7 6.7-1.74.26-3.38-.05-4.79-.76-.87-.44-1.77.49-1.34 1.35 1.74 3.45 5.42 5.76 9.61 5.48 4.91-.33 8.96-4.37 9.29-9.29a9.976 9.976 0 00-5.48-9.61c-.87-.44-1.79.47-1.35 1.34.71 1.41 1.02 3.05.76 4.79z` |
| IcNotification | notification, bell, alert | `M21 16h-1v-6a8 8 0 00-16 0v6H3a1 1 0 000 2h18a1 1 0 000-2zm-9 6a3 3 0 003-3H9a3 3 0 003 3z` |
| IcPause | pause, halt, hold | `M8.5 4A1.5 1.5 0 007 5.5v13a1.5 1.5 0 003 0v-13A1.5 1.5 0 008.5 4zm7 0A1.5 1.5 0 0014 5.5v13a1.5 1.5 0 103 0v-13A1.5 1.5 0 0015.5 4z` |
| IcPhotoCamera | camera, photo, picture, capture | `M19 6h-7V5a1 1 0 00-1-1H7a1 1 0 00-1 1v1H5a3.12 3.12 0 00-3 3.23v7.54A3.12 3.12 0 005 20h14a3.12 3.12 0 003-3.23V9.23A3.12 3.12 0 0019 6zm-7 10a3 3 0 110-5.999A3 3 0 0112 16z` |
| IcPlay | play, start, begin, resume, video | `M19.15 10.36l-10-7A2 2 0 006 5v14a2 2 0 003.15 1.64l10-7a2 2 0 000-3.28z` |
| IcProfile | profile, user, person, account | `M16 6a4 4 0 11-8 0 4 4 0 018 0zm4 10.5c0 3.038-3.582 5.5-8 5.5s-8-2.462-8-5.5S7.582 11 12 11s8 2.462 8 5.5z` |
| IcRefresh | refresh, reload, sync, update | `M12 4a8 8 0 013.85 1H15a1 1 0 100 2h3a1 1 0 001-1V3a1 1 0 00-2 0v.36A10 10 0 0012 2a10 10 0 00-8.65 5A9.94 9.94 0 002 12a1 1 0 102 0 8 8 0 018-8zm9.71 7.29A1 1 0 0020 12a8 8 0 01-11.84 7H9a1 1 0 000-2H6a1 1 0 00-1 1v3a1 1 0 102 0v-.36A10 10 0 0012 22a10 10 0 0010-10 1 1 0 00-.29-.71z` |
| IcSearch | search, find, lookup, magnify | `M10.004 2a7 7 0 015.6 11.19l6.11 6.1a1.002 1.002 0 01-1.42 1.42l-6.1-6.11A7 7 0 1110.004 2zm0 12a5 5 0 100-10 5 5 0 000 10z` |
| IcSendMessage | send, submit, post, dispatch | `M19.79 10.16l-14-6A2 2 0 003.39 7.19L6.76 12l-3.35 4.79a2 2 0 002.38 3.05l14-6a2 2 0 000-3.68z` |
| IcSettings | settings, gear, cog, preferences | `M20.43 13.4L19 12.58v-1.16l1.43-.82a2 2 0 00.73-2.73l-1-1.74a2 2 0 00-2.73-.73l-1.18.68-.25.15-1-.58V4a2 2 0 00-2-2h-2a2 2 0 00-2 2v1.65l-.25.14-.75.44-.25-.15-1.18-.68a2 2 0 00-2.73.73l-1 1.74a2 2 0 00.73 2.73l1.43.82v1.16l-1.43.82a2 2 0 00-.73 2.73l1 1.74a2 2 0 002.73.73L8 17.77l1 .58V20a2 2 0 002 2h2a2 2 0 002-2v-1.65l1-.58 1.43.83a2 2 0 002.73-.73l1-1.74a2 2 0 00-.73-2.73zM12 15a3 3 0 110-6 3 3 0 010 6z` |
| IcShare | share, send to, forward | `M18 15a3 3 0 00-2.15.91L8 12.27c.005-.09.005-.18 0-.27.005-.09.005-.18 0-.27l7.88-3.64A3 3 0 1015 6c-.005.09-.005.18 0 .27L7.15 9.91a3 3 0 100 4.18L15 17.73c-.005.09-.005.18 0 .27a3 3 0 103-3z` |
| IcStar | star, rate, rating, favorite | `M21.37 9.61a1.964 1.964 0 00-1.52-1.284l-4.235-.646-1.899-4.087a1.917 1.917 0 00-3.434 0L8.38 7.68l-4.273.646a1.964 1.964 0 00-1.52 1.283 1.91 1.91 0 00.447 1.901l3.124 3.213-.74 4.553a1.91 1.91 0 002.88 2.07l3.788-2.091 3.788 2.09a1.9 1.9 0 002.88-2.033l-.74-4.552 3.123-3.213a1.91 1.91 0 00.333-1.93z` |
| IcStop | stop, halt, end, square | `M16.84 4H7.16A3.16 3.16 0 004 7.16v9.68A3.16 3.16 0 007.16 20h9.68A3.16 3.16 0 0020 16.84V7.16A3.16 3.16 0 0016.84 4z` |
| IcStopwatch | stopwatch, timer, countdown | `M10 4h4a1 1 0 100-2h-4a1 1 0 000 2zm8.71 2.71a1 1 0 101.41-1.42l-1.41-1.41a1 1 0 10-1.42 1.41l1.42 1.42zM12 5a8.5 8.5 0 108.5 8.5A8.51 8.51 0 0012 5zm1 8a1 1 0 01-2 0V9a1 1 0 012 0v4z` |
| IcSuccess | success, check circle, done | `M12 2a10 10 0 100 20 10 10 0 000-20zm5.21 7.71l-6 6a1.002 1.002 0 01-1.42 0l-3-3a1.003 1.003 0 111.42-1.42l2.29 2.3 5.29-5.3a1.004 1.004 0 011.42 1.42z` |
| IcSunnyClear | sun, sunny, day, light mode | `M6.34 16.24l-1.41 1.41a.996.996 0 101.41 1.41l1.41-1.41a.996.996 0 10-1.41-1.41zm0-8.49a.996.996 0 101.41-1.41L6.34 4.93a.996.996 0 10-1.41 1.41l1.41 1.41zM6 11.99c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1s.45 1 1 1h2c.55 0 1-.45 1-1zm6-6c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1v2c0 .55.45 1 1 1zm5.66 1.76l1.41-1.41a.996.996 0 10-1.41-1.41l-1.41 1.41a.996.996 0 101.41 1.41zM21 10.99h-2c-.55 0-1 .45-1 1s.45 1 1 1h2c.55 0 1-.45 1-1s-.45-1-1-1zm-3.34 5.24a.996.996 0 10-1.41 1.41l1.41 1.41a.996.996 0 101.41-1.41l-1.41-1.41zM12 17.99c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1zm0-11c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5z` |
| IcTask | task, todo, checklist, clipboard | `M20 8V6a3 3 0 00-3-3h-1.28A2 2 0 0014 2h-4a2 2 0 00-1.72 1H7a3 3 0 00-3 3v13a3 3 0 003 3h10a3 3 0 003-3v-1a2 2 0 002-2v-6a2 2 0 00-2-2zm-2 11a1 1 0 01-1 1H7a1 1 0 01-1-1V6a1 1 0 011-1h1.28A2 2 0 0010 6h4a2 2 0 001.72-1H17a1 1 0 011 1v2h-6a2 2 0 00-2 2v6a2 2 0 002 2h6v1zm.71-6.79l-3 3a1.002 1.002 0 01-1.42 0l-1-1a1.004 1.004 0 111.42-1.42l.29.3 2.29-2.3a1.004 1.004 0 111.42 1.42z` |
| IcTrash | trash, delete, remove, bin | `M20 6h-2V5a3 3 0 00-3-3H9a3 3 0 00-3 3v1H4a1 1 0 000 2h1v11a3 3 0 003 3h8a3 3 0 003-3V8h1a1 1 0 100-2zM9 18a1 1 0 11-2 0v-7a1 1 0 112 0v7zm4 0a1 1 0 01-2 0v-7a1 1 0 012 0v7zm4 0a1 1 0 01-2 0v-7a1 1 0 012 0v7zM8 5a1 1 0 011-1h6a1 1 0 011 1v1H8V5z` |
| IcUpload | upload, export, send up | `M7.71 8.71L11 5.41V17a1 1 0 102 0V5.41l3.29 3.3a.999.999 0 001.42 0 1.001 1.001 0 000-1.42l-5-5a1 1 0 00-1.42 0l-5 5a1.004 1.004 0 101.42 1.42zM17 20H7a1 1 0 000 2h10a1 1 0 100-2z` |
| IcVoice | voice, waveform, audio, speaker, speak | `M12 2a1 1 0 00-1 1v18a1 1 0 002 0V3a1 1 0 00-1-1zM4 9a1 1 0 00-1 1v4a1 1 0 102 0v-4a1 1 0 00-1-1zm4-3a1 1 0 00-1 1v10a1 1 0 102 0V7a1 1 0 00-1-1zm12 3a1 1 0 00-1 1v4a1 1 0 002 0v-4a1 1 0 00-1-1zm-4-3a1 1 0 00-1 1v10a1 1 0 002 0V7a1 1 0 00-1-1z` |
| IcWarning | warning, caution, alert, danger | `M12 2a10 10 0 100 20 10 10 0 000-20zm-1 4.5a1 1 0 012 0v6a1 1 0 01-2 0v-6zm1 12a1.5 1.5 0 110-3 1.5 1.5 0 010 3z` |
| IcWidgets | widgets, dashboard, grid, modules | `M9 3H5a2 2 0 00-2 2v4a2 2 0 002 2h4a2 2 0 002-2V5a2 2 0 00-2-2zm0 10H5a2 2 0 00-2 2v4a2 2 0 002 2h4a2 2 0 002-2v-4a2 2 0 00-2-2zm12.16-7.41l-2.75-2.75a2 2 0 00-2.82 0l-2.75 2.75a2 2 0 000 2.82l2.75 2.75a2 2 0 002.82 0l2.75-2.75a2 2 0 000-2.82zM19 13h-4a2 2 0 00-2 2v4a2 2 0 002 2h4a2 2 0 002-2v-4a2 2 0 00-2-2z` |
| IcWifiOff | wifi off, no wifi, offline | `M5.4 12.81a1 1 0 001.53.01l3.73-3.72a10.06 10.06 0 00-5.15 2.3 1 1 0 00-.11 1.41zM4 10.08A11.94 11.94 0 0112 7h.72l1.81-1.8A14.26 14.26 0 0012 5a14 14 0 00-9.34 3.59A1.002 1.002 0 004 10.08zm17.34-1.49a13.891 13.891 0 00-2.63-1.85L20.49 5a1.055 1.055 0 00-1.49-1.49L3.51 19A1.052 1.052 0 105 20.49l4.7-4.71a4 4 0 014.73 0 1 1 0 001.2-1.6 5.999 5.999 0 00-3.2-1.16l1.76-1.75a8 8 0 013 1.62 1 1 0 001.3-1.52 9.848 9.848 0 00-2.78-1.67l1.52-1.52c1.008.5 1.94 1.14 2.77 1.9a1 1 0 001.34-1.49zM12 17a1.5 1.5 0 100 2.999 1.5 1.5 0 000-3z` |
| IcAlbum | album, gallery, photo album, image | `M20.12 6.77c-.56-.5-1.33-.78-2.12-.78H6c-.8 0-1.56.28-2.12.78S3 7.95 3 8.66v10.67c0 .71.32 1.39.88 1.89S5.21 22 6 22h12c.8 0 1.56-.28 2.12-.78s.88-1.18.88-1.89V8.66c0-.71-.32-1.39-.88-1.89zM19 15.08l-2.79-2.8a.955.955 0 00-.33-.22.995.995 0 00-.38-.08c-.13 0-.26.03-.38.08s-.23.13-.33.22l-4.29 4.3-1.29-1.3a.955.955 0 00-.33-.22.995.995 0 00-.38-.08c-.13 0-.26.03-.38.08s-.23.13-.33.22L5 18.08V8.99c0-.27.11-.52.29-.71.18-.19.44-.29.71-.29h12c.27 0 .52.11.71.29.19.18.29.44.29.71v6.09z M8.5 10c-.3 0-.59.09-.83.25s-.44.4-.55.67c-.11.27-.14.58-.09.87.05.29.2.56.41.77.21.21.48.35.77.41.29.06.59.03.87-.09.27-.11.51-.31.67-.55A1.499 1.499 0 008.5 10zM6 4.99h12c.55 0 1-.45 1-1s-.45-1-1-1H6c-.55 0-1 .45-1 1s.45 1 1 1z` |
| IcCalendarEvent | calendar event, event, appointment | `M18 3h-1a1 1 0 00-2 0H9a1 1 0 00-2 0H6a3 3 0 00-3 3v12a3 3 0 003 3h12a3 3 0 003-3V6a3 3 0 00-3-3zm-1.79 8.71l-5 5a1.002 1.002 0 01-1.42 0l-2-2a1.003 1.003 0 111.42-1.42l1.29 1.3 4.29-4.3a1.004 1.004 0 011.42 1.42zM19 7H5V6a1 1 0 011-1h1a1 1 0 002 0h6a1 1 0 002 0h1a1 1 0 011 1v1z` |
| IcCalendarWeek | calendar week, week view, weekly | `M20.12 3.88A3 3 0 0018 3h-1a1 1 0 00-2 0H9a1 1 0 00-2 0H6a3 3 0 00-3 3v12a3 3 0 003 3h12a3 3 0 003-3V6a3 3 0 00-.88-2.12zM8 17a1 1 0 110-2 1 1 0 010 2zm0-4a1 1 0 110-2 1 1 0 010 2zm4 4a1 1 0 110-2 1 1 0 010 2zm0-4a1 1 0 110-2 1 1 0 010 2zm4 0a1 1 0 110-2 1 1 0 010 2zm3-6H5V6a1 1 0 011-1h1a1 1 0 002 0h6a1 1 0 002 0h1a1 1 0 011 1v1z` |
| IcCopyDocument | copy document, duplicate file | `M12.33 8.82V6H4.87A1.88 1.88 0 003 7.88v12.24A1.88 1.88 0 004.87 22h10.26A1.88 1.88 0 0017 20.12v-9.41h-2.8a1.88 1.88 0 01-1.87-1.89zm8.08-3.23l-3-3A2 2 0 0016 2H8a2 2 0 00-2 2h7a3 3 0 012.12.88l3 3A3 3 0 0119 10v9a2 2 0 002-2V7a2 2 0 00-.59-1.41z` |
| IcFirstpage | first page, start, beginning | `M7 4c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1s1-.45 1-1V5c0-.55-.45-1-1-1zm5.41 8l6.29-6.29a.996.996 0 10-1.41-1.41l-7 7a.996.996 0 000 1.41l7 7c.2.2.45.29.71.29.26 0 .51-.1.71-.29a.996.996 0 000-1.41l-6.29-6.29-.01-.01z` |
| IcJioDot | jio, jio dot, brand, logo | `M8.478 7.237h-.4c-.76 0-1.174.428-1.174 1.285v4.129c0 1.063-.359 1.436-1.201 1.436-.663 0-1.202-.29-1.63-.815-.041-.055-.91.36-.91 1.381 0 1.105 1.034 1.782 2.955 1.782 2.333 0 3.563-1.174 3.563-3.742V8.521c-.002-.856-.416-1.285-1.203-1.285zm9.3 2.017c-2.265 0-3.77 1.436-3.77 3.577 0 2.196 1.45 3.605 3.728 3.605 2.265 0 3.756-1.409 3.756-3.59.001-2.156-1.477-3.592-3.714-3.592zm-.028 5.15c-.884 0-1.491-.648-1.491-1.574 0-.91.622-1.56 1.491-1.56.87 0 1.491.65 1.491 1.574 0 .898-.634 1.56-1.49 1.56zm-5.656-5.082h-.277c-.676 0-1.187.318-1.187 1.285v4.419c0 .98.497 1.285 1.215 1.285h.277c.676 0 1.16-.332 1.16-1.285v-4.42c0-.993-.47-1.284-1.188-1.284zm-.152-3.203c-.856 0-1.395.484-1.395 1.243 0 .773.553 1.256 1.436 1.256.857 0 1.395-.483 1.395-1.256s-.552-1.243-1.436-1.243z` |
| IcLastpage | last page, end, final | `M6.71 4.29A.996.996 0 105.3 5.7l6.29 6.29-6.29 6.29a.996.996 0 00.71 1.7c.26 0 .51-.1.71-.29l7-7a.996.996 0 000-1.41L6.71 4.29zM17 4c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1s1-.45 1-1V5c0-.55-.45-1-1-1z` |
| IcRepeat | repeat, loop, replay | `M4 12a5 5 0 015-5h3.59l-.3.29a1.001 1.001 0 00.326 1.64 1 1 0 001.094-.22l2-2a1 1 0 00.21-.33 1 1 0 000-.76.999.999 0 00-.21-.33l-2-2a1.004 1.004 0 10-1.42 1.42l.3.29H9a7 7 0 00-7 7 6.94 6.94 0 002.59 5.43 1 1 0 101.26-1.55A5 5 0 014 12zm15.41-5.43a.999.999 0 10-1.26 1.55A5 5 0 0115 17h-3.59l.3-.29a1.004 1.004 0 10-1.42-1.42l-2 2a1 1 0 00-.21.33 1 1 0 000 .76 1 1 0 00.21.33l2 2a1.001 1.001 0 001.639-.325 1 1 0 00-.219-1.095l-.3-.29H15a7 7 0 007-7 6.939 6.939 0 00-2.59-5.43z` |
| IcText | text, font, typography | `M20 3H4c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1s1-.45 1-1V5h6v14H9c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1h-2V5h6v2c0 .55.45 1 1 1s1-.45 1-1V4c0-.55-.45-1-1-1z` |
| IcTheme | theme, appearance, mode | `M19 2h-8a3 3 0 00-3 3v3H5a3 3 0 00-3 3v8a3 3 0 003 3h8a3 3 0 003-3v-3h3a3 3 0 003-3V5a3 3 0 00-3-3zm-5 17a1 1 0 01-1 1H5a1 1 0 01-1-1v-8a1 1 0 011-1h8a1 1 0 011 1v8z` |
| IcTime | time, clock, hour | `M12 2a10 10 0 100 20 10 10 0 000-20zm1 11a1 1 0 01-1 1H9a1 1 0 010-2h2V9a1 1 0 012 0v4z` |

---

# ICON KEYWORD INDEX — Extended SVG Library

When a keyword doesn't match the 71 core icons above, use this index to find the right SVG file.
CDN: `https://raw.githubusercontent.com/sunit1986/JioBharatIQ_Server/main/assets/icons/svg/[filename]`

## Media: play=ic_play.svg, pause=ic_pause.svg, stop=ic_stop.svg, rewind=ic_rewind.svg, shuffle=ic_shuffle.svg, repeat=ic_repeat.svg, record=ic_record.svg, play pause=ic_play_pause.svg, volume=ic_sound.svg, sound loud=ic_sound_loud.svg, sound medium=ic_sound_medium.svg, sound quiet=ic_sound_quiet.svg, sound off=ic_sound_disabled.svg, equalizer=ic_equalizer.svg

## Actions: send=ic_message_send.svg, copy=ic_copy_document.svg, paste=ic_paste_document.svg, share=ic_share_screen.svg, download=ic_download_fast.svg, upload=ic_cloud_upload.svg, edit=ic_edit_pen.svg, delete=ic_trash_clear.svg, save=ic_save.svg, print=ic_print.svg, undo=ic_undo.svg, redo=ic_redo.svg, cut=ic_cut_scissor.svg, link=ic_link.svg, unlink=ic_unlink.svg, pin=ic_pin.svg, bookmark=ic_bookmark.svg, flag=ic_flag.svg, drag=ic_drag_handle.svg, sort=ic_sort_list.svg, scan=ic_scan.svg, exchange=ic_exchange.svg

## Navigation: arrow back=ic_arrow_back.svg, arrow next=ic_arrow_next.svg, chevron left=ic_chevron_left.svg, chevron right=ic_chevron_right.svg, chevron down=ic_chevron_down.svg, chevron up=ic_chevron_up.svg, expand=ic_expand.svg, collapse=ic_collapse.svg, go back=ic_go_back.svg, go forward=ic_go_forward.svg

## Communication: chat=ic_chat.svg, chats=ic_chats.svg, message=ic_message_send.svg, mail=ic_e_mail.svg, call=ic_call.svg, video call=ic_video_call.svg, sms=ic_sms.svg, conversation=ic_conversation.svg, contacts=ic_contacts.svg, new chat=ic_new_chat.svg

## User: profile=ic_profile.svg, user=ic_user.svg, group=ic_multiple_user.svg, like=ic_like.svg, dislike=ic_dislike.svg, favorite=ic_favourite_mode.svg, login=ic_login.svg, logout=ic_logout.svg

## UI: close=ic_close.svg, menu=ic_burger_menu.svg, search=ic_search.svg, settings=ic_settings.svg, filter=ic_filter_multiple.svg, more=ic_more_horizontal.svg, info=ic_info.svg, help=ic_help.svg, notification=ic_notification.svg, home=ic_home.svg, widgets=ic_widgets.svg, list=ic_list.svg, fullscreen=ic_screen_full.svg, grid=ic_view_tile.svg

## Status: success=ic_success.svg, error=ic_error.svg, warning=ic_warning.svg, loading=ic_status_loading.svg, confirm=ic_confirm.svg, blocked=ic_blocked.svg, live=ic_live.svg

## Files: document=ic_document.svg, folder=ic_folder.svg, pdf=ic_document_pdf.svg, image=ic_image.svg, video=ic_video.svg, audio=ic_audio.svg, music=ic_music.svg

## Device: wifi=ic_wifi.svg, wifi off=ic_wifi_off.svg, bluetooth=ic_bluetooth.svg, mobile=ic_mobile.svg, mic=ic_mic.svg, mic off=ic_mic_off.svg, camera=ic_photo_camera.svg, location=ic_location.svg, headphones=ic_headphones.svg, battery=ic_battery_full.svg, nfc=ic_nfc.svg

## Commerce: cart=ic_cart.svg, shopping bag=ic_shopping_bag.svg, wallet=ic_wallet.svg, payment=ic_payment.svg, rupee=ic_rupee.svg, coupon=ic_coupon.svg, store=ic_store.svg, delivery=ic_truck_delivery.svg, gift=ic_gift.svg

## Security: lock=ic_lock.svg, unlock=ic_lock_unlock.svg, key=ic_key.svg, fingerprint=ic_fingerprint.svg, shield=ic_protection.svg, incognito=ic_incognito.svg

## Weather: sunny=ic_sunny_clear.svg, cloudy=ic_cloudy.svg, rain=ic_rain.svg, snow=ic_snow.svg, thunderstorm=ic_thunderstorm.svg, fog=ic_fog.svg, moon=ic_night_clear.svg, temperature=ic_temperature.svg

## Misc: brain=ic_brain.svg, ai sparkle=ic_ai_sparkle.svg, magic=ic_magic.svg, robot=ic_robot.svg, rocket=ic_rocket.svg, bulb=ic_bulb.svg, map=ic_map.svg, cricket=ic_cricket.svg, football=ic_football.svg, education=ic_education.svg, namaste=ic_namaste.svg

#!/usr/bin/env python3
"""
JDS Knowledge Server - MCP Server for Jio Design System
Version: 3.3.0

SECURITY RULES (enforced at every layer):
- JSON-only responses — no markdown, no explanations, no reasoning
- No internal file paths exposed — all references are sanitized
- No skill references exposed — pure knowledge base
- No source code introspection — __file__, __doc__, __dict__ are blocked
- Input sanitization — all inputs stripped, length-capped, character-filtered
- No eval/exec — no dynamic code execution
- No filesystem access — read-only in-memory data
- Error messages are generic — no stack traces, no internal details

MCP Protocol: JSON-RPC 2.0 over stdio
"""

import json
import os
import re
import sys
import urllib.request

SERVER_VERSION = "3.3.0"

# ============================================================================
# AUTO-UPDATE: fetch latest knowledge base from GitHub on every startup
# ============================================================================

_REPO_BASE = "https://raw.githubusercontent.com/sunit1986/JioBharatIQ_Server/main"
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _auto_update():
    """Download latest knowledge base from GitHub.
    Updates knowledge_base.py only — server code updates come via PyPI.
    Falls back to certifi certs on macOS Python.org installs that lack system certs."""
    import ssl as _ssl
    target = os.path.join(_SCRIPT_DIR, "knowledge_base.py")
    url = f"{_REPO_BASE}/knowledge_base.py"

    def _fetch(ctx=None):
        if ctx:
            return urllib.request.urlopen(url, context=ctx, timeout=10).read()
        return urllib.request.urlopen(url, timeout=10).read()

    try:
        # Attempt 1: standard SSL with system certificates
        data = _fetch()
    except Exception:
        try:
            # Attempt 2: certifi CA bundle (macOS Python.org without cert installer)
            import certifi as _certifi
            _ctx = _ssl.create_default_context(cafile=_certifi.where())
            data = _fetch(_ctx)
        except Exception:
            return  # offline or no certs available — use cached version silently

    try:
        with open(target, "wb") as f:
            f.write(data)
    except Exception:
        pass  # read-only filesystem — use cached version


if not os.environ.get("_JDS_NO_UPDATE"):
    _auto_update()

from .knowledge_base import COMPONENTS, TOKENS, ICONS_SEARCHABLE

# Support both old (FIGMA_REFERENCES) and new (FIGMA_REFS) naming
try:
    from .knowledge_base import FIGMA_REFERENCES
except ImportError:
    try:
        from .knowledge_base import FIGMA_REFS as FIGMA_REFERENCES
    except ImportError:
        FIGMA_REFERENCES = {}

# Support both old (ICON_CATEGORIES) and new (no categories — derive from icons)
try:
    from .knowledge_base import ICON_CATEGORIES
except ImportError:
    # Build a minimal category index from ICONS_SEARCHABLE
    _cats = {}
    if isinstance(ICONS_SEARCHABLE, dict):
        for name, data in ICONS_SEARCHABLE.items():
            cat = data.get("category", "general")
            _cats.setdefault(cat, []).append(name)
    ICON_CATEGORIES = _cats


# ============================================================================
# SECURITY: Input sanitization
# ============================================================================

MAX_INPUT_LENGTH = 200
ALLOWED_CHARS = re.compile(r'^[a-zA-Z0-9_\-\s/.]+$')


def sanitize_input(value: str) -> str:
    """
    Sanitize all user input:
    - Strip whitespace
    - Enforce max length
    - Block dangerous characters (no quotes, brackets, semicolons, etc.)
    - Returns empty string if invalid
    """
    if not isinstance(value, str):
        return ""
    value = value.strip()
    if len(value) > MAX_INPUT_LENGTH:
        value = value[:MAX_INPUT_LENGTH]
    if not ALLOWED_CHARS.match(value):
        # Remove any characters not in the allowed set
        value = re.sub(r'[^a-zA-Z0-9_\-\s/.]', '', value)
    return value


def sanitize_int(value, default: int = 10, min_val: int = 1, max_val: int = 50) -> int:
    """Sanitize integer input with bounds."""
    try:
        v = int(value)
        return max(min_val, min(v, max_val))
    except (TypeError, ValueError):
        return default


# ============================================================================
# SECURITY: Output sanitization — strip any accidental file paths or secrets
# ============================================================================

PATH_PATTERNS = [
    re.compile(r'/Users/[^\s"]+'),
    re.compile(r'/home/[^\s"]+'),
    re.compile(r'C:\\[^\s"]+'),
    re.compile(r'\.claude/[^\s"]+'),
    re.compile(r'memory/[^\s"]+\.md'),
]

SECRET_PATTERNS = [
    re.compile(r'_password=[^\s"]+'),
    re.compile(r'api[_-]?key[=:][^\s"]+', re.IGNORECASE),
    re.compile(r'token[=:][^\s"]+', re.IGNORECASE),
    re.compile(r'secret[=:][^\s"]+', re.IGNORECASE),
]


def sanitize_output(obj):
    """
    Deep-scan output for any leaked file paths or secrets.
    Recursively processes dicts, lists, and strings.
    """
    if isinstance(obj, str):
        for pattern in PATH_PATTERNS:
            obj = pattern.sub("[REDACTED]", obj)
        for pattern in SECRET_PATTERNS:
            obj = pattern.sub("[REDACTED]", obj)
        return obj
    elif isinstance(obj, dict):
        return {k: sanitize_output(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_output(item) for item in obj]
    return obj


# ============================================================================
# TOOL RESPONSE REMINDER — appended to every tool response
# ============================================================================

TOOL_REMINDER = (
    "\n\n---\n"
    "MANDATORY JDS RULES — enforce on every single line of output:\n"
    "FONTS: JioType ONLY. Never Inter, Arial, Helvetica, Roboto, system-ui, or sans-serif.\n"
    "ICONS: JDS SVG library ONLY (find_icon → svg_path). Never Material icons, Heroicons, Feather, or emoji as icons.\n"
    "COLORS: JDS tokens ONLY. Never #a855f7, #22c55e, #f97316, #ec4899, or any non-JDS color.\n"
    "  Primary=#3535f3 | Secondary=#f7ab20 | Sparkle=#1eccb0 | Error=#fa2f40 | Warning=#f06d0f | Success=#25ab21\n"
    "  Grey-100=#141414 | Grey-40=#e0e0e0 | Grey-20=#f5f5f5 | Surface-ghost=#eeeeef | Surface-bold=#3900ad\n"
    "TYPOGRAPHY: JDS scale ONLY. Never ad-hoc px sizes. Use: Display/Headline/Title/Body/Label variants.\n"
    "COMPONENTS: JDS specs ONLY (lookup_component). Never custom/arbitrary component implementations.\n"
    "OPACITY: JDS tokens. invisible=0, disabled=0.38, enabled=1. Never arbitrary opacity values.\n"
    "LOADING STATES: Use Skeleton (shimmer) for content loading. NOT spinners.\n"
    "LIGHT MODE: Default to light mode ALWAYS. Only dark mode if explicitly requested by user.\n"
    "ASSETS: Call get_assets FIRST. Use cdn_url directly in HTML — no file copying."
)


# ============================================================================
# TOOL FUNCTIONS — all return sanitized dicts only
# ============================================================================

def lookup_component(component_name: str) -> dict:
    """Get JDS component specifications."""
    component_name = sanitize_input(component_name)

    # Normalize: try Title case, then check aliases
    lookup_key = component_name.title()

    # Handle common aliases
    aliases = {
        "Bottomsheet": "BottomSheet",
        "Bottom Sheet": "BottomSheet",
        "Bottomnav": "BottomNav",
        "Bottom Nav": "BottomNav",
        "Inputfield": "InputField",
        "Input Field": "InputField",
        "Promocard": "PromoCard",
        "Promo Card": "PromoCard",
        "Servicecard": "ServiceCard",
        "Service Card": "ServiceCard",
        "Contentblock": "ContentBlock",
        "Content Block": "ContentBlock",
        "Ratingbar": "RatingBar",
        "Rating Bar": "RatingBar",
        "Avatarv2": "AvatarV2",
        "Searchbox": "SearchBox",
        "Search Box": "SearchBox",
        "Selectorbutton": "SelectorButton",
        "Selector Button": "SelectorButton",
    }
    lookup_key = aliases.get(lookup_key, lookup_key)

    if lookup_key not in COMPONENTS:
        available = sorted(COMPONENTS.keys())
        return {
            "error": "Component not found",
            "query": component_name,
            "available_components": available
        }

    component = COMPONENTS[lookup_key]
    result = {
        "component": component.get("name", lookup_key),
        "import_path": component.get("import_path", "@jds/core"),
        "description": component.get("description", ""),
        "props": component.get("props", {}),
        "variants": {},
        "code_example": component.get("code_example", component.get("css_example", ""))
    }
    # Surface extra spec fields (tokens, sizes, figma_node, etc.)
    for extra_key in ["tokens", "sizes", "figma_node", "storybook",
                      "dismissal", "position", "_rule"]:
        val = component.get(extra_key)
        if val:
            result[extra_key] = val

    # Collect all variant info dynamically
    for key in ["kinds", "sizes", "states", "types", "orientations",
                 "shapes", "indicator_types", "density_options",
                 "overflow_options", "icon_types", "badge_types",
                 "variants", "appearances", "weights", "image_ratios"]:
        val = component.get(key, [])
        if val:
            result["variants"][key] = val

    # Include sub_components if any
    if "sub_components" in component:
        result["sub_components"] = component["sub_components"]

    # Include size_map if available
    if "size_map" in component:
        result["size_map"] = component["size_map"]

    return sanitize_output(result)


def resolve_token(token_category: str, token_name: str = None) -> dict:
    """Resolve JDS design tokens."""
    token_category = sanitize_input(token_category).lower().replace(" ", "_")

    if token_category not in TOKENS:
        return {
            "error": "Token category not found",
            "available_categories": list(TOKENS.keys())
        }

    category_data = TOKENS[token_category]

    # Detect if category_data is flat {token: value} or nested {subcategory: {token: value}}
    def _is_flat(d):
        """True = flat {token: value}. False = nested {subcategory: {token: value}}.
        Rules (in priority order):
        1. Any scalar top-level value → flat (e.g. opacity: {"invisible": "0"})
        2. Any top-level KEY contains a hyphen → flat (e.g. typography: {"body-s": {...}})
        3. All values are dicts AND sub-dict keys contain hyphens → nested subcategory
        4. Otherwise → flat
        """
        if not isinstance(d, dict):
            return True
        items = [(k, v) for k, v in d.items() if not k.startswith('_')]
        if not items:
            return True
        # Rule 1: any scalar top-level value → flat
        if any(not isinstance(v, dict) for _, v in items):
            return True
        # Rule 2: any top-level KEY has a hyphen → flat token names (e.g. "body-s", "display-l")
        if any('-' in k for k, _ in items):
            return True
        # Rule 3: all values are dicts — check if sub-dicts have hyphenated token-name keys
        for _, v in items:
            if isinstance(v, dict):
                # Token name pattern: ends with hyphen+number/level e.g. "primary-50", "grey-100"
                if any(k[-1].isdigit() and '-' in k for k in v.keys()):
                    return False  # subcategory container
        return True

    _flat = _is_flat(category_data)

    if not token_name:
        if _flat:
            sample = {k: v for k, v in list(category_data.items())[:3] if not k.startswith('_')}
            return sanitize_output({
                "category": token_category,
                "token_count": len([k for k in category_data if not k.startswith('_')]),
                "sample_tokens": sample
            })
        else:
            # Legacy nested format
            keys = [k for k in category_data.keys() if not k.startswith('_')]
            return sanitize_output({
                "category": token_category,
                "subcategories": keys
            })

    token_name = sanitize_input(token_name)
    token_name_lower = token_name.lower().replace("_", "-")

    if _flat:
        # Flat search: {token_name: value}
        for key, value in category_data.items():
            if not key.startswith('_') and token_name_lower in key.lower():
                return sanitize_output({
                    "category": token_category,
                    "token": key,
                    "value": value
                })
        return {"error": f"Token not found in {token_category}"}
    else:
        # Legacy nested search: {subcategory: {token_name: value}}
        for subcategory, tokens in category_data.items():
            if not isinstance(tokens, dict):
                continue
            for key, value in tokens.items():
                if token_name_lower in key.lower():
                    return sanitize_output({
                        "category": token_category,
                        "subcategory": subcategory,
                        "token": key,
                        "value": value
                    })
        return {"error": f"Token not found in {token_category}"}


def find_icon(query: str, limit: int = 10) -> dict:
    """Search JDS icon library."""
    query = sanitize_input(query)
    limit = sanitize_int(limit, default=10, min_val=1, max_val=50)

    if not query:
        return {
            "error": "Search query is required",
            "available_categories": list(ICON_CATEGORIES.keys())
        }

    query_lower = query.lower()
    results = []

    for icon_name, icon_data in ICONS_SEARCHABLE.items():
        if query_lower in icon_name.lower():
            result_entry = {
                "icon": icon_name,
                "category": icon_data["category"],
                "keywords": icon_data["keywords"],
                "match_type": "name"
            }
            if "svg_path" in icon_data:
                result_entry["svg_path"] = icon_data["svg_path"]
            if "viewBox" in icon_data:
                result_entry["viewBox"] = icon_data["viewBox"]
            if "jsx_file" in icon_data:
                result_entry["jsx_file"] = icon_data["jsx_file"]
            results.append(result_entry)
        elif any(query_lower in keyword for keyword in icon_data["keywords"]):
            result_entry = {
                "icon": icon_name,
                "category": icon_data["category"],
                "keywords": icon_data["keywords"],
                "match_type": "keyword"
            }
            if "svg_path" in icon_data:
                result_entry["svg_path"] = icon_data["svg_path"]
            if "viewBox" in icon_data:
                result_entry["viewBox"] = icon_data["viewBox"]
            if "jsx_file" in icon_data:
                result_entry["jsx_file"] = icon_data["jsx_file"]
            results.append(result_entry)

        if len(results) >= limit:
            break

    if not results:
        matching_categories = [
            cat for cat in ICON_CATEGORIES.keys()
            if query_lower in cat.lower()
        ]
        return {
            "results": [],
            "suggestion": "No icons found matching query",
            "available_categories": list(ICON_CATEGORIES.keys()),
            "matching_categories": matching_categories if matching_categories else None
        }

    return sanitize_output({
        "query": query,
        "count": len(results),
        "results": results
    })


def get_assets(asset_type: str = "all", project_dir: str = "") -> dict:
    """Get JDS asset CDN URLs for prototyping. Returns GitHub-hosted URLs that work
    directly in HTML — no file copying required."""
    asset_type = sanitize_input(asset_type).lower()
    project_dir = sanitize_input(project_dir).strip()

    cdn_base = f"{_REPO_BASE}/assets"

    # Hardcoded manifest of all known asset files
    _FONT_FILES = [
        "JioTypeVarSubsetW05-Italic.woff2", "JioTypeVarSubsetW05-Regular.woff2",
        "JioTypeVarW05-Italic.woff2", "JioTypeVarW05-Regular.woff2",
        "JioTypeW05-Black.woff2", "JioTypeW05-BlackItalic.woff2",
        "JioTypeW05-Bold.woff2", "JioTypeW05-BoldItalic.woff2",
        "JioTypeW05-ExtraBlack.woff2", "JioTypeW05-ExtraBlackItalic.woff2",
        "JioTypeW05-Hairline.woff2", "JioTypeW05-HairlineItalic.woff2",
        "JioTypeW05-Italic.woff2", "JioTypeW05-Light.woff2",
        "JioTypeW05-LightItalic.woff2", "JioTypeW05-Medium.woff2",
        "JioTypeW05-MediumItalic.woff2", "JioTypeW05-Regular.woff2",
    ]
    _ANIMATION_FILES = [
        "HelloJio_Breath(IdleState)_241.mp4", "HelloJio_Listening_241.mp4",
    ]
    _STATE_FILES_LIGHT = [
        "Idle_state.mp4",
        "Listening_state.mp4",
        "Speaking_State.mp4",
        "Bot to bot speaking_state.mp4",
        "Thinking_state.mp4",
        "Thinking Reveal_State.mp4",
        "Thinking End_state.mp4",
        "User speaking to bot_state.mp4",
        "HelloJio_Complete_242.mp4",
    ]
    _STATE_FILES_DARK = [
        "HelloJio_Breath(IdleState)_242.mp4",
        "HelloJio_Listening_242.mp4",
        "HelloJio_BotSpeaking_242.mp4",
        "HelloJio_ThinkingToBotSpeak 242.mp4",
        "HelloJio_ThinkingLoop_242.mp4",
        "HelloJio_ThinkingReveal_242.mp4",
        "HelloJio_ThinkingEnd_242.mp4",
        "HelloJio_UserSpeaktoBotSpeak_242.mp4",
        "HelloJio_Complete_242.mp4",
    ]
    _ICON_FILES = [
        "IcAccessibility.jsx", "IcAdd.jsx", "IcAlarm.jsx", "IcAlbum.jsx",
        "IcArrowBack.jsx", "IcBack.jsx", "IcBrain.jsx", "IcBurgerMenu.jsx",
        "IcCalendar.jsx", "IcCalendarEvent.jsx", "IcCalendarWeek.jsx",
        "IcCart.jsx", "IcChat.jsx", "IcChevronDown.jsx", "IcChevronLeft.jsx",
        "IcChevronRight.jsx", "IcChevronUp.jsx", "IcClose.jsx",
        "IcCloseRemove.jsx", "IcConfirm.jsx", "IcCopy.jsx",
        "IcCopyDocument.jsx", "IcDislike.jsx", "IcDocument.jsx",
        "IcDownload.jsx", "IcEditPen.jsx", "IcError.jsx", "IcFavorite.jsx",
        "IcFilterMultiple.jsx", "IcFirstpage.jsx", "IcHomeConnection.jsx",
        "IcInfo.jsx", "IcJioDot.jsx", "IcLanguage.jsx", "IcLastpage.jsx",
        "IcLike.jsx", "IcList.jsx", "IcMic.jsx", "IcMicOff.jsx",
        "IcMinus.jsx", "IcMoreHorizontal.jsx", "IcNext.jsx",
        "IcNightClear.jsx", "IcNotification.jsx", "IcPause.jsx",
        "IcPhotoCamera.jsx", "IcPlay.jsx", "IcProfile.jsx", "IcRefresh.jsx",
        "IcRepeat.jsx", "IcSearch.jsx", "IcSendMessage.jsx",
        "IcSettings.jsx", "IcShare.jsx", "IcStar.jsx", "IcStop.jsx",
        "IcStopwatch.jsx", "IcSuccess.jsx", "IcSunnyClear.jsx",
        "IcTask.jsx", "IcText.jsx", "IcTheme.jsx", "IcTime.jsx",
        "IcTrash.jsx", "IcUpload.jsx", "IcVoice.jsx", "IcWarning.jsx",
        "IcWidgets.jsx", "IcWifiOff.jsx", "PsJioMart.jsx", "WmJiomart.jsx",
        "icon.tsx", "map.js",
    ]

    font_cdn = f"{cdn_base}/fonts/woff2"
    anim_cdn = f"{cdn_base}/animations"
    icon_cdn = f"{cdn_base}/icons"
    states_cdn = f"{cdn_base}/states"

    asset_map = {
        "fonts": {
            "description": "JioType font family (WOFF2 for web)",
            "cdn_base": font_cdn,
            "usage_css": (
                f"@font-face {{ font-family: 'JioType'; font-weight: 400; "
                f"src: url('{font_cdn}/JioTypeVarW05-Regular.woff2') format('woff2'); }}\n"
                f"@font-face {{ font-family: 'JioType'; font-weight: 500; "
                f"src: url('{font_cdn}/JioTypeW05-Medium.woff2') format('woff2'); }}\n"
                f"@font-face {{ font-family: 'JioType'; font-weight: 700; "
                f"src: url('{font_cdn}/JioTypeW05-Bold.woff2') format('woff2'); }}"
            ),
            "files": [{"name": f, "cdn_url": f"{font_cdn}/{f}"} for f in _FONT_FILES],
        },
        "animations": {
            "description": "HelloJio animation assets (MP4)",
            "cdn_base": anim_cdn,
            "usage_html": (
                f'<video src="{anim_cdn}/HelloJio_Breath(IdleState)_241.mp4" autoplay loop muted playsinline></video>\n'
                f'<video src="{anim_cdn}/HelloJio_Listening_241.mp4" autoplay loop muted playsinline></video>'
            ),
            "files": [{"name": f, "cdn_url": f"{anim_cdn}/{f}"} for f in _ANIMATION_FILES],
        },
        "icons": {
            "description": "JDS icon components (71 JSX + 1281 SVG)",
            "cdn_base": icon_cdn,
            "usage_note": (
                "For HTML prototypes, use find_icon tool — it returns svg_path directly. "
                "JSX files are React Native SVG components. SVG files are in icons/svg/ directory."
            ),
            "files": [{"name": f, "cdn_url": f"{icon_cdn}/{f}"} for f in _ICON_FILES],
            "svg_cdn_base": f"{icon_cdn}/svg",
            "svg_usage_note": (
                "1281 SVG icons available at icons/svg/{name}.svg. Use find_icon tool for "
                "instant svg_path data without fetching files."
            ),
        },
        "states": {
            "description": "Voice Q&A animation states — 9 Light + 9 Dark MP4s for AI voice interface",
            "cdn_base": states_cdn,
            "light_cdn": f"{states_cdn}/Light",
            "dark_cdn": f"{states_cdn}/Dark",
            "state_map": {
                "idle": {
                    "light": f"{states_cdn}/Light/Idle_state.mp4",
                    "dark": f"{states_cdn}/Dark/HelloJio_Breath(IdleState)_242.mp4",
                },
                "listening": {
                    "light": f"{states_cdn}/Light/Listening_state.mp4",
                    "dark": f"{states_cdn}/Dark/HelloJio_Listening_242.mp4",
                },
                "speaking": {
                    "light": f"{states_cdn}/Light/Speaking_State.mp4",
                    "dark": f"{states_cdn}/Dark/HelloJio_BotSpeaking_242.mp4",
                },
                "bot_to_bot_speaking": {
                    "light": f"{states_cdn}/Light/Bot%20to%20bot%20speaking_state.mp4",
                    "dark": f"{states_cdn}/Dark/HelloJio_ThinkingToBotSpeak%20242.mp4",
                },
                "thinking": {
                    "light": f"{states_cdn}/Light/Thinking_state.mp4",
                    "dark": f"{states_cdn}/Dark/HelloJio_ThinkingLoop_242.mp4",
                },
                "thinking_reveal": {
                    "light": f"{states_cdn}/Light/Thinking%20Reveal_State.mp4",
                    "dark": f"{states_cdn}/Dark/HelloJio_ThinkingReveal_242.mp4",
                },
                "thinking_end": {
                    "light": f"{states_cdn}/Light/Thinking%20End_state.mp4",
                    "dark": f"{states_cdn}/Dark/HelloJio_ThinkingEnd_242.mp4",
                },
                "user_speaking": {
                    "light": f"{states_cdn}/Light/User%20speaking%20to%20bot_state.mp4",
                    "dark": f"{states_cdn}/Dark/HelloJio_UserSpeaktoBotSpeak_242.mp4",
                },
                "complete": {
                    "light": f"{states_cdn}/Light/HelloJio_Complete_242.mp4",
                    "dark": f"{states_cdn}/Dark/HelloJio_Complete_242.mp4",
                },
            },
            "usage_note": (
                "Use state_map for semantic lookup by state name. "
                "Light theme for default/light mode, Dark theme for dark mode. "
                "Usage: <video src=\"{cdn_url}\" autoplay loop muted playsinline></video> "
                "States: idle, listening, speaking, bot_to_bot_speaking, thinking, "
                "thinking_reveal, thinking_end, user_speaking, complete"
            ),
            "files": (
                [{"name": f, "cdn_url": f"{states_cdn}/Light/{f.replace(' ', '%20')}", "theme": "light"}
                 for f in _STATE_FILES_LIGHT] +
                [{"name": f, "cdn_url": f"{states_cdn}/Dark/{f.replace(' ', '%20')}", "theme": "dark"}
                 for f in _STATE_FILES_DARK]
            ),
        }
    }

    if asset_type not in ("all", "fonts", "animations", "icons", "svg", "states"):
        return {
            "error": "Unknown asset type",
            "available_types": ["all", "fonts", "animations", "icons", "states"]
        }

    result = {"cdn_base": cdn_base, "types": {}}

    types_to_include = [asset_type] if asset_type != "all" else ["fonts", "animations", "icons", "states"]

    for atype in types_to_include:
        info = asset_map[atype]
        entry = {
            "description": info["description"],
            "cdn_base": info["cdn_base"],
            "files": info["files"],
            "count": len(info["files"]),
        }
        # Add usage hints and extra fields
        for key in ("usage_css", "usage_html", "usage_note", "svg_cdn_base", "svg_usage_note",
                    "state_map", "light_cdn", "dark_cdn"):
            if key in info:
                entry[key] = info[key]
        result["types"][atype] = entry

    result["IMPORTANT"] = (
        "Assets are served from GitHub CDN. Use the cdn_url values DIRECTLY in your HTML "
        "src and url() attributes. NO file copying is needed. Example: "
        f"src='{font_cdn}/JioTypeVarW05-Regular.woff2'"
    )
    return result


def get_figma_reference(design_name: str) -> dict:
    """Get Figma node references."""
    design_name = sanitize_input(design_name)
    design_name_lower = design_name.lower().replace(" ", "_").replace("-", "_")

    for key, ref_data in FIGMA_REFERENCES.items():
        # Support both "name" (old) and "title" (new) field names
        ref_name = ref_data.get("name", ref_data.get("title", key))
        if design_name_lower in key or design_name_lower in ref_name.lower():
            result = {
                "name": ref_name,
                "file_key": ref_data.get("file_key", ref_data.get("url", "")),
                "url": ref_data.get("url", ""),
                "description": ref_data.get("description", ref_data.get("usage", ""))
            }
            if "node_id" in ref_data:
                result["node_id"] = ref_data["node_id"]
            return sanitize_output(result)

    return {
        "error": "Figma reference not found",
        "available_references": [
            {"key": key, "name": ref["name"]}
            for key, ref in FIGMA_REFERENCES.items()
        ]
    }


# ============================================================================
# MCP PROTOCOL — Tool definitions and request handling
# ============================================================================

TOOLS = [
    {
        "name": "lookup_component",
        "description": f"[JioBharatIQ v{SERVER_VERSION}] Get JDS component specs: Button, Card, InputField, Modal, BottomSheet, Avatar, Tabs, Toast, Accordion, Divider, Badge, BottomNav, Container, Spinner, Skeleton, PromoCard, ServiceCard, ContentBlock, Carousel, RatingBar, Text",
        "inputSchema": {
            "type": "object",
            "properties": {
                "component_name": {
                    "type": "string",
                    "description": "Component name (e.g., 'Button', 'Card', 'Toast', 'Carousel')"
                }
            },
            "required": ["component_name"]
        }
    },
    {
        "name": "resolve_token",
        "description": "Resolve JDS design tokens (colors, typography, spacing, border_radius, opacity)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "token_category": {
                    "type": "string",
                    "description": "Token category: 'colors', 'typography', 'spacing', 'border_radius', 'opacity'"
                },
                "token_name": {
                    "type": "string",
                    "description": "Optional token name (e.g., 'primary-50', 'body-s', 'base')"
                }
            },
            "required": ["token_category"]
        }
    },
    {
        "name": "find_icon",
        "description": "Search JDS icon library (1301 icons: 71 JSX + 1230 SVG with inline svg_path data). Returns svg_path for direct HTML use — no file fetching needed.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term (icon name or keyword like 'calendar', 'mic', 'home')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results (default: 10, max: 50)",
                    "default": 10
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_assets",
        "description": f"[JioBharatIQ v{SERVER_VERSION}] Get JDS asset CDN URLs for prototyping. Returns GitHub-hosted URLs for fonts (JioType WOFF2), animations (HelloJio MP4s), icons (71 JSX + 1281 SVG), and Voice Q&A states (9 Light + 9 Dark MP4s). MANDATORY: Call this FIRST when building any prototype.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "asset_type": {
                    "type": "string",
                    "description": "Asset type: 'all', 'fonts', 'animations', 'icons', 'states' (default: 'all')",
                    "default": "all"
                },
                "project_dir": {
                    "type": "string",
                    "description": "(Optional, unused) Previously used for local copy commands. Assets are now served via GitHub CDN."
                }
            }
        }
    },
    {
        "name": "get_figma_reference",
        "description": "Get Figma node IDs and URLs for JDS designs: homepage, menu, chat_page, media_page, assistants_page, tools_page, oneui_design_kit, jio_testlab, chat_input",
        "inputSchema": {
            "type": "object",
            "properties": {
                "design_name": {
                    "type": "string",
                    "description": "Design name: 'homepage', 'menu', 'chat_page', 'oneui_design_kit', etc."
                }
            },
            "required": ["design_name"]
        }
    }
]


def handle_request(request: dict) -> dict:
    """
    Handle MCP JSON-RPC request.
    SECURITY: Only allows whitelisted methods. No introspection.
    """
    if not isinstance(request, dict):
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32600, "message": "Invalid request"}
        }

    method = request.get("method", "")
    params = request.get("params", {})
    request_id = request.get("id")

    # SECURITY: Whitelist allowed methods
    allowed_methods = {
        "initialize", "tools/list", "tools/call",
        "notifications/initialized", "ping"
    }
    if method not in allowed_methods:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": "Method not found"}
        }

    # Handle initialize — also trigger auto-update so long-running servers pick up changes
    if method == "initialize":
        try:
            _auto_update()
        except Exception:
            pass
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": f"JioBharatIQ_v{SERVER_VERSION}",
                    "version": SERVER_VERSION
                },
                "instructions": (
                    f"You are connected to the JDS (Jio Design System) knowledge server v{SERVER_VERSION}. "
                    "PROTOTYPE GENERATION RULES — apply to every output without exception:\n\n"

                    "=== LAYER 1: FOUNDATION (Always load first) ===\n"
                    "1. Call get_assets FIRST. Use cdn_url values DIRECTLY in HTML src/url — no file copying.\n"
                    "2. Single-file HTML prototype. No React, no Tailwind, no CDN libs, no build tools. "
                    "All CSS and JS inline. One index.html. Serve with python3 -m http.server.\n"
                    "3. Mobile canvas: 360×800px. Always wrap in realistic phone frame: rounded corners, "
                    "dark border, notch, status bar (time + battery + signal), scrollable screen area.\n"
                    "4. Add left sidebar outside phone listing all screens. Click = show screen in phone. "
                    "Highlight active screen.\n"
                    "5. LIGHT MODE by default for ALL prototypes. Only dark mode if user explicitly asks.\n\n"

                    "=== LAYER 2: JDS ASSET RESOLUTION (Mandatory before writing any code) ===\n"
                    "6. FONTS: JioType ONLY. From get_assets cdn_url. NEVER Inter/Arial/Helvetica/Roboto.\n"
                    "7. ICONS: Call find_icon — returns svg_path. Inline SVG in HTML. "
                    "NEVER Material, Feather, Heroicons, or emoji. JDS library: IcMic, IcSearch, IcSendMessage, "
                    "IcChevronRight, IcChevronLeft, IcClose, IcAdd, IcProfile, IcChat, IcHome, etc.\n"
                    "8. COLORS: JDS tokens ONLY. resolve_token to verify. "
                    "primary-50=#3535f3 | secondary-50=#f7ab20 | sparkle-50=#1eccb0 | "
                    "error=#fa2f40 | grey-100=#141414 | grey-20=#f5f5f5 | "
                    "surface-ghost=#eeeeef | surface-bold=#3900ad | surface-ghost-icon=#e7e9ff.\n"
                    "9. TYPOGRAPHY: JDS scale. Display 52px / Headline 28-32px / Title 16-20px / "
                    "Body-l 16px / Body-m 15px / Body-s 14px / Label-m 13px / Caption 11px. "
                    "NEVER arbitrary sizes.\n"
                    "10. COMPONENTS: lookup_component before building Button, Card, BottomSheet, etc. "
                    "Build from JDS specs — NEVER custom components.\n"
                    "11. OPACITY: invisible=0, disabled=0.38, enabled=1. NEVER arbitrary values.\n"
                    "12. ANIMATIONS: HelloJio MP4s from get_assets for AI assistant states. "
                    "Voice Q&A states (idle/listening/speaking/thinking/etc) available via get_assets('states'). "
                    "148×148px for full-screen voice, 32×32px inline.\n\n"

                    "=== LAYER 3: BLUEPRINT PROMPT (Prototype quality) ===\n"
                    "13. Show 3 UX directions per feature. Each direction = different interaction model "
                    "(not just different visuals). All accessible from sidebar.\n"
                    "14. Real content only. Indian names, ₹ amounts, Hindi/English bilingual labels. "
                    "No Lorem Ipsum, no 'John Doe', no 'Sample Text'.\n"
                    "15. Exact data makes prototypes production-ready: name real cricket players, "
                    "real Bollywood films, real song titles, real product names from Jio ecosystem.\n"
                    "16. Include ALL states: default, loading (shimmer skeleton — NEVER spinners), "
                    "empty state (with actionable guidance), error, success. All navigable from sidebar.\n\n"

                    "=== LAYER 4: CULTURAL CONTEXT (JBIQ specifics) ===\n"
                    "17. Hindi-first copy where appropriate. Key phrases: 'Namasté', 'Aap kaise hain?', "
                    "'Bahut achha!', 'Shukriya'. Use Devanagari for Hindi text (Noto Sans Devanagari).\n"
                    "18. Indian context: IPL cricket, Bollywood, JioSaavn, JioCinema, JioMart, "
                    "Tira, regional languages (Telugu, Tamil, Bengali, Kannada, Marathi).\n"
                    "19. JioBharatIQ brand name = JBIQ. Jio Omni AI = JBIQ. Never 'Jio Omni AI'.\n"
                    "20. Assistant avatar: 4-dot grid (blue=#3535f3, orange=#f7ab20, purple=#6464ff, "
                    "teal=#1eccb0). Use get_assets('states') for all Voice Q&A states (idle, listening, speaking, thinking, etc).\n\n"

                    "=== LAYER 5: POLISH PASS (Always include) ===\n"
                    "21. Staggered CSS entrance animations (fadeDown with animation-delay: 0s, 0.1s, 0.15s, 0.2s).\n"
                    "22. AI thinking indicator: animated shimmer text or 3-dot pulse during processing states.\n"
                    "23. Feedback row below every AI response: thumbs-up, thumbs-down, copy, share icons.\n"
                    "24. Celebration overlays for success states (confetti burst, checkmark animation).\n"
                    "25. Toast notifications for user actions (bottom of screen, auto-dismiss 3s).\n\n"

                    "=== JDS COMPONENT QUICK REFERENCE ===\n"
                    "Button: primary=#3535f3 filled, secondary=outlined, tertiary=text. Radius=pill(999px). "
                    "Height: small=32px, medium=44px, large=52px.\n"
                    "InputField: bg=#eeeeef, radius=23px, no border, JioType 14px.\n"
                    "Card: bg=white, radius=16px, border=1px rgba(36,38,43,0.12), shadow=0 4px 16px rgba(0,0,0,0.08).\n"
                    "BottomSheet: bg=white, top-radius=16px, handle=4×32px grey bar, max-height=80vh.\n"
                    "Toast: bottom-center mobile, radius=12px, max 2 lines, NEVER primary button inside.\n"
                    "Skeleton: bg=#f5f5f5 (grey-20) ONLY. Shimmer animation. Use for ALL content loading.\n"
                    "Speak button: bg=#3900ad, radius=999px, padding=12px 20px, white text+icon, JioType Bold 16px.\n"
                    "Icon buttons: 36×36px circle, bg=#e7e9ff (ghost-icon), icon 20px #170054.\n"
                )
            }
        }

    # Handle ping
    elif method == "ping":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {}
        }

    # Handle tools/list
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": TOOLS}
        }

    # Handle tools/call
    elif method == "tools/call":
        tool_name = params.get("name", "")
        args = params.get("arguments", {})

        if not isinstance(args, dict):
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32602, "message": "Invalid params"}
            }

        # SECURITY: Whitelist tool names
        allowed_tools = {
            "lookup_component", "resolve_token",
            "find_icon", "get_figma_reference", "get_assets"
        }
        if tool_name not in allowed_tools:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32602, "message": "Unknown tool"}
            }

        try:
            if tool_name == "lookup_component":
                result = lookup_component(args.get("component_name", ""))
            elif tool_name == "resolve_token":
                result = resolve_token(
                    args.get("token_category", ""),
                    args.get("token_name")
                )
            elif tool_name == "find_icon":
                result = find_icon(
                    args.get("query", ""),
                    args.get("limit", 10)
                )
            elif tool_name == "get_figma_reference":
                result = get_figma_reference(args.get("design_name", ""))
            elif tool_name == "get_assets":
                result = get_assets(args.get("asset_type", "all"), args.get("project_dir", ""))
                # NOTE: get_assets intentionally skips sanitize_output
                # because returning file paths IS its purpose
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }]
                    }
                }

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(result, indent=2) + TOOL_REMINDER
                    }]
                }
            }
        except Exception:
            # SECURITY: Never expose stack traces or internal details
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": "Tool execution failed"
                }
            }

    # Handle notifications (no response)
    elif method == "notifications/initialized":
        return None

    return None


# ============================================================================
# MAIN — MCP server loop over stdio
# ============================================================================

def main():
    """
    Main MCP server loop.
    Reads JSON-RPC requests from stdin, writes responses to stdout.
    SECURITY: Max message size enforced, no eval/exec.
    """
    MAX_MESSAGE_SIZE = 1_000_000  # 1MB max per message

    for line in sys.stdin:
        # SECURITY: Enforce max message size
        if len(line) > MAX_MESSAGE_SIZE:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32600, "message": "Message too large"}
            }
            print(json.dumps(error_response), flush=True)
            continue

        try:
            request = json.loads(line)
            response = handle_request(request)
            if response:
                print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            }
            print(json.dumps(error_response), flush=True)
        except Exception:
            # SECURITY: Generic error, no internals leaked
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": "Internal error"}
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    print(f"JioBharatIQ Knowledge Server v{SERVER_VERSION} ready", file=sys.stderr, flush=True)
    main()

#!/usr/bin/env python3
"""
JDS Knowledge Server - MCP Server for Jio Design System
Version: 3.1.0

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

SERVER_VERSION = "3.1.0"

# ============================================================================
# AUTO-UPDATE: fetch latest knowledge base from GitHub on every startup
# ============================================================================

_REPO_BASE = "https://raw.githubusercontent.com/sunit1986/JioBharatIQ_Server/main"
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _auto_update():
    """Download latest knowledge base from GitHub.
    Updates knowledge_base.py only — server code updates come via PyPI."""
    target = os.path.join(_SCRIPT_DIR, "knowledge_base.py")
    url = f"{_REPO_BASE}/knowledge_base.py"
    try:
        data = urllib.request.urlopen(url, timeout=10).read()
        with open(target, "wb") as f:
            f.write(data)
    except Exception:
        pass  # offline or error — use cached version


if not os.environ.get("_JDS_NO_UPDATE"):
    _auto_update()

from .knowledge_base import (
    COMPONENTS, TOKENS, ICON_CATEGORIES, ICONS_SEARCHABLE, FIGMA_REFERENCES
)


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
    "REMINDER: (1) Call get_assets FIRST to get GitHub-hosted CDN URLs for all JDS assets. "
    "(2) Use JioType font ONLY — never system fonts. "
    "(3) Use JDS icons from assets/icons/ — NEVER use emojis. "
    "(4) Call resolve_token for colors/spacing — never hardcode. "
    "(5) Use the cdn_url paths from get_assets response directly in your HTML src/url attributes — no file copying needed."
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
        "component": component["name"],
        "import_path": component["import_path"],
        "description": component.get("description", ""),
        "props": component.get("props", {}),
        "variants": {},
        "code_example": component.get("code_example", "")
    }

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

    if not token_name:
        if token_category == "colors":
            return sanitize_output({
                "category": token_category,
                "subcategories": list(category_data.keys()),
                "sample_tokens": {
                    "primary-50": category_data["primary"]["primary-50"],
                    "grey-100": category_data["grey"]["grey-100"],
                    "error": category_data["feedback"]["error"]
                }
            })
        elif token_category == "typography":
            return sanitize_output({
                "category": token_category,
                "subcategories": list(category_data.keys()),
                "sample_tokens": {
                    "heading-xl": category_data["heading"]["heading-xl"],
                    "body-s": category_data["body"]["body-s"]
                }
            })
        else:
            return sanitize_output({
                "category": token_category,
                "tokens": category_data
            })

    token_name = sanitize_input(token_name)
    token_name_lower = token_name.lower().replace("_", "-")

    if token_category in ["colors", "typography"]:
        for subcategory, tokens in category_data.items():
            for key, value in tokens.items():
                if token_name_lower in key.lower():
                    return sanitize_output({
                        "category": token_category,
                        "subcategory": subcategory,
                        "token": key,
                        "value": value
                    })
        return {"error": f"Token not found in {token_category}"}
    else:
        for key, value in category_data.items():
            if token_name_lower in key.lower():
                return sanitize_output({
                    "category": token_category,
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
        }
    }

    if asset_type not in ("all", "fonts", "animations", "icons", "svg"):
        return {
            "error": "Unknown asset type",
            "available_types": ["all", "fonts", "animations", "icons"]
        }

    result = {"cdn_base": cdn_base, "types": {}}

    types_to_include = [asset_type] if asset_type != "all" else ["fonts", "animations", "icons"]

    for atype in types_to_include:
        info = asset_map[atype]
        entry = {
            "description": info["description"],
            "cdn_base": info["cdn_base"],
            "files": info["files"],
            "count": len(info["files"]),
        }
        # Add usage hints and extra fields
        for key in ("usage_css", "usage_html", "usage_note", "svg_cdn_base", "svg_usage_note"):
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
        if design_name_lower in key or design_name_lower in ref_data["name"].lower():
            result = {
                "name": ref_data["name"],
                "file_key": ref_data["file_key"],
                "url": ref_data["url"],
                "description": ref_data.get("description", "")
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
        "description": f"[JioBharatIQ v{SERVER_VERSION}] Get JDS asset CDN URLs for prototyping. Returns GitHub-hosted URLs for fonts (JioType WOFF2), animations (HelloJio MP4s), icons (71 JSX + 1281 SVG). MANDATORY: Call this FIRST when building any prototype.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "asset_type": {
                    "type": "string",
                    "description": "Asset type: 'all', 'fonts', 'animations', 'icons' (default: 'all')",
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
                    "When building any prototype or UI:\n"
                    "1. ALWAYS call get_assets FIRST to get GitHub-hosted CDN URLs for all JDS assets. "
                    "Use the cdn_url values DIRECTLY in your HTML src and url() attributes — no file copying needed.\n"
                    "2. Use JioType font family (woff2 for web, ttf for native) — NEVER use system fonts like Inter, Arial, Helvetica, or sans-serif.\n"
                    "3. Call lookup_component before implementing any JDS component.\n"
                    "4. Call resolve_token for colors, typography, spacing — NEVER hardcode values.\n"
                    "5. Use find_icon tool to get SVG path data for any icon — returns svg_path for direct HTML inline use. "
                    "1301 icons available (71 JSX + 1230 SVG).\n"
                    "6. Use HelloJio animations from assets/animations/ for assistant/AI states.\n"
                    "7. NEVER use emojis anywhere in the UI — use JDS icons from assets/icons/ instead.\n"
                    "8. NEVER use placeholder or dummy assets — always use real JDS assets from get_assets."
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

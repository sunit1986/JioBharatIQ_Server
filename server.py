#!/usr/bin/env python3
"""
JDS Knowledge Server - MCP Server for Jio Design System
Version: 1.0.0

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
import re
import sys
from knowledge_base import (
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
            results.append({
                "icon": icon_name,
                "category": icon_data["category"],
                "keywords": icon_data["keywords"],
                "match_type": "name"
            })
        elif any(query_lower in keyword for keyword in icon_data["keywords"]):
            results.append({
                "icon": icon_name,
                "category": icon_data["category"],
                "keywords": icon_data["keywords"],
                "match_type": "keyword"
            })

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
        "description": "Get JDS component specs: Button, Card, InputField, Modal, BottomSheet, Avatar, Tabs, Toast, Accordion, Divider, Badge, BottomNav, Container, Spinner, Skeleton, PromoCard, ServiceCard, ContentBlock, Carousel, RatingBar, Text",
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
        "description": "Search JDS icon library (1546 icons across 15 categories)",
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

    # Handle initialize
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "jds-knowledge-server",
                    "version": "1.0.0"
                }
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
            "find_icon", "get_figma_reference"
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
    main()

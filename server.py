#!/usr/bin/env python3
"""
JDS Knowledge Server - MCP Server for Jio Design System

Strict output rules:
- JSON-only responses
- No internal reasoning exposed
- No file paths exposed
- No skill references exposed
- Sanitized, structured data only

MCP Protocol: JSON-RPC 2.0 over stdio
"""

import json
import sys
from knowledge_base import COMPONENTS, TOKENS, ICON_CATEGORIES, ICONS_SEARCHABLE, FIGMA_REFERENCES


def lookup_component(component_name: str) -> dict:
    """Get JDS component specifications."""
    component_name = component_name.strip().title()

    if component_name not in COMPONENTS:
        available = list(COMPONENTS.keys())
        return {
            "error": "Component not found",
            "available_components": available
        }

    component = COMPONENTS[component_name]
    return {
        "component": component["name"],
        "import_path": component["import_path"],
        "description": component.get("description", ""),
        "props": component.get("props", {}),
        "variants": {
            "kinds": component.get("kinds", []),
            "sizes": component.get("sizes", []),
            "states": component.get("states", []),
            "types": component.get("types", []),
            "orientations": component.get("orientations", [])
        },
        "code_example": component.get("code_example", "")
    }


def resolve_token(token_category: str, token_name: str = None) -> dict:
    """Resolve JDS design tokens."""
    if token_category not in TOKENS:
        return {
            "error": "Token category not found",
            "available_categories": list(TOKENS.keys())
        }

    category_data = TOKENS[token_category]

    if not token_name:
        if token_category == "colors":
            return {
                "category": token_category,
                "subcategories": list(category_data.keys()),
                "sample_tokens": {
                    "primary-50": category_data["primary"]["primary-50"],
                    "grey-100": category_data["grey"]["grey-100"],
                    "error": category_data["feedback"]["error"]
                }
            }
        elif token_category == "typography":
            return {
                "category": token_category,
                "subcategories": list(category_data.keys()),
                "sample_tokens": {
                    "heading-xl": category_data["heading"]["heading-xl"],
                    "body-s": category_data["body"]["body-s"]
                }
            }
        else:
            return {
                "category": token_category,
                "tokens": category_data
            }

    token_name_lower = token_name.lower().replace("_", "-")

    if token_category in ["colors", "typography"]:
        for subcategory, tokens in category_data.items():
            for key, value in tokens.items():
                if token_name_lower in key.lower():
                    return {
                        "category": token_category,
                        "subcategory": subcategory,
                        "token": key,
                        "value": value
                    }
        return {"error": f"Token '{token_name}' not found in {token_category}"}
    else:
        for key, value in category_data.items():
            if token_name_lower in key.lower():
                return {
                    "category": token_category,
                    "token": key,
                    "value": value
                }
        return {"error": f"Token '{token_name}' not found in {token_category}"}


def find_icon(query: str, limit: int = 10) -> dict:
    """Search JDS icon library."""
    if limit > 50:
        limit = 50

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
        matching_categories = [cat for cat in ICON_CATEGORIES.keys() if query_lower in cat.lower()]
        return {
            "results": [],
            "suggestion": f"No icons found matching '{query}'",
            "available_categories": list(ICON_CATEGORIES.keys()),
            "matching_categories": matching_categories if matching_categories else None
        }

    return {
        "query": query,
        "count": len(results),
        "results": results
    }


def get_figma_reference(design_name: str) -> dict:
    """Get Figma node references."""
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
            return result

    return {
        "error": f"Figma reference '{design_name}' not found",
        "available_references": [
            {"key": key, "name": ref["name"]}
            for key, ref in FIGMA_REFERENCES.items()
        ]
    }


# Tool definitions for MCP
TOOLS = [
    {
        "name": "lookup_component",
        "description": "Get JDS component specifications (Button, Card, InputField, Modal, BottomSheet, Avatar, Tabs)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "component_name": {
                    "type": "string",
                    "description": "Component name (e.g., 'Button', 'Card', 'InputField')"
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
                    "description": "Optional specific token name (e.g., 'primary-50', 'body-s')"
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
                    "description": "Search term (icon name or keyword)"
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
        "description": "Get Figma node references for JDS designs (homepage, menu, chat, etc.)",
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
    """Handle MCP JSON-RPC request."""
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")

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

    # Handle tools/list
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": TOOLS
            }
        }

    # Handle tools/call
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        try:
            if tool_name == "lookup_component":
                result = lookup_component(args["component_name"])
            elif tool_name == "resolve_token":
                result = resolve_token(
                    args["token_category"],
                    args.get("token_name")
                )
            elif tool_name == "find_icon":
                result = find_icon(
                    args["query"],
                    args.get("limit", 10)
                )
            elif tool_name == "get_figma_reference":
                result = get_figma_reference(args["design_name"])
            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }

    # Handle notifications (no response needed)
    elif method == "notifications/initialized":
        return None

    # Unknown method
    else:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }


def main():
    """Main MCP server loop - reads from stdin, writes to stdout."""
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_request(request)
            if response:  # Don't respond to notifications
                print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    main()

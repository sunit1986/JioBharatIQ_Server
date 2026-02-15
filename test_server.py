#!/usr/bin/env python3
"""
Comprehensive test suite for JDS Knowledge Server.

Tests cover:
1. All 4 tools — happy paths
2. Edge cases — missing args, empty strings, unknown values
3. Security — injection attempts, path traversal, oversized inputs
4. MCP protocol — initialize, tools/list, tools/call, unknown methods
5. Output structure — strict JSON validation
6. Data integrity — all components, tokens, icons, figma refs
"""

import json
import subprocess
import sys
import os

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

passed = 0
failed = 0
warnings = 0


def send_request(request_dict: dict) -> dict:
    """Send a JSON-RPC request to the server and get the response."""
    server_path = os.path.join(os.path.dirname(__file__), "server.py")
    proc = subprocess.run(
        [sys.executable, server_path],
        input=json.dumps(request_dict) + "\n",
        capture_output=True,
        text=True,
        timeout=10
    )
    if proc.returncode != 0 and proc.stderr:
        return {"_error": proc.stderr}
    if proc.stdout.strip():
        return json.loads(proc.stdout.strip().split("\n")[0])
    return {}


def call_tool(tool_name: str, arguments: dict) -> dict:
    """Helper to call an MCP tool and return the parsed result."""
    response = send_request({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    })
    if "result" in response and "content" in response["result"]:
        text = response["result"]["content"][0]["text"]
        return json.loads(text)
    return response


def test(name: str, condition: bool, detail: str = ""):
    """Record a test result."""
    global passed, failed
    if condition:
        passed += 1
        print(f"  {GREEN}PASS{RESET}  {name}")
    else:
        failed += 1
        print(f"  {RED}FAIL{RESET}  {name}")
        if detail:
            print(f"        {detail}")


def warn(name: str, detail: str = ""):
    """Record a warning (non-fatal)."""
    global warnings
    warnings += 1
    print(f"  {YELLOW}WARN{RESET}  {name}")
    if detail:
        print(f"        {detail}")


# ============================================================================
# TEST GROUP 1: MCP Protocol
# ============================================================================

def test_mcp_protocol():
    print(f"\n{BOLD}{CYAN}=== MCP Protocol Tests ==={RESET}")

    # Initialize
    resp = send_request({
        "jsonrpc": "2.0", "id": 1,
        "method": "initialize", "params": {}
    })
    test("Initialize returns protocolVersion",
         resp.get("result", {}).get("protocolVersion") == "2024-11-05")
    test("Initialize returns serverInfo",
         resp.get("result", {}).get("serverInfo", {}).get("name") == "jds-knowledge-server")
    test("Initialize returns tools capability",
         "tools" in resp.get("result", {}).get("capabilities", {}))

    # Tools list
    resp = send_request({
        "jsonrpc": "2.0", "id": 2,
        "method": "tools/list", "params": {}
    })
    tools = resp.get("result", {}).get("tools", [])
    test("tools/list returns 4 tools", len(tools) == 4)
    tool_names = {t["name"] for t in tools}
    test("All tool names present",
         tool_names == {"lookup_component", "resolve_token", "find_icon", "get_figma_reference"})

    # Each tool has inputSchema
    for tool in tools:
        test(f"Tool '{tool['name']}' has inputSchema",
             "inputSchema" in tool and "properties" in tool["inputSchema"])

    # Ping
    resp = send_request({
        "jsonrpc": "2.0", "id": 3,
        "method": "ping", "params": {}
    })
    test("Ping returns empty result", resp.get("result") == {})

    # Unknown method
    resp = send_request({
        "jsonrpc": "2.0", "id": 4,
        "method": "unknown/method", "params": {}
    })
    test("Unknown method returns error",
         "error" in resp and resp["error"]["code"] == -32601)

    # Invalid JSON (tested via malformed input)
    proc = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(__file__), "server.py")],
        input="not json\n",
        capture_output=True, text=True, timeout=10
    )
    if proc.stdout.strip():
        resp = json.loads(proc.stdout.strip())
        test("Malformed JSON returns parse error",
             resp.get("error", {}).get("code") == -32700)
    else:
        test("Malformed JSON returns parse error", False, "No output")


# ============================================================================
# TEST GROUP 2: lookup_component
# ============================================================================

def test_lookup_component():
    print(f"\n{BOLD}{CYAN}=== lookup_component Tests ==={RESET}")

    # All components that should exist
    expected_components = [
        "Button", "InputField", "Card", "Modal", "BottomSheet",
        "Avatar", "Tabs", "Toast", "Accordion", "Divider",
        "Badge", "BottomNav", "Container", "Spinner", "Skeleton",
        "PromoCard", "ServiceCard", "ContentBlock", "Carousel",
        "RatingBar", "Text"
    ]

    for comp in expected_components:
        result = call_tool("lookup_component", {"component_name": comp})
        test(f"Component '{comp}' found",
             result.get("component") == comp,
             f"Got: {result.get('error', result.get('component', 'N/A'))}")

    # Verify structure for Button
    result = call_tool("lookup_component", {"component_name": "Button"})
    test("Button has import_path", result.get("import_path") == "@jds/core")
    test("Button has props dict", isinstance(result.get("props"), dict))
    test("Button has code_example", len(result.get("code_example", "")) > 0)
    test("Button has description", len(result.get("description", "")) > 0)
    test("Button has variants", isinstance(result.get("variants"), dict))

    # Case insensitivity
    result = call_tool("lookup_component", {"component_name": "button"})
    test("Case insensitive: 'button' -> Button",
         result.get("component") == "Button")

    result = call_tool("lookup_component", {"component_name": "CARD"})
    test("Case insensitive: 'CARD' -> Card",
         result.get("component") == "Card")

    # Aliases
    result = call_tool("lookup_component", {"component_name": "bottom sheet"})
    test("Alias: 'bottom sheet' -> BottomSheet",
         result.get("component") == "BottomSheet")

    result = call_tool("lookup_component", {"component_name": "input field"})
    test("Alias: 'input field' -> InputField",
         result.get("component") == "InputField")

    # Unknown component
    result = call_tool("lookup_component", {"component_name": "FooBar"})
    test("Unknown component returns error", "error" in result)
    test("Unknown component lists available",
         "available_components" in result and len(result["available_components"]) >= 21)

    # Empty string
    result = call_tool("lookup_component", {"component_name": ""})
    test("Empty string returns error", "error" in result)


# ============================================================================
# TEST GROUP 3: resolve_token
# ============================================================================

def test_resolve_token():
    print(f"\n{BOLD}{CYAN}=== resolve_token Tests ==={RESET}")

    # Category overview
    for category in ["colors", "typography", "spacing", "border_radius", "opacity"]:
        result = call_tool("resolve_token", {"token_category": category})
        test(f"Category '{category}' returns data", "error" not in result)

    # Colors overview
    result = call_tool("resolve_token", {"token_category": "colors"})
    test("Colors has subcategories",
         "subcategories" in result and "primary" in result["subcategories"])
    test("Colors has sample_tokens", "sample_tokens" in result)

    # Specific token lookups
    result = call_tool("resolve_token",
                       {"token_category": "colors", "token_name": "primary-50"})
    test("primary-50 resolves to #3535f3",
         result.get("value", {}).get("value") == "#3535f3")

    result = call_tool("resolve_token",
                       {"token_category": "colors", "token_name": "error"})
    test("error token resolves to #fa2F40",
         result.get("value", {}).get("value") == "#fa2F40")

    result = call_tool("resolve_token",
                       {"token_category": "colors", "token_name": "grey-100"})
    test("grey-100 resolves to #141414",
         result.get("value", {}).get("value") == "#141414")

    # Typography
    result = call_tool("resolve_token",
                       {"token_category": "typography", "token_name": "heading-xl"})
    test("heading-xl is 88px JioType Black",
         result.get("value", {}).get("size") == "88px" and
         result.get("value", {}).get("weight") == "Black")

    result = call_tool("resolve_token",
                       {"token_category": "typography", "token_name": "body-s"})
    test("body-s is 16px JioType Medium",
         result.get("value", {}).get("size") == "16px" and
         result.get("value", {}).get("weight") == "Medium")

    # Spacing
    result = call_tool("resolve_token",
                       {"token_category": "spacing", "token_name": "base"})
    test("spacing 'base' is 16px",
         result.get("value", {}).get("value") == "16px")

    # Border radius
    result = call_tool("resolve_token",
                       {"token_category": "border_radius", "token_name": "pill"})
    test("border_radius 'pill' is 999px",
         result.get("value", {}).get("value") == "999px")

    # Unknown category
    result = call_tool("resolve_token", {"token_category": "fake_category"})
    test("Unknown category returns error", "error" in result)

    # Unknown token
    result = call_tool("resolve_token",
                       {"token_category": "colors", "token_name": "nonexistent"})
    test("Unknown token returns error", "error" in result)


# ============================================================================
# TEST GROUP 4: find_icon
# ============================================================================

def test_find_icon():
    print(f"\n{BOLD}{CYAN}=== find_icon Tests ==={RESET}")

    # Name match
    result = call_tool("find_icon", {"query": "mic"})
    test("'mic' finds ic_mic", result.get("count", 0) > 0)

    # Keyword match
    result = call_tool("find_icon", {"query": "voice"})
    test("'voice' finds icons via keyword",
         result.get("count", 0) > 0)

    result = call_tool("find_icon", {"query": "calendar"})
    test("'calendar' finds icons",
         result.get("count", 0) >= 1)

    result = call_tool("find_icon", {"query": "heart"})
    test("'heart' keyword match",
         result.get("count", 0) > 0)

    # Limit enforcement
    result = call_tool("find_icon", {"query": "ic", "limit": 3})
    test("Limit=3 returns at most 3",
         result.get("count", 0) <= 3)

    result = call_tool("find_icon", {"query": "ic", "limit": 100})
    test("Limit capped at 50",
         result.get("count", 0) <= 50)

    # No results
    result = call_tool("find_icon", {"query": "zzzznonexistent"})
    test("No results returns suggestion",
         "suggestion" in result and result.get("results") == [])
    test("No results includes available_categories",
         "available_categories" in result)

    # Empty query
    result = call_tool("find_icon", {"query": ""})
    test("Empty query returns error", "error" in result)


# ============================================================================
# TEST GROUP 5: get_figma_reference
# ============================================================================

def test_figma_reference():
    print(f"\n{BOLD}{CYAN}=== get_figma_reference Tests ==={RESET}")

    expected_refs = {
        "homepage": "AI Assistant Homepage",
        "menu": "Hamburger Menu",
        "chat_page": "Chat Page",
        "media_page": "Media Page",
        "assistants_page": "Assistants Page",
        "tools_page": "Tools Page",
        "oneui_design_kit": "OneUI Design Kit (BETA)",
        "jio_testlab": "Jio Testlab Library",
        "chat_input": "Chat Input",
    }

    for key, expected_name in expected_refs.items():
        result = call_tool("get_figma_reference", {"design_name": key})
        test(f"Reference '{key}' found",
             result.get("name") == expected_name,
             f"Got: {result.get('error', result.get('name', 'N/A'))}")

    # Homepage has all fields
    result = call_tool("get_figma_reference", {"design_name": "homepage"})
    test("Homepage has file_key", "file_key" in result)
    test("Homepage has node_id", "node_id" in result)
    test("Homepage has url", "url" in result and "figma.com" in result.get("url", ""))
    test("Homepage has description", len(result.get("description", "")) > 0)

    # Unknown reference
    result = call_tool("get_figma_reference", {"design_name": "nonexistent_design"})
    test("Unknown ref returns error", "error" in result)
    test("Unknown ref lists available",
         "available_references" in result and len(result["available_references"]) >= 9)


# ============================================================================
# TEST GROUP 6: Security Tests
# ============================================================================

def test_security():
    print(f"\n{BOLD}{CYAN}=== Security Tests ==={RESET}")

    # Injection attempts in component name
    injection_payloads = [
        "__import__('os').system('ls')",
        "'; DROP TABLE components; --",
        "<script>alert('xss')</script>",
        "../../etc/passwd",
        "${env.SECRET_KEY}",
        "{{7*7}}",
        "`whoami`",
        "Button\"; cat /etc/passwd; echo \"",
    ]

    for payload in injection_payloads:
        result = call_tool("lookup_component", {"component_name": payload})
        test(f"Injection blocked: {payload[:40]}...",
             "error" in result or result.get("component") is None)

    # Path traversal in token name
    result = call_tool("resolve_token",
                       {"token_category": "../../etc/passwd", "token_name": "test"})
    test("Path traversal blocked in token_category", "error" in result)

    # Oversized input
    huge_input = "A" * 10000
    result = call_tool("lookup_component", {"component_name": huge_input})
    test("Oversized input handled gracefully",
         "error" in result)

    # No file paths in output
    for comp_name in ["Button", "Card", "Modal"]:
        result = call_tool("lookup_component", {"component_name": comp_name})
        result_str = json.dumps(result)
        test(f"No file paths in {comp_name} output",
             "/Users/" not in result_str and
             "/home/" not in result_str and
             ".claude/" not in result_str and
             "memory/" not in result_str)

    # No secrets in output
    for category in ["colors", "typography", "spacing"]:
        result = call_tool("resolve_token", {"token_category": category})
        result_str = json.dumps(result)
        test(f"No secrets in {category} tokens",
             "password" not in result_str.lower() and
             "api_key" not in result_str.lower() and
             "secret" not in result_str.lower())

    # Unknown tool name
    resp = send_request({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": "exec_command", "arguments": {"cmd": "ls"}}
    })
    test("Unknown tool 'exec_command' rejected",
         "error" in resp)

    # Invalid params type
    resp = send_request({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": "lookup_component", "arguments": "not a dict"}
    })
    test("Non-dict arguments rejected",
         "error" in resp)

    # Method not in whitelist
    for method in ["__import__", "eval", "exec", "system", "resources/list",
                   "prompts/list", "completions/create"]:
        resp = send_request({
            "jsonrpc": "2.0", "id": 1,
            "method": method, "params": {}
        })
        test(f"Method '{method}' blocked",
             "error" in resp)


# ============================================================================
# TEST GROUP 7: Output Structure Validation
# ============================================================================

def test_output_structure():
    print(f"\n{BOLD}{CYAN}=== Output Structure Tests ==={RESET}")

    # All component results must have these exact keys
    required_keys = {"component", "import_path", "description", "props", "variants", "code_example"}
    for comp in ["Button", "Card", "Toast", "Text"]:
        result = call_tool("lookup_component", {"component_name": comp})
        actual_keys = set(result.keys())
        has_all = required_keys.issubset(actual_keys)
        test(f"'{comp}' result has all required keys",
             has_all,
             f"Missing: {required_keys - actual_keys}" if not has_all else "")

    # Token results must be structured
    result = call_tool("resolve_token",
                       {"token_category": "colors", "token_name": "primary-50"})
    test("Token result has category", "category" in result)
    test("Token result has subcategory", "subcategory" in result)
    test("Token result has token name", "token" in result)
    test("Token result has value object", "value" in result)

    # Icon results must be structured
    result = call_tool("find_icon", {"query": "home"})
    test("Icon result has count", "count" in result)
    test("Icon result has results array", isinstance(result.get("results"), list))
    if result.get("results"):
        icon = result["results"][0]
        test("Icon entry has 'icon' key", "icon" in icon)
        test("Icon entry has 'category' key", "category" in icon)
        test("Icon entry has 'keywords' key", "keywords" in icon)
        test("Icon entry has 'match_type' key", "match_type" in icon)

    # Figma results must be structured
    result = call_tool("get_figma_reference", {"design_name": "homepage"})
    test("Figma result has 'name'", "name" in result)
    test("Figma result has 'file_key'", "file_key" in result)
    test("Figma result has 'url'", "url" in result)

    # JSON serializable check — every response must be valid JSON
    for tool, args in [
        ("lookup_component", {"component_name": "Button"}),
        ("resolve_token", {"token_category": "colors"}),
        ("find_icon", {"query": "mic"}),
        ("get_figma_reference", {"design_name": "homepage"}),
    ]:
        result = call_tool(tool, args)
        try:
            json.dumps(result)
            test(f"'{tool}' output is JSON serializable", True)
        except (TypeError, ValueError) as e:
            test(f"'{tool}' output is JSON serializable", False, str(e))


# ============================================================================
# TEST GROUP 8: Data Integrity (matching CLAUDE.md)
# ============================================================================

def test_data_integrity():
    print(f"\n{BOLD}{CYAN}=== Data Integrity Tests ==={RESET}")

    # Button must match CLAUDE.md spec
    result = call_tool("lookup_component", {"component_name": "Button"})
    props = result.get("props", {})
    test("Button.kind has primary/secondary/tertiary",
         "primary" in str(props.get("kind", {}).get("options", [])))
    test("Button has onClick prop", "onClick" in props)
    test("Button import is @jds/core", result.get("import_path") == "@jds/core")

    # Typography tokens match CLAUDE.md
    result = call_tool("resolve_token",
                       {"token_category": "typography", "token_name": "heading-xl"})
    val = result.get("value", {})
    test("heading-xl: 88px size", val.get("size") == "88px")
    test("heading-xl: -3% letter spacing", val.get("letter_spacing") == "-3%")
    test("heading-xl: Black weight", val.get("weight") == "Black")
    test("heading-xl: JioType font", val.get("font") == "JioType")

    result = call_tool("resolve_token",
                       {"token_category": "typography", "token_name": "body-xs"})
    val = result.get("value", {})
    test("body-xs: 14px size", val.get("size") == "14px")
    test("body-xs: -0.5% letter spacing", val.get("letter_spacing") == "-0.5%")
    test("body-xs: Medium weight", val.get("weight") == "Medium")

    # Color tokens match CLAUDE.md
    result = call_tool("resolve_token",
                       {"token_category": "colors", "token_name": "primary-60"})
    test("primary-60 is #000093 (links)",
         result.get("value", {}).get("value") == "#000093")

    result = call_tool("resolve_token",
                       {"token_category": "colors", "token_name": "sparkle-50"})
    test("sparkle-50 is #1eccb0",
         result.get("value", {}).get("value") == "#1eccb0")

    # Border radius xxl = 23px (input fields, cards)
    result = call_tool("resolve_token",
                       {"token_category": "border_radius", "token_name": "xxl"})
    test("border_radius xxl is 23px (chat input)",
         result.get("value", {}).get("value") == "23px")

    # Figma homepage node ID matches CLAUDE.md
    result = call_tool("get_figma_reference", {"design_name": "homepage"})
    test("Homepage file_key is yvWQ7pqZSgFIfO0XrzY1me",
         result.get("file_key") == "yvWQ7pqZSgFIfO0XrzY1me")
    test("Homepage node_id is 13157:2011",
         result.get("node_id") == "13157:2011")

    # Chat input reference
    result = call_tool("get_figma_reference", {"design_name": "chat_input"})
    test("Chat input file_key is b95Apii4f27AoRxhm0nJZq",
         result.get("file_key") == "b95Apii4f27AoRxhm0nJZq")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    print(f"\n{BOLD}{'='*60}")
    print(f"  JDS Knowledge Server — Comprehensive Test Suite")
    print(f"{'='*60}{RESET}")

    test_mcp_protocol()
    test_lookup_component()
    test_resolve_token()
    test_find_icon()
    test_figma_reference()
    test_security()
    test_output_structure()
    test_data_integrity()

    print(f"\n{BOLD}{'='*60}")
    print(f"  RESULTS: {GREEN}{passed} passed{RESET}, {RED}{failed} failed{RESET}, {YELLOW}{warnings} warnings{RESET}")
    print(f"{'='*60}{RESET}\n")

    if failed > 0:
        sys.exit(1)
    else:
        print(f"  {GREEN}{BOLD}ALL TESTS PASSED{RESET}\n")
        sys.exit(0)

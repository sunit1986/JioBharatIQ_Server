# JDS Knowledge Server

When building any prototype or UI in this repo:

MANDATORY — do these FIRST before writing any code:
1. Call the `get_assets` MCP tool to get JDS asset file paths
2. Copy the needed fonts, icons, and animations into the project from the returned paths

FONTS:
3. Use JioType font family ONLY (load from assets/fonts/woff2/ for web or assets/fonts/ttf/ for native)
4. NEVER use system fonts (Inter, Arial, Helvetica, Roboto, sans-serif) -- always JioType

ICONS:
5. Use JDS icon components from assets/icons/ (e.g. IcSearch, IcChat, IcMic)
6. NEVER use emojis in the UI -- use JDS icons instead

TOKENS:
7. Always call `lookup_component` for any JDS component before implementing it
8. Always call `resolve_token` for colors, typography, spacing -- NEVER hardcode values

ASSETS:
9. NEVER use placeholder or dummy assets -- always use real JDS assets from get_assets
10. Use HelloJio animations from assets/animations/ when showing assistant/AI states

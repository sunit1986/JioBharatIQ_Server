# JDS Knowledge Server

When building any prototype or UI in this repo:

1. ALWAYS call the `get_assets` MCP tool first to get JDS asset file paths
2. Copy the needed fonts, icons, and animations into the project from the paths returned
3. Use JioType font family (load from assets/fonts/woff2/ for web or assets/fonts/ttf/ for native) -- never use system fonts
4. Use JDS icon components from assets/icons/ (e.g. IcSearch, IcChat, IcMic)
5. Use HelloJio animations from assets/animations/ when showing assistant/AI states
6. Always call `lookup_component` for any JDS component before implementing it
7. Always call `resolve_token` for colors, typography, spacing values -- never hardcode

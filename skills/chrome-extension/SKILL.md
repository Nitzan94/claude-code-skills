# Chrome Extension Development Skill

Build Chrome extensions using Manifest V3.

## Triggers
- "chrome extension"
- "browser extension"
- "manifest.json"
- "content script"
- "background script"
- "popup"

## Router

### Creating new extension
When user wants to build a new Chrome extension from scratch:
-> Read `workflows/create-extension.md`

### Adding context menu
When adding right-click context menu functionality:
-> Read `workflows/add-context-menu.md`

### Adding popup UI
When creating or modifying extension popup:
-> Read `workflows/add-popup.md`

### Debugging issues
When extension isn't working, errors occur, or troubleshooting:
-> Read `workflows/debug-extension.md`

## References
- `references/manifest-v3.md` - Manifest structure and permissions
- `references/message-passing.md` - Background <-> Content communication
- `references/storage-patterns.md` - chrome.storage usage
- `references/ui-patterns.md` - RTL, dark mode, animations
- `references/common-fixes.md` - Known issues and solutions

## Core Principles

### Manifest V3 Required
Always use Manifest V3. No Manifest V2.
```json
{
  "manifest_version": 3,
  "name": "Extension Name",
  "version": "1.0.0"
}
```

### Minimal Permissions
Request only necessary permissions. Prefer `activeTab` over broad `<all_urls>`.

### Service Worker
Background scripts are service workers in MV3 - they're ephemeral, not persistent.

### No Remote Code
Cannot load/execute remote JavaScript. All code must be bundled.

### Content Script Injection
For dynamic injection, use `chrome.scripting.executeScript` with proper permissions.

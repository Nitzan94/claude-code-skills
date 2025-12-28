# Chrome Extension

A Claude Code skill for building Chrome extensions with Manifest V3.

## What It Does

Guides you through building Chrome extensions with:
- Manifest V3 (required, no V2)
- Content scripts
- Background service workers
- Popup UIs
- Context menus
- Message passing
- Storage patterns

## Usage

In Claude Code, mention:
- "chrome extension"
- "browser extension"
- "manifest.json"
- "content script"
- "popup"

Or invoke directly: `/chrome-extension`

## Workflows

| Task | What You Get |
|------|--------------|
| Create extension | Full project structure with manifest, scripts, icons |
| Add context menu | Right-click menu with action handlers |
| Add popup | HTML/CSS/JS popup with storage integration |
| Debug | Troubleshooting common extension issues |

## Core Principles

### Manifest V3 Only
```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0"
}
```

### Minimal Permissions
Prefer `activeTab` over broad `<all_urls>`. Only request what you need.

### Service Workers
Background scripts are ephemeral service workers in MV3 - they don't persist.

### No Remote Code
All JavaScript must be bundled. Cannot load/execute remote scripts.

## References Included

- `manifest-v3.md` - Manifest structure and permissions
- `message-passing.md` - Background <-> Content communication
- `storage-patterns.md` - chrome.storage usage
- `ui-patterns.md` - RTL, dark mode, animations
- `common-fixes.md` - Known issues and solutions

## When to Use

- Building a new Chrome extension
- Adding features to existing extension
- Debugging extension issues
- Learning Manifest V3 patterns

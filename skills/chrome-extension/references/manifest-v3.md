# Manifest V3 Reference

## Complete manifest.json Template

```json
{
  "manifest_version": 3,
  "name": "Extension Name",
  "version": "1.0.0",
  "description": "Brief description of what the extension does",

  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },

  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    },
    "default_title": "Click to open"
  },

  "background": {
    "service_worker": "background.js"
  },

  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "css": ["content.css"],
      "run_at": "document_idle"
    }
  ],

  "permissions": [
    "storage",
    "activeTab",
    "contextMenus",
    "scripting"
  ],

  "host_permissions": [
    "<all_urls>"
  ],

  "web_accessible_resources": [
    {
      "resources": ["images/*", "styles/*"],
      "matches": ["<all_urls>"]
    }
  ]
}
```

## Key Differences: MV3 vs MV2

| Feature | MV2 | MV3 |
|---------|-----|-----|
| Background | Persistent page | Service worker (ephemeral) |
| Remote code | Allowed | NOT allowed |
| Host permissions | In permissions | Separate host_permissions |
| Web request | blocking | declarativeNetRequest |

## permissions vs host_permissions

### permissions
API access, no host access needed:
```json
{
  "permissions": [
    "storage",       // chrome.storage
    "contextMenus",  // chrome.contextMenus
    "activeTab",     // Current tab only when user interacts
    "scripting",     // chrome.scripting
    "tabs",          // chrome.tabs (read tab info)
    "alarms",        // chrome.alarms
    "notifications"  // chrome.notifications
  ]
}
```

### host_permissions
Access to specific websites:
```json
{
  "host_permissions": [
    "<all_urls>",                    // All websites
    "https://*.google.com/*",        // Google domains
    "https://example.com/*",         // Specific site
    "*://example.com/*"              // HTTP and HTTPS
  ]
}
```

## Content Script run_at Options

```json
{
  "content_scripts": [{
    "run_at": "document_start",  // Before DOM
    "run_at": "document_end",    // DOM ready, before images
    "run_at": "document_idle"    // After page load (default)
  }]
}
```

## Match Patterns

```json
{
  "matches": [
    "<all_urls>",                    // All URLs
    "*://*.google.com/*",            // All Google
    "https://example.com/*",         // HTTPS only
    "http://localhost/*",            // Localhost
    "file:///*"                      // Local files (needs permission)
  ]
}
```

## Optional Permissions

Request at runtime instead of install:
```json
{
  "optional_permissions": ["tabs", "history"],
  "optional_host_permissions": ["https://optional.com/*"]
}
```

Request in code:
```javascript
chrome.permissions.request({
  permissions: ['tabs'],
  origins: ['https://optional.com/*']
}, (granted) => {
  if (granted) {
    // Permission granted
  }
});
```

## Service Worker Notes

Service workers in MV3:
- Ephemeral - sleep after ~30 seconds idle
- No DOM access
- No window object
- Cannot use localStorage (use chrome.storage)
- Wake on events (messages, alarms, etc.)

## No Remote Code

MV3 prohibits:
- eval()
- new Function()
- Loading external JS
- Inline event handlers in HTML

All code must be bundled with extension.

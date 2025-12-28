# Create New Chrome Extension

## Directory Structure
```
extension-name/
├── manifest.json
├── background.js          # Service worker (if needed)
├── content.js            # Content script (if needed)
├── popup/                # Popup UI (if needed)
│   ├── popup.html
│   ├── popup.css
│   └── popup.js
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

## Step 1: Create manifest.json

```json
{
  "manifest_version": 3,
  "name": "Extension Name",
  "version": "1.0.0",
  "description": "Brief description",
  "permissions": [],
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

## Step 2: Add Components As Needed

### For Background Service Worker
Add to manifest.json:
```json
{
  "background": {
    "service_worker": "background.js"
  }
}
```

Create background.js:
```javascript
// ABOUTME: Background service worker
// ABOUTME: Handles extension events and messaging

chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});
```

### For Content Script
Add to manifest.json:
```json
{
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"]
    }
  ]
}
```

Or for dynamic injection, add permissions:
```json
{
  "permissions": ["scripting", "activeTab"]
}
```

### For Storage
Add to manifest.json:
```json
{
  "permissions": ["storage"]
}
```

## Step 3: Create Popup (if needed)

popup/popup.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Extension</title>
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div class="container">
    <h1>Extension Name</h1>
  </div>
  <script src="popup.js"></script>
</body>
</html>
```

popup/popup.css:
```css
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  width: 350px;
  min-height: 400px;
  background: #fff;
}

.container {
  padding: 16px;
}
```

popup/popup.js:
```javascript
// ABOUTME: Popup script
// ABOUTME: Handles popup UI interactions

document.addEventListener('DOMContentLoaded', init);

async function init() {
  // Initialize popup
}
```

## Step 4: Load Extension in Chrome

1. Open `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select extension directory
5. Extension appears in toolbar

## Step 5: Reload After Changes

- Code changes: Click refresh icon on extension card
- manifest.json changes: Remove and re-load extension
- onInstalled changes: Remove and re-load extension

## Common Permission Combinations

### Read/modify current tab
```json
{
  "permissions": ["activeTab", "scripting"]
}
```

### Access all websites
```json
{
  "host_permissions": ["<all_urls>"]
}
```

### Store data
```json
{
  "permissions": ["storage"]
}
```

### Context menu
```json
{
  "permissions": ["contextMenus"]
}
```

### Tabs info
```json
{
  "permissions": ["tabs"]
}
```

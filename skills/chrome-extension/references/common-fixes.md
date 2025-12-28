# Common Fixes Reference

Known issues and their solutions.

## "Could not establish connection. Receiving end does not exist."

### Cause
Sending message to content script that isn't loaded.

### Fix
Use ensureContentScript pattern:

```javascript
async function ensureContentScript(tabId) {
  try {
    await chrome.tabs.sendMessage(tabId, { action: 'ping' });
    return true;
  } catch {
    try {
      await chrome.scripting.executeScript({
        target: { tabId },
        files: ['content.js']
      });
      await new Promise(r => setTimeout(r, 100));  // Wait 100ms!
      return true;
    } catch (e) {
      console.error('Cannot inject:', e);
      return false;
    }
  }
}
```

Content script must handle ping:
```javascript
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'ping') {
    sendResponse({ pong: true });
    return true;
  }
});
```

## Context Menu Not Appearing

### Cause
`chrome.runtime.onInstalled` only runs once when extension is installed.

### Fix
1. Go to `chrome://extensions/`
2. Click trash icon to remove extension
3. Click "Load unpacked" and re-add

Refreshing extension does NOT re-run onInstalled.

## Script Injection Timing Issue

### Cause
Message sent immediately after injection, before script initializes.

### Fix
Add 100ms delay after injection:

```javascript
await chrome.scripting.executeScript({
  target: { tabId },
  files: ['content.js']
});

// CRITICAL: Wait for script to initialize
await new Promise(resolve => setTimeout(resolve, 100));

// Now safe to send message
await chrome.tabs.sendMessage(tabId, { action: 'doSomething' });
```

## Quote Escaping in HTML Strings

### Problem
```javascript
// BREAKS - quotes conflict
const html = '<img onerror="this.style.display='none'">';
```

### Fix 1: Remove problematic attribute
```javascript
const html = '<img src="' + url + '">';
```

### Fix 2: Use template literals carefully
```javascript
const html = `<img onerror="this.style.display='none'">`;  // OK
```

### Fix 3: Set via JS
```javascript
img.onerror = function() { this.style.display = 'none'; };
```

## Service Worker "Inactive"

### Cause
MV3 service workers sleep after ~30 seconds of inactivity.

### Fix
Design for ephemeral execution:
- Don't store state in variables (use chrome.storage)
- Use chrome.alarms for periodic tasks
- Accept that service worker will restart

## "Extension context invalidated"

### Cause
Extension reloaded while content script was running on page.

### Fix
Reload the page after reloading extension.

## Async Response Not Received

### Cause
Message handler didn't return `true` for async response.

### Wrong
```javascript
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  doAsync().then(sendResponse);  // Missing return true!
});
```

### Fix
```javascript
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  doAsync().then(sendResponse);
  return true;  // Keep channel open for async response
});
```

## Cannot Inject into Page

### Restricted Pages
Cannot inject into:
- `chrome://` pages
- `chrome-extension://` pages
- Chrome Web Store (chrome.google.com/webstore)
- Other extension pages

### Check before injection
```javascript
function canInject(url) {
  if (!url) return false;
  if (url.startsWith('chrome://')) return false;
  if (url.startsWith('chrome-extension://')) return false;
  if (url.includes('chrome.google.com/webstore')) return false;
  return true;
}
```

## Permission Denied

### Check manifest.json
```json
{
  "permissions": ["scripting", "activeTab"],
  "host_permissions": ["<all_urls>"]
}
```

Need `scripting` for dynamic injection.
Need `host_permissions` for specific sites.

## Storage Not Persisting

### Check permission
```json
{
  "permissions": ["storage"]
}
```

### Check async handling
```javascript
// Wrong - not waiting
chrome.storage.sync.set({ key: 'value' });
const result = chrome.storage.sync.get(['key']);  // Undefined!

// Fix - await
await chrome.storage.sync.set({ key: 'value' });
const result = await chrome.storage.sync.get(['key']);
```

## Changes Not Applying

### Code changes (JS/CSS/HTML)
1. Click refresh icon on extension card at `chrome://extensions/`
2. Reload any tabs using the extension

### manifest.json changes
1. Refresh extension
2. Some changes need remove + reload

### onInstalled changes
1. MUST remove extension
2. Load unpacked again
3. Refresh alone won't re-run onInstalled

## Console Logs Not Appearing

### Background script logs
Open service worker devtools:
1. `chrome://extensions/`
2. Click "Service worker" link

### Content script logs
Open page devtools (F12), check Console.

### Popup logs
Right-click extension icon -> "Inspect popup"

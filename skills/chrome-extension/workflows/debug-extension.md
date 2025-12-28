# Debug Chrome Extension

Common debugging techniques and error fixes.

## Accessing DevTools

### Service Worker (Background)
1. Go to `chrome://extensions/`
2. Find your extension
3. Click "Service worker" link
4. DevTools opens for background script

### Popup
1. Right-click extension icon
2. Click "Inspect popup"
3. DevTools opens for popup

### Content Script
1. Open page where content script runs
2. Open DevTools (F12)
3. Content script logs appear in Console
4. Source files under Sources > Content scripts

## Common Errors and Fixes

### "Could not establish connection. Receiving end does not exist."

Cause: Content script not loaded when sending message.

Fix: Use ensureContentScript pattern:
```javascript
async function ensureContentScript(tabId) {
  try {
    await chrome.tabs.sendMessage(tabId, { action: 'ping' });
    return true;
  } catch {
    await chrome.scripting.executeScript({
      target: { tabId },
      files: ['content.js']
    });
    await new Promise(r => setTimeout(r, 100));
    return true;
  }
}
```

### Context Menu Not Appearing

Cause: onInstalled only runs once on install.

Fix:
1. Go to `chrome://extensions/`
2. Remove extension (trash icon)
3. Load unpacked again

### Service Worker Inactive

Cause: MV3 service workers sleep after ~30 seconds.

Fix: Design for ephemeral execution. Don't rely on persistent state.

### "Extension context invalidated"

Cause: Extension was reloaded while content script was running.

Fix: Reload the page after reloading extension.

### Permission Denied

Cause: Missing permissions in manifest.

Fix: Add required permissions:
```json
{
  "permissions": ["activeTab", "scripting"],
  "host_permissions": ["<all_urls>"]
}
```

### Script Not Injecting

Cause: Page loaded before extension, or restricted page.

Fix:
1. Refresh page after loading extension
2. Cannot inject into: chrome:// pages, Chrome Web Store, other extensions

## Debugging Techniques

### Console Logging
```javascript
console.log('Debug:', variable);
console.table(arrayData);
console.dir(object);
console.error('Error:', error);
```

### Check Extension Storage
In popup or background DevTools:
```javascript
chrome.storage.sync.get(null, (data) => console.log(data));
```

### Test Message Passing
In content script DevTools:
```javascript
chrome.runtime.sendMessage({ test: true }, (r) => console.log(r));
```

### Check Permissions
```javascript
chrome.permissions.getAll((permissions) => {
  console.log('Permissions:', permissions);
});
```

## When Changes Don't Apply

### Code Changes (JS/CSS/HTML)
1. Go to `chrome://extensions/`
2. Click refresh icon on extension card
3. Reload any open pages

### manifest.json Changes
1. Must refresh extension (click refresh icon)
2. Some changes require remove + load unpacked

### onInstalled Handler Changes
1. MUST remove extension completely
2. Load unpacked again
3. Just refreshing won't re-run onInstalled

## Restricted Pages

Cannot inject content scripts into:
- `chrome://` pages
- `chrome-extension://` pages
- Chrome Web Store
- Other extension pages
- `file://` (unless permission granted)

## Check If Page Allows Injection

```javascript
async function canInject(tabId) {
  try {
    await chrome.scripting.executeScript({
      target: { tabId },
      func: () => true
    });
    return true;
  } catch {
    return false;
  }
}
```

## Debugging Message Flow

### Background Script
```javascript
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  console.log('BG received:', msg, 'from:', sender);
  // ...
});
```

### Content Script
```javascript
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  console.log('CS received:', msg);
  // ...
});
```

## Quick Checklist

1. Is extension loaded? Check `chrome://extensions/`
2. Are there errors? Check service worker console
3. Is content script loaded? Check page console for your logs
4. Did you reload after changes?
5. Is page restricted? (chrome://, Web Store, etc.)
6. Are permissions correct in manifest?
7. Did you modify onInstalled? Remove and reload extension

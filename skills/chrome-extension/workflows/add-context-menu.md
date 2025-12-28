# Add Context Menu

Right-click context menu for Chrome extensions.

## Required Permissions

manifest.json:
```json
{
  "permissions": ["contextMenus", "scripting", "activeTab"],
  "host_permissions": ["<all_urls>"],
  "background": {
    "service_worker": "background.js"
  }
}
```

## Create Context Menu

In background.js, create menu in onInstalled:

```javascript
// ABOUTME: Background service worker with context menu
// ABOUTME: Handles right-click menu and content script injection

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'my-action',
    title: 'Do Something',
    contexts: ['selection', 'page']  // or just ['selection'] for text
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === 'my-action') {
    await handleAction(info, tab);
  }
});
```

## The ensureContentScript Pattern

CRITICAL: Content scripts may not be loaded. Always ensure injection before sending messages.

```javascript
async function ensureContentScript(tabId) {
  try {
    // Ping content script to check if loaded
    await chrome.tabs.sendMessage(tabId, { action: 'ping' });
    return true;
  } catch (error) {
    // Not loaded - inject it
    try {
      await chrome.scripting.executeScript({
        target: { tabId },
        files: ['content.js']
      });
      // CRITICAL: Wait for script to initialize
      await new Promise(resolve => setTimeout(resolve, 100));
      return true;
    } catch (injectError) {
      console.error('Cannot inject:', injectError);
      return false;
    }
  }
}
```

## Handle Context Menu Click

```javascript
async function handleAction(info, tab) {
  // Ensure content script is ready
  const ready = await ensureContentScript(tab.id);
  if (!ready) {
    console.error('Cannot inject content script');
    return;
  }

  // Now safe to send message
  try {
    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'doSomething',
      selectedText: info.selectionText,
      pageUrl: info.pageUrl
    });
    console.log('Response:', response);
  } catch (error) {
    console.error('Message failed:', error);
  }
}
```

## Content Script Handler

content.js must handle ping and actual actions:

```javascript
// ABOUTME: Content script for page interaction
// ABOUTME: Handles messages from background

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  // Ping handler - proves script is loaded
  if (request.action === 'ping') {
    sendResponse({ status: 'ok' });
    return true;
  }

  if (request.action === 'doSomething') {
    // Handle the action
    const result = doSomething(request.selectedText);
    sendResponse({ success: true, result });
    return true;  // Keep channel open for async
  }
});

function doSomething(text) {
  // Your logic here
  return text;
}
```

## Multiple Menu Items

```javascript
chrome.runtime.onInstalled.addListener(() => {
  // Parent menu
  chrome.contextMenus.create({
    id: 'parent',
    title: 'My Extension',
    contexts: ['selection']
  });

  // Child items
  chrome.contextMenus.create({
    id: 'action-1',
    parentId: 'parent',
    title: 'Action 1',
    contexts: ['selection']
  });

  chrome.contextMenus.create({
    id: 'action-2',
    parentId: 'parent',
    title: 'Action 2',
    contexts: ['selection']
  });
});
```

## Context Types

- `page` - Page background
- `selection` - Selected text
- `link` - Right-click on link
- `image` - Right-click on image
- `video` - Right-click on video
- `audio` - Right-click on audio
- `frame` - Iframe
- `editable` - Input fields

## IMPORTANT: After Modifying onInstalled

Changes to `chrome.runtime.onInstalled` require:
1. Go to `chrome://extensions/`
2. Remove extension completely
3. Load unpacked again

Just refreshing won't run onInstalled again.

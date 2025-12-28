# Message Passing Reference

Communication between background, content scripts, and popup.

## Background -> Content Script

```javascript
// background.js
async function sendToContent(tabId, message) {
  try {
    const response = await chrome.tabs.sendMessage(tabId, message);
    return response;
  } catch (error) {
    console.error('Send failed:', error);
    return null;
  }
}

// Usage
const response = await sendToContent(tab.id, {
  action: 'highlight',
  text: 'example'
});
```

## Content Script -> Background

```javascript
// content.js
async function sendToBackground(message) {
  try {
    const response = await chrome.runtime.sendMessage(message);
    return response;
  } catch (error) {
    console.error('Send failed:', error);
    return null;
  }
}

// Usage
const response = await sendToBackground({
  action: 'saveData',
  data: { key: 'value' }
});
```

## Receiving Messages

### In Background
```javascript
// background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('From:', sender.tab?.url);

  if (message.action === 'getData') {
    // Sync response
    sendResponse({ data: 'value' });
  }

  if (message.action === 'asyncAction') {
    // Async response - MUST return true
    handleAsync(message).then(sendResponse);
    return true;  // Keep channel open
  }
});

async function handleAsync(message) {
  const result = await someAsyncOperation();
  return { success: true, result };
}
```

### In Content Script
```javascript
// content.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'ping') {
    sendResponse({ status: 'ok' });
    return true;
  }

  if (message.action === 'highlight') {
    highlightText(message.text);
    sendResponse({ done: true });
    return true;
  }
});
```

## Ping/Pong Pattern

Check if content script is loaded before sending:

```javascript
// background.js
async function isContentScriptReady(tabId) {
  try {
    await chrome.tabs.sendMessage(tabId, { action: 'ping' });
    return true;
  } catch {
    return false;
  }
}

// content.js
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'ping') {
    sendResponse({ pong: true });
    return true;
  }
  // ... other handlers
});
```

## Full ensureContentScript Pattern

```javascript
// background.js
async function ensureContentScript(tabId) {
  // Check if already loaded
  try {
    await chrome.tabs.sendMessage(tabId, { action: 'ping' });
    return true;
  } catch {
    // Not loaded - inject
  }

  try {
    await chrome.scripting.executeScript({
      target: { tabId },
      files: ['content.js']
    });
    // CRITICAL: Wait for initialization
    await new Promise(resolve => setTimeout(resolve, 100));
    return true;
  } catch (error) {
    console.error('Inject failed:', error);
    return false;
  }
}

// Usage
async function sendMessageSafely(tabId, message) {
  const ready = await ensureContentScript(tabId);
  if (!ready) return null;

  return await chrome.tabs.sendMessage(tabId, message);
}
```

## Popup <-> Background

```javascript
// popup.js - send to background
const response = await chrome.runtime.sendMessage({
  action: 'getData'
});

// background.js - receives via onMessage listener
// (same as content script -> background)
```

## Broadcast to All Tabs

```javascript
// background.js
async function broadcastToAllTabs(message) {
  const tabs = await chrome.tabs.query({});
  for (const tab of tabs) {
    try {
      await chrome.tabs.sendMessage(tab.id, message);
    } catch {
      // Tab may not have content script
    }
  }
}
```

## Message Structure Convention

```javascript
// Good: action-based messages
{ action: 'saveData', payload: { key: 'value' } }
{ action: 'highlight', text: 'example' }
{ action: 'ping' }

// Response structure
{ success: true, data: result }
{ success: false, error: 'Error message' }
```

## Important: Return true for Async

If using async/await in message handler:
```javascript
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'async') {
    doAsyncWork().then(sendResponse);
    return true;  // REQUIRED for async response
  }
});
```

Without `return true`, channel closes before async response sends.

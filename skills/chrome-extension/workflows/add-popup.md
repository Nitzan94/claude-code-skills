# Add Popup UI

Extension popup appears when clicking toolbar icon.

## manifest.json

```json
{
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  }
}
```

## Basic Structure

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
  <header class="header">
    <h1>Extension Name</h1>
  </header>

  <main class="main">
    <!-- Content here -->
  </main>

  <footer class="footer">
    <!-- Footer content -->
  </footer>

  <script src="popup.js"></script>
</body>
</html>
```

## CSS with Dark Mode Support

popup/popup.css:
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #1a1a1a;
  --text-secondary: #666666;
  --accent: #4f46e5;
  --border: #e5e5e5;
  --radius: 8px;
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2a2a2a;
    --text-primary: #ffffff;
    --text-secondary: #a0a0a0;
    --border: #3a3a3a;
    --shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
  color: var(--text-primary);
  background: var(--bg-primary);
  width: 350px;
  min-height: 400px;
}

.header {
  padding: 16px;
  border-bottom: 1px solid var(--border);
}

.main {
  padding: 16px;
}

.footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--text-secondary);
}
```

## RTL (Hebrew/Arabic) Support

For RTL languages, update HTML:
```html
<html lang="he" dir="rtl">
```

Add RTL CSS:
```css
body {
  direction: rtl;
  text-align: right;
}

/* RTL-specific adjustments */
[dir="rtl"] .icon { margin-left: 8px; margin-right: 0; }
```

## Glass-morphism Effect

```css
.card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

@media (prefers-color-scheme: dark) {
  .card {
    background: rgba(30, 30, 50, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}
```

## Animations

```css
/* Slide in animation */
@keyframes slideIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.item {
  animation: slideIn 0.3s ease forwards;
  opacity: 0;
}

/* Staggered animation */
.item:nth-child(1) { animation-delay: 0.05s; }
.item:nth-child(2) { animation-delay: 0.1s; }
.item:nth-child(3) { animation-delay: 0.15s; }

/* Button hover */
.btn {
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

## JavaScript Pattern

popup/popup.js:
```javascript
// ABOUTME: Popup script
// ABOUTME: Handles popup UI and storage

document.addEventListener('DOMContentLoaded', init);

async function init() {
  await loadData();
  setupEventListeners();
}

async function loadData() {
  try {
    const result = await chrome.storage.sync.get(['data']);
    const data = result.data || [];
    renderData(data);
  } catch (error) {
    console.error('Failed to load:', error);
  }
}

async function saveData(data) {
  try {
    await chrome.storage.sync.set({ data });
  } catch (error) {
    console.error('Failed to save:', error);
  }
}

function renderData(data) {
  const container = document.getElementById('container');
  container.innerHTML = data.map(item =>
    `<div class="item">${escapeHtml(item.name)}</div>`
  ).join('');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function setupEventListeners() {
  document.getElementById('saveBtn').addEventListener('click', handleSave);
}

async function handleSave() {
  // Handle save logic
}
```

## Buttons

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  border: none;
  border-radius: var(--radius);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--accent);
  color: white;
}

.btn-primary:hover {
  filter: brightness(1.1);
}
```

## Input Fields

```css
.input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 14px;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: border-color 0.2s;
}

.input:focus {
  outline: none;
  border-color: var(--accent);
}

.input::placeholder {
  color: var(--text-secondary);
}
```

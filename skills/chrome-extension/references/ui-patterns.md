# UI Patterns Reference

Popup UI patterns: theming, RTL, animations.

## CSS Variables for Theming

```css
:root {
  /* Colors */
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --bg-tertiary: #fafafa;
  --text-primary: #1a1a1a;
  --text-secondary: #666666;
  --accent: #4f46e5;
  --accent-hover: #4338ca;
  --border: #e5e5e5;
  --success: #22c55e;
  --error: #ef4444;

  /* Spacing & Sizing */
  --radius: 8px;
  --radius-lg: 12px;
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);
}
```

## Dark Mode Support

### Using prefers-color-scheme
```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2a2a2a;
    --bg-tertiary: #333333;
    --text-primary: #ffffff;
    --text-secondary: #a0a0a0;
    --border: #3a3a3a;
    --shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }
}
```

### Manual Theme Toggle
```css
[data-theme="dark"] {
  --bg-primary: #1a1a1a;
  --bg-secondary: #2a2a2a;
  --text-primary: #ffffff;
  /* ... */
}

/* Respect system unless manually set */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg-primary: #1a1a1a;
    /* ... dark variables */
  }
}
```

```javascript
// Toggle theme
function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  chrome.storage.sync.set({ theme });
}
```

## RTL Support (Hebrew/Arabic)

### HTML Setup
```html
<html lang="he" dir="rtl">
```

### CSS Adjustments
```css
body {
  direction: rtl;
  text-align: right;
}

/* Flip specific elements */
[dir="rtl"] .icon-left { margin-right: 0; margin-left: 8px; }
[dir="rtl"] .arrow { transform: scaleX(-1); }
```

### Auto-detect Language
```javascript
function detectLanguage() {
  const lang = navigator.language;
  if (lang.startsWith('he') || lang.startsWith('ar')) {
    document.documentElement.setAttribute('dir', 'rtl');
    document.documentElement.setAttribute('lang', lang.slice(0, 2));
  }
}
```

## Glass-morphism Effect

```css
.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
}

@media (prefers-color-scheme: dark) {
  .glass-card {
    background: rgba(30, 30, 50, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}
```

## Gradient Backgrounds

```css
/* Warm gradient */
.gradient-warm {
  background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FFE66D 100%);
}

/* Cool gradient */
.gradient-cool {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Animated shimmer */
.header::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0%, 100% { transform: translateX(0) translateY(0); }
  50% { transform: translateX(-20px) translateY(10px); }
}
```

## Animations

### Slide In
```css
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.item {
  animation: slideIn 0.3s ease forwards;
  opacity: 0;
}
```

### Staggered Animation
```css
.item { animation: slideIn 0.3s ease forwards; opacity: 0; }
.item:nth-child(1) { animation-delay: 0.05s; }
.item:nth-child(2) { animation-delay: 0.10s; }
.item:nth-child(3) { animation-delay: 0.15s; }
.item:nth-child(4) { animation-delay: 0.20s; }
.item:nth-child(5) { animation-delay: 0.25s; }
```

### Button Hover
```css
.btn {
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn:active {
  transform: translateY(0);
}
```

### Success Pulse
```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.btn.success {
  animation: pulse 0.5s ease;
}
```

### Expand/Collapse
```css
.expand-icon {
  transition: transform 0.2s ease;
}

.item.expanded .expand-icon {
  transform: rotate(180deg);
}

.content {
  display: none;
}

.item.expanded .content {
  display: block;
}
```

## Common Components

### Button
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
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

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
}
```

### Input
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
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}
```

### Card
```css
.card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 16px;
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-lg);
  border-color: var(--accent);
}
```

## Popup Sizing

```css
body {
  width: 350px;      /* Fixed width */
  min-height: 400px; /* Minimum height */
  max-height: 600px; /* Maximum height */
  overflow-y: auto;
}
```

# Storage Patterns Reference

chrome.storage API for extension data persistence.

## Permission Required

```json
{
  "permissions": ["storage"]
}
```

## sync vs local

### chrome.storage.sync
- Syncs across user's Chrome browsers
- 100KB total limit
- 8KB per item limit
- Good for: settings, small data

### chrome.storage.local
- Local only, no sync
- 10MB limit (5MB default, can request more)
- Good for: large data, cached content

## Basic Operations

### Save Data
```javascript
// Single value
await chrome.storage.sync.set({ key: 'value' });

// Multiple values
await chrome.storage.sync.set({
  setting1: true,
  setting2: 'option',
  data: { nested: 'object' }
});
```

### Load Data
```javascript
// Single key
const result = await chrome.storage.sync.get(['key']);
const value = result.key;  // undefined if not set

// Multiple keys
const result = await chrome.storage.sync.get(['key1', 'key2']);

// All data
const allData = await chrome.storage.sync.get(null);

// With defaults
const result = await chrome.storage.sync.get({
  key1: 'default1',
  key2: 'default2'
});
```

### Remove Data
```javascript
// Single key
await chrome.storage.sync.remove('key');

// Multiple keys
await chrome.storage.sync.remove(['key1', 'key2']);

// Clear all
await chrome.storage.sync.clear();
```

## Common Patterns

### Load with Defaults
```javascript
const DEFAULTS = {
  enabled: true,
  theme: 'light',
  count: 0
};

async function loadSettings() {
  const result = await chrome.storage.sync.get(DEFAULTS);
  return result;
}

// result always has all keys with defaults if not set
```

### Array Storage
```javascript
// Load array
async function loadItems() {
  const result = await chrome.storage.sync.get({ items: [] });
  return result.items;
}

// Add item
async function addItem(item) {
  const items = await loadItems();
  items.push(item);
  await chrome.storage.sync.set({ items });
}

// Remove item
async function removeItem(id) {
  const items = await loadItems();
  const filtered = items.filter(item => item.id !== id);
  await chrome.storage.sync.set({ items: filtered });
}

// Update item
async function updateItem(id, updates) {
  const items = await loadItems();
  const index = items.findIndex(item => item.id === id);
  if (index !== -1) {
    items[index] = { ...items[index], ...updates };
    await chrome.storage.sync.set({ items });
  }
}
```

### Listen for Changes
```javascript
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName !== 'sync') return;

  for (const [key, { oldValue, newValue }] of Object.entries(changes)) {
    console.log(`${key}: ${oldValue} -> ${newValue}`);
  }
});
```

### Settings Manager Class
```javascript
class Settings {
  static DEFAULTS = {
    enabled: true,
    theme: 'auto',
    language: 'en'
  };

  static async get(key) {
    const result = await chrome.storage.sync.get({ [key]: this.DEFAULTS[key] });
    return result[key];
  }

  static async set(key, value) {
    await chrome.storage.sync.set({ [key]: value });
  }

  static async getAll() {
    return await chrome.storage.sync.get(this.DEFAULTS);
  }

  static async reset() {
    await chrome.storage.sync.set(this.DEFAULTS);
  }
}

// Usage
const theme = await Settings.get('theme');
await Settings.set('theme', 'dark');
```

## Error Handling

```javascript
async function safeGet(keys) {
  try {
    return await chrome.storage.sync.get(keys);
  } catch (error) {
    console.error('Storage get failed:', error);
    return typeof keys === 'object' ? keys : {};  // Return defaults
  }
}

async function safeSet(data) {
  try {
    await chrome.storage.sync.set(data);
    return true;
  } catch (error) {
    console.error('Storage set failed:', error);
    return false;
  }
}
```

## Storage Limits

### sync limits
- QUOTA_BYTES: 102,400 (100KB total)
- QUOTA_BYTES_PER_ITEM: 8,192 (8KB per item)
- MAX_ITEMS: 512
- MAX_WRITE_OPERATIONS_PER_HOUR: 1,800
- MAX_WRITE_OPERATIONS_PER_MINUTE: 120

### Check usage
```javascript
chrome.storage.sync.getBytesInUse(null, (bytes) => {
  console.log(`Using ${bytes} of 102400 bytes`);
});
```

## Using local for Large Data

```javascript
// For data > 8KB per item or > 100KB total
async function saveLargeData(data) {
  await chrome.storage.local.set({ largeData: data });
}

async function loadLargeData() {
  const result = await chrome.storage.local.get({ largeData: null });
  return result.largeData;
}
```

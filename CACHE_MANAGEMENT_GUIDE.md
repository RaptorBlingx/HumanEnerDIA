# 🔄 Cache Management Guide - Root Solution

**Created:** January 2, 2026  
**Purpose:** Permanent solution to browser caching issues  
**Status:** ✅ IMPLEMENTED

---

## 🎯 Root Problem

**Issue:** Browser caches JavaScript files aggressively, causing users to see old versions even after updates.

**Symptom:** "Pilot Factory Call" link disappeared after deployment because browsers served cached `sidebar.js` without the new link.

**Root Cause:** Inconsistent version parameters across HTML files allowed browsers to cache old versions.

---

## ✅ Permanent Solution Implemented

### 1. **Version-Based Cache Busting**

**Strategy:** Every JavaScript file includes a version query parameter that changes on every update.

**Format:** `sidebar.js?v=YYYYMMDDHHMMSS` (timestamp-based)

**Example:**
```html
<!-- OLD (causes caching issues) -->
<script src="/js/sidebar.js"></script>

<!-- NEW (forces refresh on version change) -->
<script src="/js/sidebar.js?v=20260102115822"></script>
```

**Why This Works:**
- Browser treats `sidebar.js?v=20260102115822` as a DIFFERENT file than `sidebar.js?v=20260102`
- Forces immediate download of new version
- Works across ALL browsers (Chrome, Firefox, Safari, Edge)
- No manual cache clearing needed

---

## 📋 Standard Operating Procedure

### When You Update sidebar.js or Any JS File:

**Step 1: Generate New Version**
```bash
NEW_VERSION=$(date +%Y%m%d%H%M%S)
echo $NEW_VERSION
```

**Step 2: Update ALL HTML Files**
```bash
# Find all files with old version
grep -r "sidebar.js?v=" portal/public/*.html

# Update all files at once (automated)
find portal/public -name "*.html" -type f -exec \
  sed -i "s/sidebar\.js?v=[0-9]*/sidebar.js?v=${NEW_VERSION}/g" {} \;

# Verify changes
grep -r "sidebar.js?v=" portal/public/*.html | wc -l
```

**Step 3: Restart Nginx**
```bash
docker compose restart nginx
```

**Step 4: Verify Deployment**
```bash
curl -s https://wasabi.intel50001.com/index.html | grep "sidebar.js?v="
```

---

## 🗂️ Files That Include sidebar.js (ALL must be updated)

| File | Current Version | Last Updated |
|------|----------------|--------------|
| **Public Pages** | | |
| `portal/public/index.html` | v=20260102115822 | Jan 2, 2026 |
| `portal/public/about.html` | v=20260102115822 | Jan 2, 2026 |
| `portal/public/iso50001.html` | v=20260102115822 | Jan 2, 2026 |
| `portal/public/contact.html` | v=20260102115822 | Jan 2, 2026 |
| `portal/public/auth.html` | v=20260102115822 | Jan 2, 2026 |
| **Pilot Factory Pages** | | |
| `portal/public/pilot-factory-call.html` | v=20260102115822 | Jan 2, 2026 |
| `portal/public/pilot-factory-application.html` | v=20260102115822 | Jan 2, 2026 |
| `portal/public/pilot-factory-thank-you.html` | v=20260102115822 | Jan 2, 2026 |
| **Admin Pages** | | |
| `portal/public/admin/pilot-applications.html` | v=20260102115822 | Jan 2, 2026 |
| `portal/public/admin/pilot-application-detail.html` | v=20260102115822 | Jan 2, 2026 |

**Total:** 10 files

---

## 🚨 Common Mistakes to Avoid

### ❌ DON'T: Update Only Some Files
```bash
# This leaves inconsistent versions
sed -i 's/sidebar.js?v=.*/sidebar.js?v=20260102/g' index.html
# Other files still have old version!
```

### ✅ DO: Update All Files at Once
```bash
# Update ALL HTML files in one command
find portal/public -name "*.html" -exec \
  sed -i 's/sidebar.js?v=[^"]*"/sidebar.js?v=20260102115822"/g' {} \;
```

### ❌ DON'T: Use Same Version for Different Updates
```bash
# Reusing version won't bust cache
sidebar.js?v=1
sidebar.js?v=1  # Browser uses cached version!
```

### ✅ DO: Generate Unique Version Every Time
```bash
# Always generate new timestamp
sidebar.js?v=20260102120000
sidebar.js?v=20260102121500  # Different version = forced refresh
```

### ❌ DON'T: Forget to Restart Nginx
```bash
# Files updated but nginx serves cached version
vim index.html
# Missing: docker compose restart nginx
```

### ✅ DO: Always Restart Nginx After Updates
```bash
vim index.html
docker compose restart nginx  # Clear server cache
```

---

## 🛠️ Automated Update Script

**Create:** `scripts/update-sidebar-version.sh`

```bash
#!/bin/bash
# Update sidebar.js version across all HTML files

set -e  # Exit on error

# Generate new version (timestamp)
NEW_VERSION=$(date +%Y%m%d%H%M%S)

echo "🔄 Updating sidebar.js version to: v=${NEW_VERSION}"

# Find all HTML files
HTML_FILES=$(find portal/public -name "*.html" -type f)
COUNT=$(echo "$HTML_FILES" | wc -l)

echo "📁 Found ${COUNT} HTML files to update"

# Update all files
for FILE in $HTML_FILES; do
    if grep -q "sidebar.js?v=" "$FILE"; then
        sed -i "s/sidebar\.js?v=[^\"']*/sidebar.js?v=${NEW_VERSION}/g" "$FILE"
        echo "   ✅ Updated: $FILE"
    fi
done

# Restart nginx
echo "🔄 Restarting nginx..."
docker compose restart nginx

# Verify
sleep 2
DEPLOYED=$(curl -s https://wasabi.intel50001.com/index.html | grep -o "sidebar.js?v=[0-9]*" | head -1)
echo "✅ Deployed version: ${DEPLOYED}"

echo "🎉 Update complete! New version: v=${NEW_VERSION}"
```

**Make Executable:**
```bash
chmod +x scripts/update-sidebar-version.sh
```

**Usage:**
```bash
# After editing sidebar.js
./scripts/update-sidebar-version.sh
```

---

## 🌐 Nginx Cache Configuration

**Current Settings:** `nginx/conf.d/default.conf`

```nginx
# JavaScript files - SHORT cache, must-revalidate
location /js/ {
    alias /usr/share/nginx/html/portal/js/;
    expires 1h;  # Cache for 1 hour only
    add_header Cache-Control "public, must-revalidate";
    add_header Access-Control-Allow-Origin * always;
}
```

**Why These Settings:**
- **expires 1h**: Browser can cache for 1 hour max
- **must-revalidate**: Browser MUST check with server after expiry
- **NOT immutable**: Allows version parameter to force refresh

**Alternative for Production:**
```nginx
# Option 1: Shorter cache (15 minutes)
expires 15m;

# Option 2: No cache (always fresh, but slower)
expires -1;
add_header Cache-Control "no-cache, no-store, must-revalidate";
```

---

## 🧪 Testing Cache Busting

### Test 1: Version Parameter Works
```bash
# Check current version
curl -I https://wasabi.intel50001.com/js/sidebar.js?v=20260102115822

# Should return: 200 OK
# Should include: Cache-Control: public, must-revalidate
```

### Test 2: Different Version Fetches New File
```bash
# Fetch with old version
curl -s https://wasabi.intel50001.com/js/sidebar.js?v=OLD_VERSION > /tmp/old.js

# Fetch with new version
curl -s https://wasabi.intel50001.com/js/sidebar.js?v=NEW_VERSION > /tmp/new.js

# Compare
diff /tmp/old.js /tmp/new.js
# Should show differences if sidebar.js changed
```

### Test 3: Browser DevTools Check
1. Open https://wasabi.intel50001.com in Chrome
2. Press F12 → Network tab
3. Refresh page (Ctrl+F5)
4. Find `sidebar.js?v=20260102115822` request
5. Check status: Should be `200` (not `304 Not Modified`)
6. Check size: Should show actual file size (not "disk cache")

---

## 📊 Cache Hit/Miss Monitoring

**Optional:** Add logging to track cache effectiveness

**In nginx.conf:**
```nginx
log_format cache_status '$remote_addr - $upstream_cache_status [$time_local] '
                       '"$request" $status $body_bytes_sent '
                       '"$http_referer" "$http_user_agent"';

access_log /var/log/nginx/cache.log cache_status;
```

**Monitor:**
```bash
docker compose exec nginx tail -f /var/log/nginx/cache.log | grep sidebar.js
```

**Interpret:**
- `MISS`: Cache miss, fetched from origin (good after version change)
- `HIT`: Cache hit, served from cache (good for unchanged files)
- `STALE`: Cached version expired, revalidating
- `BYPASS`: Cache bypassed (version parameter forces this)

---

## 🔮 Future Improvements

### Option 1: Webpack/Vite Build Process
**Status:** Not implemented (would require frontend build pipeline)

**How it works:**
```javascript
// sidebar.js becomes sidebar.a3f2e1b.js (hash-based filename)
<script src="/js/sidebar.a3f2e1b.js"></script>
```

**Benefits:**
- ✅ Automatic cache busting (hash changes when file changes)
- ✅ No manual version updates needed
- ✅ Optimal caching (long expiry for hashed files)

**Trade-offs:**
- ⚠️ Requires build step in deployment
- ⚠️ More complex development workflow
- ⚠️ Need to update HTML references dynamically

### Option 2: Service Worker
**Status:** Not needed for current scale

**How it works:**
```javascript
// Service worker intercepts requests and manages cache
self.addEventListener('fetch', (event) => {
  // Custom cache logic
});
```

**Benefits:**
- ✅ Full control over caching strategy
- ✅ Offline functionality
- ✅ Background updates

**Trade-offs:**
- ⚠️ Complex implementation
- ⚠️ Browser support required
- ⚠️ Debugging can be challenging

### Option 3: CDN with Purge API
**Status:** Not using CDN currently

**How it works:**
```bash
# Purge cache via API after deployment
curl -X PURGE https://cdn.wasabi.intel50001.com/js/sidebar.js
```

**Benefits:**
- ✅ Instant cache invalidation
- ✅ No version parameters needed
- ✅ Global distribution

**Trade-offs:**
- ⚠️ Requires CDN subscription
- ⚠️ Additional costs
- ⚠️ More infrastructure complexity

---

## 📚 Additional Resources

- **MDN Cache-Control:** https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
- **Nginx Caching Guide:** https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache
- **Google Web Fundamentals - HTTP Caching:** https://web.dev/http-cache/

---

## ✅ Checklist: Deploying JS Changes

- [ ] Edit JavaScript file (e.g., `portal/public/js/sidebar.js`)
- [ ] Generate new version: `NEW_VERSION=$(date +%Y%m%d%H%M%S)`
- [ ] Update ALL HTML files: `find portal/public -name "*.html" -exec sed -i "s/sidebar.js?v=[^\"']*/sidebar.js?v=${NEW_VERSION}/g" {} \;`
- [ ] Verify count: `grep -r "sidebar.js?v=" portal/public/*.html | wc -l` (should be 10)
- [ ] Restart nginx: `docker compose restart nginx`
- [ ] Wait 3 seconds: `sleep 3`
- [ ] Verify deployment: `curl -s https://wasabi.intel50001.com/index.html | grep "sidebar.js?v="`
- [ ] Test in browser: Open https://wasabi.intel50001.com and check sidebar
- [ ] Document version in git commit: `git commit -m "feat: update sidebar.js (v=${NEW_VERSION})"`

---

**Status:** ✅ Root solution implemented  
**Last Updated:** January 2, 2026  
**Current Version:** v=20260102115822

---

_This guide serves as the permanent solution to cache-related issues. Follow the SOP for ALL JavaScript updates._

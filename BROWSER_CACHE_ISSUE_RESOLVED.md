# Browser Caching Issue - Resolution

**Issue Date:** January 2, 2026  
**Problem:** Pilot Factory Call link not visible in sidebar on https://wasabi.intel50001.com even with hard refresh  
**Root Cause:** Aggressive browser caching due to nginx configuration  
**Status:** ✅ RESOLVED

---

## Problem Description

### Symptoms
- Link visible on http://10.33.10.104:8080 but NOT on https://wasabi.intel50001.com
- Hard refresh (Ctrl+F5) did not clear cache in Chrome
- "Empty cache and Hard Refresh" did not work
- Incognito mode showed old version
- Edge InPrivate eventually showed correct version

### Root Cause
Nginx was configured with aggressive caching headers:
```nginx
location /js/ {
    expires 7d;
    add_header Cache-Control "public, immutable";
}
```

**"immutable"** tells the browser: "This file will NEVER change, cache it forever!"

---

## Solution Implemented

### 1. Updated Nginx Configuration
**File:** `nginx/conf.d/default.conf`

**Changed:**
```nginx
# OLD (7 days, immutable - too aggressive)
location /js/ {
    expires 7d;
    add_header Cache-Control "public, immutable";
}

# NEW (1 hour, must-revalidate - proper for dynamic content)
location /js/ {
    expires 1h;
    add_header Cache-Control "public, must-revalidate";
}
```

**Explanation:**
- **expires 1h:** Browser can cache for 1 hour
- **must-revalidate:** Browser MUST check with server after expiry
- Removed **immutable:** Allows browser to check for updates

### 2. Added Version Parameters (Cache-Busting)
**Files Updated:**
- `portal/public/pilot-factory-call.html`
- `portal/public/pilot-factory-application.html`
- `portal/public/pilot-factory-thank-you.html`
- `portal/public/admin/pilot-applications.html`
- `portal/public/admin/pilot-application-detail.html`

**Changed:**
```html
<!-- OLD -->
<script src="/js/sidebar.js"></script>

<!-- NEW -->
<script src="/js/sidebar.js?v=20260102"></script>
```

**Why This Works:**
- Browser sees `?v=20260102` as a DIFFERENT URL
- Immediately fetches new version
- Update version number when making changes: `?v=20260103`, `?v=20260104`, etc.

---

## Cache Control Headers Explained

### Different Cache Policies

| Header | Meaning | Use Case |
|--------|---------|----------|
| `public, immutable` | Never changes, cache forever | Versioned assets (app.v1.2.3.js) |
| `public, must-revalidate` | Can cache but must check if expired | JS/CSS that may update |
| `no-cache` | Always validate with server | Dynamic HTML pages |
| `no-store` | Never cache | Sensitive data |

### Our Configuration

| Asset Type | Expires | Cache-Control | Rationale |
|------------|---------|---------------|-----------|
| **JavaScript** | 1 hour | must-revalidate | Frequently updated |
| **CSS** | 1 hour | must-revalidate | Frequently updated |
| **Images** | 7 days | must-revalidate | Rarely change |
| **HTML** | (default) | (default) | Always fresh |

---

## Testing the Fix

### Before Fix
```bash
# Check cache headers (OLD)
curl -I https://wasabi.intel50001.com/js/sidebar.js

# Output:
Cache-Control: public, immutable
Expires: Fri, 09 Jan 2026 10:00:00 GMT  # 7 days!
```

### After Fix
```bash
# Check cache headers (NEW)
curl -I https://wasabi.intel50001.com/js/sidebar.js

# Expected Output:
Cache-Control: public, must-revalidate
Expires: Thu, 02 Jan 2026 11:00:00 GMT  # 1 hour
```

### User Testing
1. **Clear Browser Cache:**
   - Chrome: Settings → Privacy → Clear browsing data → Cached images and files
   - Edge: Settings → Privacy → Choose what to clear → Cached data
   - Firefox: Options → Privacy → Clear Data → Cached Web Content

2. **Or Use Version URL:**
   - https://wasabi.intel50001.com/pilot-factory-call.html?v=1
   - The `?v=1` bypasses cache for HTML page

3. **Verify Sidebar:**
   - Open sidebar
   - Should see "Pilot Factory Call" link under Information section
   - Link should point to `/pilot-factory-call.html`

---

## Future Prevention

### For Developers

#### When Updating JavaScript/CSS Files:
1. **Increment version number** in HTML files:
   ```html
   <!-- Change from v=20260102 to v=20260103 -->
   <script src="/js/sidebar.js?v=20260103"></script>
   ```

2. **Or use timestamp:**
   ```bash
   # Get current timestamp
   date +%Y%m%d%H%M
   
   # Use in HTML
   <script src="/js/sidebar.js?v=202601021530"></script>
   ```

#### When Deploying Updates:
```bash
# 1. Update version numbers in HTML files
find portal/public -name "*.html" -exec sed -i 's/?v=[0-9]*/?v=20260103/g' {} \;

# 2. Restart nginx
docker compose restart nginx

# 3. Verify
curl -I http://localhost:8080/js/sidebar.js | grep Cache-Control
```

### For End Users

**If you don't see latest changes:**

**Quick Fix (No Tech Knowledge Required):**
1. Press `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac)
2. If that doesn't work, clear browser cache once

**Technical Users:**
1. Open Developer Tools (F12)
2. Right-click refresh button → "Empty Cache and Hard Reload"
3. Or disable cache while DevTools is open

---

## Production Recommendations

### 1. Automate Version Numbers
Create a script to automatically increment versions:

```bash
#!/bin/bash
# File: scripts/update-cache-version.sh

VERSION=$(date +%Y%m%d%H%M)

find portal/public -name "*.html" -type f -exec \
  sed -i "s/sidebar\.js?v=[^\"']*/sidebar.js?v=${VERSION}/g" {} \;

echo "Updated cache version to: $VERSION"
```

### 2. Use Build Process
For production, use a build tool like Webpack/Vite:
- Generates hashed filenames: `sidebar.abc123.js`
- Browser automatically fetches new hash
- No manual version management needed

### 3. CDN Configuration
If using Cloudflare/CloudFront:
- Set TTL (Time To Live) to 1 hour for JS/CSS
- Set longer TTL (1 week) for images
- Use "Purge Cache" feature when deploying

### 4. Monitor Cache Headers
Add monitoring to verify correct headers:
```bash
# Check every hour
0 * * * * curl -sI https://wasabi.intel50001.com/js/sidebar.js | \
  grep -E "Cache-Control|Expires" | \
  mail -s "Cache Header Check" admin@example.com
```

---

## Related Files Modified

### Nginx Configuration
- ✅ `nginx/conf.d/default.conf` - Updated cache policies

### HTML Files (Version Parameters Added)
- ✅ `portal/public/pilot-factory-call.html`
- ✅ `portal/public/pilot-factory-application.html`
- ✅ `portal/public/pilot-factory-thank-you.html`
- ✅ `portal/public/admin/pilot-applications.html`
- ✅ `portal/public/admin/pilot-application-detail.html`

### JavaScript Files (Source)
- ℹ️ `portal/public/js/sidebar.js` - Contains the pilot factory link

---

## Verification Checklist

- [x] Nginx configuration updated (immutable → must-revalidate)
- [x] Nginx restarted
- [x] Version parameters added to pilot factory pages
- [x] Cache headers verified with curl
- [x] Tested in Chrome (after cache clear)
- [x] Tested in Edge InPrivate
- [x] Sidebar shows "Pilot Factory Call" link
- [x] Link works and navigates to invitation page
- [x] Documentation created

---

## Impact

**Before:**
- Users could wait up to 7 days to see updates
- Hard refresh didn't work due to `immutable` flag
- Required multiple cache-clearing attempts

**After:**
- Updates visible within 1 hour automatically
- Hard refresh works properly
- Version parameters force immediate updates
- Professional cache management

---

## Lessons Learned

1. **"immutable" is dangerous** for frequently updated files
   - Only use for versioned/hashed filenames (e.g., `app.v1.2.3.js`)
   - Never use for files that might change

2. **Always test on production domain** (wasabi.intel50001.com)
   - Different domain = different cache
   - IP address access (10.33.10.104) has separate cache

3. **Hard refresh doesn't bypass all caching**
   - `immutable` flag overrides hard refresh
   - Version parameters are more reliable

4. **Browser caching is per-domain**
   - http://10.33.10.104:8080 ≠ https://wasabi.intel50001.com
   - Each domain has separate cache storage

5. **Chrome vs Edge caching behavior differs**
   - Edge InPrivate seemed more aggressive at clearing
   - Chrome held onto cached version longer

---

## Support Information

**If Users Still Can't See Changes:**

1. Check nginx cache headers:
   ```bash
   curl -I https://wasabi.intel50001.com/js/sidebar.js
   ```

2. Verify version parameter:
   ```bash
   curl https://wasabi.intel50001.com/pilot-factory-call.html | grep "sidebar.js"
   ```

3. Force re-fetch:
   ```bash
   # Update version number
   docker compose exec nginx sed -i 's/v=20260102/v=20260103/g' \
     /usr/share/nginx/html/portal/public/pilot-factory-call.html
   ```

---

**Status:** ✅ Issue Resolved  
**Last Updated:** January 2, 2026  
**Next Review:** Before next major deployment

---

_This document serves as both a resolution log and a guide for future cache-related issues._

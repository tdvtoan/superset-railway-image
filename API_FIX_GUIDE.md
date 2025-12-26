# Superset API Fix Guide - Railway Deployment

## Issues Found & Fixed

### Issue 1: Missing Flask SECRET_KEY ❌ → ✅ FIXED

**Problem:**
- `superset_config.py` was setting `SUPERSET_SECRET_KEY`
- Flask requires `SECRET_KEY` (not `SUPERSET_SECRET_KEY`)
- This caused Flask to fail initialization, resulting in "Fatal error" on login

**Fix Applied:**
```python
# Before (Line 33):
SUPERSET_SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "temporary_superset_secret_key")

# After (Line 34):
SECRET_KEY = os.environ.get("SECRET_KEY") or os.environ.get("SUPERSET_SECRET_KEY", "temporary_superset_secret_key")
```

### Issue 2: Hardcoded Admin Password ❌ → ✅ FIXED

**Problem:**
- `startup.sh` hardcoded admin password as "admin" (line 40)
- Didn't read `SUPERSET_ADMIN_PASSWORD` from environment
- Admin initialization couldn't use custom credentials

**Fix Applied:**
```bash
# Before (Line 40):
ADMIN_PASSWORD="admin"

# After (Lines 40-44):
ADMIN_PASSWORD="${SUPERSET_ADMIN_PASSWORD:-admin}"
ADMIN_USERNAME="${SUPERSET_ADMIN_USER:-admin}"
ADMIN_EMAIL="${SUPERSET_ADMIN_EMAIL:-admin@example.com}"
ADMIN_FIRSTNAME="${SUPERSET_ADMIN_FIRSTNAME:-Superset}"
ADMIN_LASTNAME="${SUPERSET_ADMIN_LASTNAME:-Admin}"
```

## How to Deploy the Fix

### Step 1: Commit the Changes
```bash
cd /Users/tonytran/Documents/GitHub/superset-railway-image
git add -A
git commit -m "fix: Add Flask SECRET_KEY and support environment-based admin credentials"
```

### Step 2: Set Railway Environment Variables

In your Railway dashboard:

1. Go to your Superset deployment
2. Click **Variables** tab
3. Add these environment variables:

```
# CRITICAL: Flask SECRET_KEY (was missing!)
SECRET_KEY=superset-production-secret-key-$(openssl rand -hex 32)

# Or use a simpler key:
SECRET_KEY=your-super-secret-production-key-2025

# Admin Credentials
SUPERSET_ADMIN_USER=admin
SUPERSET_ADMIN_PASSWORD=#Stayahead88
SUPERSET_ADMIN_EMAIL=admin@example.com
SUPERSET_ADMIN_FIRSTNAME=Admin
SUPERSET_ADMIN_LASTNAME=User

# Database (if using external)
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host/dbname

# Optional: Redis for caching
SUPERSET_CACHE_REDIS_URL=redis://localhost:6379/0
```

### Step 3: Redeploy

1. Go to **Deployments** tab
2. Click the latest deployment
3. Click **Redeploy** or
4. Push a new commit to trigger auto-deploy

The deployment will:
1. Build the Docker image
2. Run `startup.sh` which will:
   - Apply database migrations
   - Create admin user with your credentials
   - Initialize Superset
   - Start the web server

## Testing After Fix

### Test 1: Check if API is Working
```bash
# Test login endpoint
curl -X POST https://superset-railway-image-production-6d86.up.railway.app/api/v1/security/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"#Stayahead88"}'

# Expected response (Status 200):
# {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGc...","refresh_token":"..."}
```

### Test 2: Run Dashboard Creation Script
```bash
python3 create_superset_dashboard.py
# Should now work without "Fatal error"
```

## What Changed in This Repository

**Files Modified:**
1. `superset_config.py` - Fixed SECRET_KEY configuration
2. `startup.sh` - Added environment variable support for admin credentials

**Files Added (in .claude/plugins/):**
- `.claude/plugins/superset-integration/` - Superset skill
- `.claude/plugins/superset-integration/SKILL.md` - Main skill documentation
- `.claude/plugins/superset-integration/references/` - API and dashboard guides
- `.claude/plugins/superset-integration/examples/` - Working code examples

**Helper Scripts:**
- `create_superset_dashboard.py` - Python API client to create dashboards
- `diagnose_superset.py` - Diagnostic tool for API issues
- `SUPERSET_RAILWAY_FIX.md` - Alternative fix guide

## Why This Happened

The original configuration had these issues:

1. **SECRET_KEY vs SUPERSET_SECRET_KEY**: Flask's security middleware looks for `SECRET_KEY`, not Superset's custom `SUPERSET_SECRET_KEY`. The config file was setting the wrong variable name.

2. **Hardcoded Credentials**: Startup script hardcoded "admin" password instead of reading environment variables, making it impossible to set custom credentials at deployment time.

3. **No Admin Initialization from Environment**: Railway's variable injection system couldn't override the admin credentials because they were hardcoded in shell variables.

## Verification Checklist

After deployment:

- [ ] Railway deployment completes successfully
- [ ] Check logs for "Loaded superset_config: env=production"
- [ ] No "Fatal error" in logs
- [ ] Login test returns access token (Status 200)
- [ ] Can query `/api/v1/databases` with token
- [ ] Dashboard creation script runs successfully
- [ ] Log events dashboard is created and published

## Rollback (if needed)

If something goes wrong:

```bash
git revert <commit-hash>
git push
# Railway will auto-redeploy previous version
```

## Additional Notes

- The fixes are backward compatible - if environment variables aren't set, defaults are used
- Admin credentials can be changed at runtime via environment variables on each deployment
- SECRET_KEY should be a strong random string in production
- The skill at `.claude/plugins/superset-integration/` is ready to use for both API and UI guidance

## Next Steps

1. Commit and deploy the fix
2. Test the API using the test commands above
3. Run `create_superset_dashboard.py` to create your first dashboard
4. Use the Superset skill (available when Claude Code is started in this folder) for guidance

## Support

- Check Railway logs if deployment fails
- See `SUPERSET_RAILWAY_FIX.md` for additional troubleshooting
- See `.claude/plugins/superset-integration/SKILL.md` for Superset guidance

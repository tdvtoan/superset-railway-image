# Fix Superset API on Railway Deployment

## Problem
Superset UI works, but API login returns "Fatal error" (500 status). This indicates the Flask app isn't properly initialized.

## Root Causes
1. **Missing Flask Secret Key** - Superset needs `SECRET_KEY` environment variable
2. **Database Not Initialized** - Superset metadata database needs migrations
3. **Missing Admin Account** - Even with defaults, initialization must run
4. **Missing FLASK_APP** - The Flask app entry point not specified

## Solution

### Option 1: Fix via Railway Dashboard (Recommended)

**Step 1: Access Railway Variables**
1. Go to your Railway project dashboard
2. Select your Superset deployment
3. Go to **Variables** tab

**Step 2: Add/Update These Environment Variables**

Add these critical variables:

```
# Flask Configuration
FLASK_APP=superset.app:create_app
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this-12345

# Superset Admin
SUPERSET_ADMIN_USER=admin
SUPERSET_ADMIN_PASSWORD=#Stayahead88
SUPERSET_LOAD_EXAMPLES=False

# Database (Superset internal - uses SQLite by default, which should work)
# If using external Postgres for Superset metadata:
# SQLALCHEMY_DATABASE_URI=postgresql://user:pass@host/dbname

# Redis (optional but recommended for caching)
# REDIS_URL=redis://localhost:6379/0

# Python/Gunicorn
GUNICORN_CMD_ARGS=--workers=2 --timeout=120
```

**Step 3: Save and Redeploy**
1. Click **Save** on variables
2. Railway will automatically redeploy
3. Wait for deployment to complete (3-5 minutes)
4. Test login again

---

### Option 2: Fix via Dockerfile (If you control the image)

If you have a custom Dockerfile, ensure it includes initialization:

```dockerfile
# Ensure this command runs during build/startup
RUN superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@example.com \
    --password '#Stayahead88'

# Initialize database
RUN superset db upgrade

# Load examples (optional)
# RUN superset load_examples
```

---

### Option 3: Verify Current Configuration

Check what Railway is currently using:

**In Railway Dashboard:**
1. Select Superset deployment
2. Go to **Logs** tab
3. Look for startup errors - search for:
   - "Fatal error"
   - "SECRET_KEY"
   - "database"
   - "migration"

Common error patterns:
```
KeyError: 'SECRET_KEY'  ← Missing SECRET_KEY variable
sqlalchemy.exc.OperationalError  ← Database connection issue
No module named  ← Missing dependencies
```

---

## Testing After Fix

### Test 1: Verify Login Works
```bash
curl -X POST https://superset-railway-image-production-6d86.up.railway.app/api/v1/security/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"#Stayahead88"}'

# Expected response (200):
# {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGc...","refresh_token":"..."}
```

### Test 2: Get Databases
```bash
TOKEN="your-access-token-from-above"
curl https://superset-railway-image-production-6d86.up.railway.app/api/v1/databases \
  -H "Authorization: Bearer $TOKEN"

# Should return list of databases
```

---

## Common Issues & Solutions

### Issue: "Invalid credentials"
**Cause:** PASSWORD doesn't match SUPERSET_ADMIN_PASSWORD
**Fix:** Ensure both match in .env.local and Railway variables

### Issue: "Database connection error"
**Cause:** Superset metadata database not accessible
**Fix:**
- Check database credentials
- Verify network access
- Use SQLite if no external DB: `SQLALCHEMY_DATABASE_URI=sqlite:///superset.db`

### Issue: "Secret key not set"
**Cause:** SECRET_KEY environment variable missing
**Fix:** Add `SECRET_KEY=your-random-secret-key` to Railway variables

### Issue: Still getting "Fatal error"
**Steps:**
1. Restart deployment: Railway dashboard → Deployment → Restart
2. Check recent logs for specific error
3. Redeploy from scratch if needed

---

## Step-by-Step Fix Process

### For Superset on Railway:

1. **Add SECRET_KEY**
   - Go to Railway project → Superset deployment → Variables
   - Add: `SECRET_KEY=superset-secret-key-$(openssl rand -hex 32)`
   - (Or use any random string: `SECRET_KEY=your-super-secret-12345`)

2. **Add FLASK_APP**
   - Add: `FLASK_APP=superset.app:create_app`
   - Add: `FLASK_ENV=production`

3. **Verify Admin Credentials**
   - Add: `SUPERSET_ADMIN_USER=admin`
   - Add: `SUPERSET_ADMIN_PASSWORD=#Stayahead88`

4. **Save Variables**
   - Click Save
   - Railway auto-redeploys

5. **Wait for Deployment**
   - Monitor logs
   - Wait for "ready" status

6. **Test**
   ```bash
   python3 create_superset_dashboard.py
   ```

---

## If You Don't Have Railway Access

If you can't modify Railway variables:

1. **Contact Railway Support** - They can help configure environment variables
2. **Use Manual Dashboard Creation** - Use the UI instead of API (fully functional)
3. **Redeploy with Different Image** - Use official Superset image with proper env vars

---

## After Fix: Complete Workflow

Once API is fixed, run the dashboard creation script:

```bash
python3 create_superset_dashboard.py
```

This will:
1. Authenticate to Superset
2. Find your "supabase staging" database
3. Create dataset from peter_log_event table
4. Create 4 visualizations
5. Build dashboard
6. Publish it live

---

## References

- [Superset Configuration](https://superset.apache.org/docs/installation/configuring-superset)
- [Railway Documentation](https://docs.railway.app/)
- [Superset GitHub Issues](https://github.com/apache/superset/issues)

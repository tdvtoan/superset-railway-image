# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository provides a 1-click deployment template for Apache Superset on Railway.app. It is NOT the core Apache Superset codebase - it's a deployment wrapper that:
- Extends the official `apache/superset:latest` Docker image
- Adds Google Cloud integrations (BigQuery, Cloud Storage)
- Configures Redis caching and Celery for Railway environments
- Handles database initialization and admin user creation

## Architecture

### Docker Build Process
1. **Base Image**: Extends `apache/superset:latest` (do not modify core Superset code)
2. **Environment Variable Substitution**: `superset_config.py` uses `envsubst` to inject Railway environment variables at build time into `/app/docker/superset_config.py`
3. **Startup Flow**:
   - `startup.sh` → calls `bootstrap.sh` → runs `superset db upgrade` → creates admin user → runs `superset init` → starts web server via `/usr/bin/run-server.sh`

### Configuration Architecture
- **superset_config.py**: Template file that reads ALL configuration from environment variables (DATABASE_URL, REDIS_URL, SUPERSET_SECRET_KEY, etc.)
- **Environment-driven**: Never hardcode values - all config must come from env vars for Railway compatibility
- **Redis Setup**: Uses same Redis instance for cache (DB 0), Celery results (DB 0), and Celery broker (DB 1)

### Key Files
- `Dockerfile`: Multi-stage build with environment variable substitution
- `superset_config.py`: Configuration template (gets processed by envsubst)
- `startup.sh`: Database migration, admin user creation, and server startup
- `bootstrap.sh`: Installs local requirements if present

## Development Commands

### Building and Testing Locally
```bash
# Build the Docker image (requires environment variables)
docker build \
  --build-arg DATABASE_URL="postgresql://..." \
  --build-arg REDIS_URL="redis://..." \
  --build-arg SUPERSET_SECRET_KEY="your-secret-key" \
  -t superset-railway .

# Run locally (mount config for live changes)
docker run -p 8088:8088 \
  -e DATABASE_URL="postgresql://..." \
  -e REDIS_URL="redis://..." \
  -e SUPERSET_SECRET_KEY="your-secret-key" \
  superset-railway
```

### Testing Configuration Changes
When modifying `superset_config.py`:
1. Use `os.environ.get()` for all values
2. Provide sensible defaults for local dev (except secrets)
3. Test environment variable substitution: `envsubst < superset_config.py`
4. Never log sensitive values (SECRET_KEY, DATABASE_URL with passwords)

### Shell Access for Debugging
```bash
# Access running container
docker exec -it <container_id> /bin/bash

# Check processed config
cat /app/docker/superset_config.py

# Test Superset CLI
superset --help
```

## Environment Variables

Required by Railway (set in Railway dashboard):
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL` or `REDISHOST`+`REDISPORT`: Redis connection
- `SUPERSET_SECRET_KEY`: Flask secret key (generate with `openssl rand -base64 42`)

Optional:
- `SUPERSET_LOAD_EXAMPLES`: Set to "yes" to load example datasets
- `SUPERSET_PORT`: Default 8088

## Important Constraints

### Do Not:
- Modify core Superset functionality (we extend the official image)
- Hardcode credentials or connection strings
- Add build steps that require internet access at runtime
- Change the admin user creation logic in startup.sh without updating README

### Railway-Specific:
- All config MUST support environment variable substitution via `envsubst`
- Variables referenced in superset_config.py as `${VAR_NAME}` are replaced during build
- Python config uses `os.environ.get()` to read runtime environment variables

## Default Credentials
- Username: `admin`
- Password: `admin`
- Created during first startup in startup.sh:54-60

## Adding Python Dependencies
Add to Dockerfile RUN pip install section (line 30-36):
```dockerfile
RUN pip install --no-cache-dir \
    existing-package \
    your-new-package
```

## Common Issues

### Config Not Loading
- Check that `/app/docker/superset_config.py` exists in container
- Verify envsubst processed variables correctly: `docker exec <id> cat /app/docker/superset_config.py`
- Ensure SUPERSET_CONFIG_PATH env var is set to `/app/docker/superset_config.py`

### Database Connection Failures
- Verify DATABASE_URL format includes `postgresql://` or `postgresql+psycopg2://`
- Check that Railway PostgreSQL service is provisioned and connected

### Redis Connection Issues
- Confirm REDIS_URL is set and reachable
- Check Redis DB indices: broker uses DB 1, cache/results use DB 0

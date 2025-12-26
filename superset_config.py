import os
import sys
import logging

logger = logging.getLogger()

# Optionally extend PYTHONPATH if provided
PYTHONPATH = os.environ.get("PYTHONPATH", "")
if PYTHONPATH:
    for p in PYTHONPATH.split(os.pathsep):
        if p and p not in sys.path:
            sys.path.insert(0, p)

# Helper to interpret booleans from env strings
def _env_bool(name, default=False):
    val = os.environ.get(name)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "on")

# Read environment values safely
SUPERSET_CACHE_REDIS_URL = os.environ.get("SUPERSET_CACHE_REDIS_URL", "")
RATELIMIT_STORAGE_URI = SUPERSET_CACHE_REDIS_URL or os.environ.get("RATELIMIT_STORAGE_URI", "")

# Get database URI - prefer DATABASE_URL over SQLALCHEMY_DATABASE_URI to avoid template strings
_db_uri = os.environ.get("SQLALCHEMY_DATABASE_URI", "")
# If SQLALCHEMY_DATABASE_URI contains template syntax or is empty, use DATABASE_URL instead
if not _db_uri or "${" in _db_uri:
    _db_uri = os.environ.get("DATABASE_URL", "")
SQLALCHEMY_DATABASE_URI = _db_uri
SUPERSET_ENV = os.environ.get("SUPERSET_ENV", "production")
SUPERSET_LOAD_EXAMPLES = _env_bool("SUPERSET_LOAD_EXAMPLES", False)
# Flask needs SECRET_KEY, not SUPERSET_SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY") or os.environ.get("SUPERSET_SECRET_KEY", "temporary_superset_secret_key")
# Ports: try converting to int, with sensible defaults
try:
    SUPERSET_PORT = int(os.environ.get("SUPERSET_PORT", 8088))
except ValueError:
    SUPERSET_PORT = 8088

REDIS_HOST = os.environ.get("REDIS_HOST", "")
try:
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
except ValueError:
    REDIS_PORT = 6379
REDIS_URL = os.environ.get("REDIS_URL", os.environ.get("CACHE_REDIS_URL", ""))

# Cache configuration (use URLs when available)
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST or None,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": 0,
    "CACHE_REDIS_URL": REDIS_URL or SUPERSET_CACHE_REDIS_URL,
}
DATA_CACHE_CONFIG = CACHE_CONFIG

class CeleryConfig(object):
    # Use the redis url and append DB index for broker and result backend
    BROKER_URL = (SUPERSET_CACHE_REDIS_URL or REDIS_URL) + "/1" if (SUPERSET_CACHE_REDIS_URL or REDIS_URL) else None
    CELERY_IMPORTS = ("superset.sql_lab",)
    CELERY_RESULT_BACKEND = (SUPERSET_CACHE_REDIS_URL or REDIS_URL) + "/0" if (SUPERSET_CACHE_REDIS_URL or REDIS_URL) else None
    CELERY_ANNOTATIONS = {"tasks.add": {"rate_limit": "10/s"}}

CELERY_CONFIG = CeleryConfig

# Expose useful variables to Superset
RATELIMIT_STORAGE_URI = RATELIMIT_STORAGE_URI
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
SUPERSET_CACHE_REDIS_URL = SUPERSET_CACHE_REDIS_URL

# Other Superset settings
REDIS_HOST = REDIS_HOST
REDIS_PORT = REDIS_PORT
SUPERSET_ENV = SUPERSET_ENV
SUPERSET_LOAD_EXAMPLES = SUPERSET_LOAD_EXAMPLES
SECRET_KEY = SECRET_KEY
SUPERSET_PORT = SUPERSET_PORT

# Optional: log what we loaded (avoid logging secrets)
logger.info("Loaded superset_config: env=%s, load_examples=%s, redis_host=%s, redis_port=%s",
            SUPERSET_ENV, SUPERSET_LOAD_EXAMPLES, REDIS_HOST, REDIS_PORT)

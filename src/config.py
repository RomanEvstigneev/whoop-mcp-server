"""
Configuration for WHOOP MCP Server
"""
import os
from typing import Optional

# OAuth application endpoints
OAUTH_BASE_URL = "https://personal-integrations-462307.uc.r.appspot.com"
OAUTH_AUTH_URL = f"{OAUTH_BASE_URL}/"
OAUTH_TOKEN_URL = f"{OAUTH_BASE_URL}/api/get-tokens"
OAUTH_REFRESH_URL = f"{OAUTH_BASE_URL}/api/refresh-token"

# WHOOP API configuration
WHOOP_API_BASE = "https://api.prod.whoop.com/developer/v1"
WHOOP_SCOPES = [
    "read:profile",
    "read:workout", 
    "read:sleep",
    "read:recovery",
    "offline"
]

# Storage configuration
import os
HOME_DIR = os.path.expanduser("~")
STORAGE_DIR = os.path.join(HOME_DIR, ".whoop-mcp-server")
TOKEN_STORAGE_PATH = os.path.join(STORAGE_DIR, "tokens.json")
CACHE_STORAGE_PATH = os.path.join(STORAGE_DIR, "cache.json")
CACHE_DURATION = 300  # 5 minutes

# Security configuration
ENCRYPTION_KEY_FILE = os.path.join(STORAGE_DIR, ".encryption_key")

# Rate limiting
MAX_REQUESTS_PER_MINUTE = 100
REQUEST_TIMEOUT = 30  # seconds

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', None)  # None means console only